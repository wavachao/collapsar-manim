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

待成片渲染后补充实际规格与检查结果。
