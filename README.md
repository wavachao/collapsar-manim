# 黑洞：宇宙的单向门

中文 Manim 科普短片：深空星点、青紫光轨、动态公式、光锥、双时钟和时空网格。中文合成配音、内嵌字幕与原创程序合成氛围音均随构建生成。

## 播放与复现

最终视频：`output/black_hole_science.mp4`（4 分 15 秒）；字幕：`output/black_hole_science.srt`。九幅成片分镜：`output/storyboard.jpg`；完整解码验证报告：`output/validation.json`。

在 Windows PowerShell 中执行：

```powershell
uv sync --locked
uv run python build.py --quality preview
uv run python build.py --quality final
```

`preview` 为 480p / 15 fps，`final` 为 1920 × 1080 / 30 fps。默认输出 H.264 视频与 AAC 音频，可在普通播放器中打开。安装的包由 `uv.lock` 固定；FFmpeg 使用 imageio-ffmpeg 自带版本。数学公式使用 Manim MathTex，需可用的 LaTeX 与 dvisvgm（本机 TeX Live 2024 已验证）；数字使用 Text。

本机配音使用 Windows `System.Speech` 的 `Microsoft Huihui Desktop` 中文语音；中文画面使用 `Microsoft YaHei` 字体。其他操作系统需替换 `build.py` 的配音生成函数与字体。语音首先生成到 `media/voice/`，按文本哈希缓存；修改文字即可生成新语音。`--voice-only` 只生成配音，`--skip-render` 使用现有画面重新混音。

## 内容结构

1. 黑洞不是吸尘器：同质量替换太阳的轨道思想实验，角动量与吸积。
2. 逃逸速度的直觉推导与事件视界的因果解释；远处红移、变暗和落入者视角。
3. 静止、无旋转黑洞外的理想双时钟比较，以及重逢时的时间差。
4. 折纸类比虫洞，清楚区分几何猜想、可穿越条件和观测证据。
5. 爱因斯坦场方程与证据边界。

关键科学依据与制作限制见 [docs/SCIENCE.md](docs/SCIENCE.md)。图形是简化示意，不是数值相对论仿真；视界内的光锥只表示因果趋势，折纸不会真的生成虫洞。成片没有声称黑洞可以通往过去。

## 修改与 Git 分工

- `black_hole.py`：主场景、前半段、字幕和时间线。
- `spacetime.py`：后半段时间与虫洞动画。
- `build.py`：本地语音、Manim 渲染、音轨合成、SRT 与 MP4。
- `PLAN.md`：执行前保存的制作计划。
- `docs/PRODUCTION.md`：worktree 分工和交付验证记录。

两个 subagent 分别在 `.worktrees/science`（`science-script` 分支）与 `.worktrees/spacetime`（`spacetime-scenes` 分支）制作并提交，通过 cherry-pick 合并到主分支。虚拟环境、worktree 和生成媒体均不进入 Git。
