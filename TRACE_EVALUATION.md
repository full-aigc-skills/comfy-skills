# TRACE 评测报告

评测日期：2026-09-20。评测方法：固定版本确定性 TRACE 基分 + 人工语义复核。语义复核确认安全边界、外部副作用禁令、失败矩阵和验证契约与技能领域一致，本轮未做无证据的分数校准。

| Skill | T | R | A | C | E | Overall |
|---|---:|---:|---:|---:|---:|---:|
| comfy-generate-3d | 5.0 | 4.6 | 4.3 | 4.8 | 4.5 | 4.63 |
| comfy-generate-audio | 5.0 | 4.6 | 4.3 | 4.8 | 4.5 | 4.63 |
| comfy-generate-image | 5.0 | 4.6 | 4.3 | 4.8 | 4.5 | 4.63 |
| comfy-generate-video | 5.0 | 4.6 | 4.3 | 4.8 | 4.5 | 4.63 |
| comfy-help | 5.0 | 4.6 | 4.3 | 4.8 | 4.5 | 4.63 |
| comfy-remove-background | 5.0 | 4.6 | 4.3 | 4.8 | 4.5 | 4.63 |
| comfy-search-models | 5.0 | 4.6 | 4.3 | 4.7 | 4.5 | 4.62 |
| comfy-search-nodes | 5.0 | 4.6 | 4.3 | 4.7 | 4.5 | 4.62 |
| comfy-search-templates | 5.0 | 4.6 | 4.3 | 4.7 | 4.5 | 4.62 |
| comfy-upscale-image | 5.0 | 4.6 | 4.1 | 4.8 | 4.5 | 4.58 |
| technique-combine-people | 5.0 | 4.6 | 4.5 | 4.8 | 4.5 | 4.65 |

结论：11 个技能全部达到 4.5 发布门禁，平均 4.625；已删除高危 `comfy-rickroll`，并由 CI 阻止同类未经确认的主机副作用重新进入发行物。

发布前复跑：

```bash
python3 scripts/trace_gate.py --evaluator <trace_evaluate.py> --threshold 4.5
```
