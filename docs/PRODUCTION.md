# 制作记录

## 并行协作

执行前先提交 PLAN.md（ac39dec），随后创建两个独立 Git worktree：

| 分工 | worktree | 分支 | subagent 提交 | 合并提交 |
|---|---|---|---|---|
| 科学核验与解说建议 | .worktrees/science | science-script | 4f8fa30 | 4e199e9 |
| 双时钟与虫洞动画 | .worktrees/spacetime | spacetime-scenes | 372255e | 627d3f3 |

主 agent 负责 uv 环境、统一视觉接口、前半段动画、语音、混音、预览检查与最终成片。

## 视觉与声音

采用 16:9 深空背景、青紫几何网格、金色物质轨迹、数学公式逐步变换。全部画面由 Manim 原生矢量对象生成，不依赖外部图像。中文声音由 Windows 本地 Huihui 引擎合成，音轨使用原创正弦波低音氛围和章节扫频。解说及字幕时间来自实际语音长度。

## 验证

- 成片：`output/black_hole_science.mp4`，255 秒（4:15），1920 × 1080，标称 30 fps，H.264 / AAC，48 kHz 单声道，15,713,758 字节。
- 完整解码所有 7,650 帧及完整音轨，通过帧数/时长一致性检查。容器平均帧率因末帧时间戳舍入略偏离 30，基础帧率为精确 30。
- 23 段中文配音，38 条字幕；每条最多 30 字，时间来自实际渲染帧边界，无字幕重叠。段内文字与语音按字数近似对齐，不是逐字强制对齐。
- AAC 解码峰值 0.8764，未过载；音轨 RMS 0.04984。
- 实际预览迭代后检查轨道、数学推导、视界光锥、双时钟、折叠空间、弯曲网格与片尾。最终渲染日志没有 WARNING、ERROR 或 Traceback。
- 核心公式改为实际 MathTex；LaTeX/dvisvgm 在本机 TeX Live 2024 中已验证。字幕保持 Microsoft YaHei 矢量文字。
- 修正角动量输运表述、视界内示意光锥方向、淡出对象闪回、时钟文字与方程网格重叠；字幕结束时间对齐渲染帧边界。
- 检查报告：`output/validation.json`；九幅成片分镜：`output/storyboard.jpg`；可选独立字幕：`output/caption_exports/black_hole_science.transcript.srt`。

## 字幕重叠修复

视频已烧录画内字幕，旧版同时在视频旁导出同名 SRT，播放器可能自动加载并叠加。默认构建现仅保留画内字幕；独立字幕需 --export-srt 显式导出，并放在 caption_exports 目录、使用 transcript 文件名。旧同名字幕迁移至该目录，保留可编辑文本。未删除画内字幕，也无需重新渲染数学画面。

## 复现范围

本项目使用本机 Windows 中文语音与微软雅黑字体；换机需具备这些系统资源及 LaTeX/dvisvgm。uv 负责 Python 环境和依赖锁定。影片为教学几何示意，不是相对论数值模拟；黑洞穿越到过去没有被描绘为已实现的事实。
