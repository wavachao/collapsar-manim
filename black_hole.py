"""Manim: a Chinese journey from gravity to the limits of time travel."""
from pathlib import Path
import hashlib
import json
import wave
import numpy as np
from manim import *
from spacetime import SpacetimeMixin

BG = "#050914"
CYAN = "#55E8FF"
PURPLE = "#A58AFF"
GOLD = "#FFCE73"
ROOT = Path(__file__).parent


def subtitle_chunks(text, limit=30):
    chunks = []
    while len(text) > limit:
        cuts = [i + 1 for i, c in enumerate(text[:limit]) if c in "，。；：！？" and i >= 12]
        cut = cuts[-1] if cuts else limit
        chunks.append(text[:cut])
        text = text[cut:]
    if text:
        chunks.append(text)
    return chunks


class BlackHoleFilm(SpacetimeMixin, Scene):
    def text(self, value, font_size=28, color=WHITE):
        return Text(value, font="Microsoft YaHei", font_size=font_size, color=color)

    def formula(self, text, font_size=40):
        equations = {
            "F = GMm / r²": r"F=\frac{GMm}{r^2}",
            "½mv² = GMm / r": r"\frac12 mv^2=\frac{GMm}{r}",
            "v = √(2GM/r)": r"v=\sqrt{\frac{2GM}{r}}",
            "rₛ = 2GM / c²": r"r_s=\frac{2GM}{c^2}",
            "rₛ": r"r_s",
            "dτ/dt = √(1 − rₛ/r)": r"\frac{d\tau}{dt}=\sqrt{1-\frac{r_s}{r}}",
            "r = 4rₛ/3  →  dτ/dt = 0.5": r"r=\frac43 r_s\quad\Longrightarrow\quad\frac{d\tau}{dt}=0.5",
            "Gμν = (8πG/c⁴) Tμν": r"G_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}",
        }
        if text in equations:
            return MathTex(equations[text], font_size=font_size, color=CYAN)
        return Text(text, font="Microsoft YaHei", font_size=font_size, color=CYAN)

    def caption(self, text):
        if self.subtitle is not None:
            self.remove(self.subtitle)
        line = self.text(text, 27)
        if line.width > 12.4:
            line.scale_to_fit_width(12.4)
        line.move_to([0, -3.38, 0])
        self.subtitle = line
        self.add(line)

    def say(self, text, duration=3):
        key = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        wav = ROOT / "media" / "voice" / f"{key}.wav"
        voice_length = 0
        if wav.exists():
            with wave.open(str(wav)) as stream:
                voice_length = stream.getnframes() / stream.getframerate()
        span = max(duration, voice_length + .3)
        chunks = subtitle_chunks(text)
        cues = []
        start = float(self.time)
        for chunk in chunks:
            chunk_duration = span * len(chunk) / len(text)
            cue_start = float(self.time)
            self.caption(chunk)
            self.wait(chunk_duration)
            cues.append({"start": cue_start, "duration": float(self.time) - cue_start, "text": chunk})
        self.timeline.append({"start": start, "duration": float(self.time) - start,
                              "text": text, "file": str(wav), "cues": cues})

    def section(self, number, title, kicker):
        if len(self.body):
            self.play(FadeOut(self.body), run_time=.65)
            self.remove(self.body)
        if self.subtitle is not None:
            self.remove(self.subtitle)
            self.subtitle = None
        self.body = VGroup()
        title_group = VGroup(self.text(f"{number} / {title}", 30, CYAN),
                             self.text(kicker, 16, PURPLE)).arrange(DOWN, buff=.13)
        title_group.move_to([0, 3.22, 0])
        self.body.add(title_group)
        self.play(FadeIn(title_group, shift=DOWN * .15), run_time=.6)
        self.chapter_times.append(float(self.time))

    def hole(self, radius=1, center=ORIGIN):
        glow = VGroup(*[Circle(radius=radius + i * .035,
                              color=PURPLE if i > 3 else CYAN,
                              stroke_width=2 + i, stroke_opacity=.12 / (1 + i * .15))
                        for i in range(9, -1, -1)])
        disk = Circle(radius=radius, fill_color=BLACK, fill_opacity=1,
                      stroke_color=CYAN, stroke_width=2)
        return VGroup(glow, disk).move_to(center)

    def construct(self):
        self.timeline, self.chapter_times = [], []
        self.body = VGroup()
        self.subtitle = None
        rng = np.random.default_rng(71)
        stars = VGroup(*[Dot([rng.uniform(-7, 7), rng.uniform(-3.85, 3.85), 0],
                            radius=rng.uniform(.008, .022), color=WHITE,
                            fill_opacity=rng.uniform(.12, .5)) for _ in range(85)])
        grid = VGroup(*[Line([-7, y, 0], [7, y, 0], color=CYAN,
                            stroke_width=.4, stroke_opacity=.06)
                       for y in np.arange(-3, 3.1, .5)])
        self.add(stars, grid)
        border = VGroup(Line([-6.7, -2.98, 0], [6.7, -2.98, 0],
                             color=CYAN, stroke_opacity=.25),
                        self.text("SPACETIME LAB  ·  GENERAL RELATIVITY", 13, PURPLE)
                        .move_to([0, -3.85, 0]))
        self.add(border)
        self.intro()
        self.gravity_chapter()
        self.horizon_chapter()
        self.time_chapter()
        self.wormhole_chapter()
        self.ending()
        out = ROOT / "media" / "timeline.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps({"duration": float(self.time), "segments": self.timeline,
                                   "chapters": self.chapter_times}, ensure_ascii=False, indent=2),
                       encoding="utf-8")

    def intro(self):
        hole = self.hole(.94, LEFT * 3.5)
        rings = VGroup(*[Ellipse(width=3.4 + i * .23, height=.65 + i * .08,
                                stroke_color=GOLD, stroke_width=1.5,
                                stroke_opacity=.6 - i * .06).rotate(.23)
                         .move_to(LEFT * 3.5) for i in range(6)])
        title = self.text("黑洞", 76).move_to([2, .85, 0])
        sub = self.text("宇宙的单向门", 34, CYAN).move_to([2, -.2, 0])
        question = self.text("吞噬万物？穿越时空？", 24, PURPLE).move_to([2, -1.15, 0])
        self.body.add(rings, hole, title, sub, question)
        self.play(Create(rings), FadeIn(hole), Write(title), run_time=2)
        self.play(FadeIn(sub), FadeIn(question), run_time=1)
        rings.add_updater(lambda m, dt: m.rotate(.045 * dt, about_point=LEFT * 3.5))
        self.say("如果光都逃不出来，黑洞会不会是时光机？", 3)
        self.say("让我们用数学，拆开这扇宇宙的单向门。", 3)
        rings.clear_updaters()

    def gravity_chapter(self):
        self.section("01", "黑洞不是宇宙吸尘器", "MASS → GEOMETRY → ORBIT")
        center = LEFT * 3.4 + DOWN * .1
        sun = Circle(.65, color=GOLD, fill_color=GOLD, fill_opacity=.85).move_to(center)
        orbit = Ellipse(width=4.6, height=3.8, color=CYAN, stroke_opacity=.6).move_to(center)
        earth = Dot(orbit.point_from_proportion(0), color=CYAN, radius=.095)
        phase = ValueTracker(0)
        earth.add_updater(lambda m: m.move_to(orbit.point_from_proportion((phase.get_value() + self.time * .055) % 1)))
        eq = self.formula("F = GMm / r²", 39).move_to([3.25, 1.05, 0])
        note = self.text("相同质量 · 相同距离", 27).move_to([3.25, .1, 0])
        label = self.text("远处弱场近似", 18, PURPLE).move_to([3.25, -.7, 0])
        self.body.add(sun, orbit, earth, eq, note, label)
        self.play(FadeIn(sun), Create(orbit), FadeIn(earth), Write(eq), FadeIn(note), FadeIn(label), run_time=1.6)
        self.say("先纠正一个误会：黑洞不会把整个宇宙吸进去。", 3)
        self.play(phase.animate.set_value(.55), run_time=2, rate_func=linear)
        black = self.hole(.65, center)
        self.play(ReplacementTransform(sun, black), run_time=1)
        self.body.remove(sun).add(black)
        self.play(phase.animate.set_value(1.2), run_time=2, rate_func=linear)
        self.say("太阳若换成同质量黑洞，忽略其他影响，地球仍会沿原轨道运行。", 3)
        earth.clear_updaters()
        self.say("真正决定命运的，是距离、速度，以及角动量。", 3)
        spiral = ParametricFunction(lambda t: center + np.array([
            (2.2 - 1.55 * t) * np.cos(4 * PI * t),
            (1.7 - 1.25 * t) * np.sin(4 * PI * t), 0]), t_range=[0, 1], color=GOLD)
        gas = Dot(spiral.get_start(), radius=.07, color=GOLD)
        self.body.add(spiral, gas)
        self.play(Create(spiral), FadeIn(gas), run_time=1)
        self.play(MoveAlongPath(gas, spiral), run_time=2.3, rate_func=linear)
        self.say("气体相互作用，把角动量向外输运，部分物质才逐渐旋入。", 3)
        self.say("发亮的是外面的吸积盘，黑洞本身仍然漆黑。", 3)

    def horizon_chapter(self):
        self.section("02", "为什么连光都逃不出？", "ESCAPE SPEED → EVENT HORIZON → CAUSALITY")
        eq1 = self.formula("½mv² = GMm / r", 42).move_to([0, 1.65, 0])
        eq2 = self.formula("v = √(2GM/r)", 42).move_to([0, .65, 0])
        eq3 = self.formula("rₛ = 2GM / c²", 48).move_to([0, -.45, 0])
        note = self.text("牛顿推导只提供直觉；视界需要广义相对论", 20, PURPLE).move_to([0, -1.4, 0])
        self.body.add(eq1, eq2, eq3, note)
        self.play(Write(eq1), run_time=1)
        self.play(TransformFromCopy(eq1, eq2), run_time=1)
        self.say("先用逃逸速度找直觉：天体越紧凑，逃离所需的速度越大。", 3)
        self.play(TransformFromCopy(eq2, eq3), FadeIn(note), run_time=1.3)
        self.say("令逃逸速度等于光速，得到史瓦西半径。太阳质量对应约三公里。", 3)
        self.play(FadeOut(VGroup(eq1, eq2, eq3, note)), run_time=.6)
        self.body.remove(eq1, eq2, eq3, note)
        hole = self.hole(1.05, LEFT * 3.65)
        horizon = DashedVMobject(Circle(1.35, color=CYAN).move_to(LEFT * 3.65), num_dashes=60)
        radius_line = Line([-3.65, 0, 0], [-2.3, 0, 0], color=CYAN)
        radius_label = self.formula("rₛ", 28).move_to([-2.95, .28, 0])
        hlabel = self.text("事件视界：因果边界", 23).move_to([-3.65, -2.1, 0])
        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-1.6, 1.6, .8],
                            x_length=4.2, y_length=3.2,
                            background_line_style={"stroke_color": PURPLE, "stroke_opacity": .18},
                            axis_config={"stroke_opacity": .35}).move_to([3.2, 0, 0])
        cone = Polygon([3.2, -.9, 0], [2.25, 1.4, 0], [4.15, 1.4, 0],
                       fill_color=CYAN, fill_opacity=.15, stroke_color=CYAN)
        arrows = VGroup(*[Arrow([3.2, -.9, 0], [x, .85, 0], buff=0, color=CYAN,
                                stroke_width=2) for x in [2.6, 3.2, 3.8]])
        ctext = self.text("未来允许的方向", 22).move_to([3.2, -2.1, 0])
        axis_labels = VGroup(self.text("r 增大 →", 15, PURPLE).move_to([5.15, -1.78, 0]),
                             self.text("示意时间 ↑", 15, PURPLE).move_to([1.35, 1.87, 0]))
        self.body.add(hole, horizon, radius_line, radius_label, hlabel, plane, cone, arrows, ctext, axis_labels)
        self.play(FadeIn(hole), Create(horizon), Create(radius_line), FadeIn(radius_label),
                  FadeIn(hlabel), Create(plane), FadeIn(cone), GrowFromCenter(arrows), FadeIn(ctext), FadeIn(axis_labels), run_time=2)
        self.say("更深的答案是时空几何：光锥规定了你能够走向的未来。", 3)
        inside_cone = Polygon([3.2, -.9, 0], [.95, 1.4, 0], [2.8, 1.4, 0],
                              fill_color=GOLD, fill_opacity=.15, stroke_color=GOLD)
        inside_arrows = VGroup(*[Arrow([3.2, -.9, 0], [x, .85, 0], buff=0, color=GOLD,
                                       stroke_width=2) for x in [1.5, 2.05, 2.6]])
        self.play(Transform(cone, inside_cone), Transform(arrows, inside_arrows),
                  ctext.animate.become(self.text("视界内：未来指向更小的 r", 22).move_to([3.2, -2.1, 0])), run_time=2)
        self.say("跨过视界后，所有未来方向都朝向更小的半径，连光也无法返回。", 3)
        self.say("光锥图是因果示意；黑洞不是一块可以撞上的实体表面。", 3)
        self.say("落入者可在有限自身时间内越过视界；远处看到的信号却越来越红、越来越暗。", 3)

    def ending(self):
        self.section("05", "宇宙最奇妙的，是规则本身", "THE FUTURE IS GEOMETRY")
        eq = self.formula("Gμν = (8πG/c⁴) Tμν", 48).move_to([0, .65, 0])
        left = self.text("时空如何弯曲", 25, CYAN).move_to([-3.1, -.3, 0])
        right = self.text("物质与能量", 25, GOLD).move_to([3.1, -.3, 0])
        lines = VGroup(*[ParametricFunction(lambda x, y=y: np.array([
            x, y - .65 * np.exp(-x*x/3) * np.cos(y), 0]),
            t_range=[-6, 6, .15], color=PURPLE, stroke_opacity=.4)
            for y in np.arange(-2.35, -1, .2)])
        self.body.add(eq, left, right, lines)
        self.play(Write(eq), FadeIn(left), FadeIn(right), LaggedStart(*[Create(l) for l in lines], lag_ratio=.06), run_time=2)
        self.say("物质告诉时空如何弯曲，时空告诉物质如何运动。", 3)
        self.say("黑洞是单向的因果边界。时间差有物理依据，穿洞回到过去仍是猜想。", 3)
        refs = self.text("科学资料：NASA Science · Einstein Online\n动画为简化示意；公式讨论静止、无旋转黑洞", 16, PURPLE).move_to([0, -2.5, 0])
        self.body.add(refs)
        self.play(FadeIn(refs), run_time=.8)
        self.wait(2)
