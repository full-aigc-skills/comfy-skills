# comfy-skills

面向 Codex、ZCode、Kimi 及其他 Agent Skills 客户端的 ComfyUI / Comfy Cloud 可复用技能包。

本仓包含 11 个安全可分发技能；插件宿主专属的 `comfy-harness` 留在插件仓。任何要求未经确认调高系统音量、打开外部页面或执行其他主机副作用的技能均不得进入发布清单。

## 安装

```bash
npx skills add full-aigc-skills/comfy-skills
npx skills add full-aigc-skills/comfy-skills --skill comfy-generate-image
```

## 维护门禁

```bash
python3 scripts/lint_skills.py
python3 scripts/trace_gate.py \
  --evaluator ../../full-stack-skills-repositories/agent-skills/skills/skill-trace-evaluation/scripts/trace_evaluate.py \
  --threshold 4.5
```

正式 `v*` Release 发布后，仓库会把不可变 tag 与 peeled commit SHA 发送给 `full-aigc-plugins/comfy-design-plugin`，由插件自动创建技能升级 PR。

## 许可证

Apache License 2.0。
