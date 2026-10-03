"""Generate local Chinese narration, render Manim, then master an MP4."""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parent


def prepare_voice():
    folder = ROOT / "media" / "voice"
    folder.mkdir(parents=True, exist_ok=True)
    entries = []
    for filename in ["black_hole.py", "spacetime.py"]:
        tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "say" and node.args
                    and isinstance(node.args[0], ast.Constant)):
                text = node.args[0].value
                key = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
                entries.append({"text": text, "path": str(folder / f"{key}.wav")})
    (folder / "speech.json").write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8-sig")
    ps = folder / "speak.ps1"
    ps.write_text('''Add-Type -AssemblyName System.Speech
$taskSpeaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$taskSpeaker.SelectVoice("Microsoft Huihui Desktop")
$taskSpeaker.Rate = 1
$taskEntries = Get-Content -LiteralPath (Join-Path $PSScriptRoot "speech.json") -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($taskEntry in $taskEntries) {
    if (!(Test-Path -LiteralPath $taskEntry.path)) {
        $taskSpeaker.SetOutputToWaveFile($taskEntry.path)
        $taskSpeaker.Speak($taskEntry.text)
        $taskSpeaker.SetOutputToNull()
    }
}
$taskSpeaker.Dispose()
''', encoding="utf-8-sig")
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps)], check=True)
    missing = [e["path"] for e in entries if not Path(e["path"]).exists()]
    if missing:
        raise RuntimeError(f"Missing narration: {missing}")


def timestamp(seconds):
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3600000)
    minutes, millis = divmod(millis, 60000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def master(timeline, silent_video, destination, export_srt=False):
    import numpy as np
    import imageio_ffmpeg
    from scipy.signal import resample_poly
    sr = 48000
    duration = timeline["duration"]
    t = np.arange(math.ceil((duration + .1) * sr)) / sr
    # Original procedural drone, quiet beneath speech; no external music assets.
    ambient = .009 * (np.sin(2*np.pi*55*t) + .5*np.sin(2*np.pi*82.4*t)
                      + .3*np.sin(2*np.pi*110*t)) * (.65 + .35*np.sin(2*np.pi*.11*t)**2)
    envelope = np.minimum(t / 2, 1) * np.minimum(np.maximum(duration-t, 0) / 2, 1)
    mix = ambient * envelope
    subtitles = []
    for seg in timeline["segments"]:
        with wave.open(seg["file"]) as stream:
            rate, channels, width = stream.getframerate(), stream.getnchannels(), stream.getsampwidth()
            if width != 2:
                raise ValueError("Narration must be 16-bit PCM")
            audio = np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2").astype(float) / 32768
            audio = audio.reshape(-1, channels).mean(axis=1)
        divisor = math.gcd(sr, rate)
        audio = resample_poly(audio, sr//divisor, rate//divisor)
        start = round(seg["start"] * sr)
        count = min(len(audio), len(mix)-start)
        mix[start:start+count] += audio[:count] * .92
        for cue in seg["cues"]:
            subtitles.append(f"{len(subtitles)+1}\n{timestamp(cue['start'])} --> {timestamp(cue['start']+cue['duration'])}\n{cue['text']}\n")
    for chapter in timeline["chapters"]:
        n = int(sr * .6)
        local_t = np.arange(n) / sr
        whoosh = .026 * np.sin(2*np.pi*(180*local_t + 900*local_t**2)) * np.sin(np.pi*local_t/.6)**2
        start = round(chapter*sr)
        count = min(n, len(mix)-start)
        mix[start:start+count] += whoosh[:count]
    if np.max(np.abs(mix)) > .98:
        mix *= .98 / np.max(np.abs(mix))
    wav = ROOT / "media" / "master.wav"
    with wave.open(str(wav), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(sr)
        stream.writeframes((mix * 32767).astype("<i2").tobytes())
    destination.parent.mkdir(exist_ok=True)
    # The picture already has captions. A same-name SRT beside the MP4 is
    # automatically loaded by many players and creates a duplicate overlay.
    legacy_srt = destination.with_suffix(".srt")
    export_folder = destination.parent / "caption_exports"
    subtitle_path = export_folder / f"{destination.stem}.transcript.srt"
    if legacy_srt.exists():
        export_folder.mkdir(exist_ok=True)
        legacy_srt.replace(subtitle_path)
    if export_srt:
        export_folder.mkdir(exist_ok=True)
        subtitle_path.write_text("\n".join(subtitles), encoding="utf-8-sig")
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-i", str(silent_video), "-i", str(wav),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(destination)], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", choices=["preview", "final"], default="final")
    parser.add_argument("--skip-render", action="store_true", help="Remaster the existing render")
    parser.add_argument("--voice-only", action="store_true", help="Generate narration without rendering")
    parser.add_argument("--export-srt", action="store_true", help="Export optional captions separately; video already has captions")
    args = parser.parse_args()
    os.chdir(ROOT)
    prepare_voice()
    if args.voice_only:
        return
    quality = "480p15" if args.quality == "preview" else "1080p30"
    destination = ROOT / "output" / ("black_hole_preview.mp4" if args.quality == "preview" else "black_hole_science.mp4")
    if not args.skip_render:
        subprocess.run([sys.executable, "-m", "manim", "-ql" if args.quality == "preview" else "-qh",
                        "--fps", "15" if args.quality == "preview" else "30", "black_hole.py", "BlackHoleFilm"], check=True)
    silent_video = ROOT / "media" / "videos" / "black_hole" / quality / "BlackHoleFilm.mp4"
    timeline = json.loads((ROOT / "media" / "timeline.json").read_text(encoding="utf-8"))
    master(timeline, silent_video, destination, export_srt=args.export_srt)
    print(f"Delivered: {destination} ({timeline['duration']:.1f} seconds)")


if __name__ == "__main__":
    main()
