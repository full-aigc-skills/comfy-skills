#!/usr/bin/env python3
"""Generate deterministic quality resources from repository skill profiles."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER_START = "<!-- QUALITY_CONTRACT_START -->"
MARKER_END = "<!-- QUALITY_CONTRACT_END -->"


def render_contract(name: str, profile: dict[str, str]) -> str:
    return f"""{MARKER_START}
## 什么时候使用

✅ 适用：

1. 用户明确要{profile['purpose']}。
2. 已提供或可安全取得必要上下文，需要得到可验证的 `{profile['artifact']}`。
3. 需要按最小权限、可回滚方式执行，并保留审计证据。

⚠️ 先澄清：

1. 目标环境、授权边界或成功标准缺失时，先给出只读假设方案并列出缺失项。
2. 涉及生产环境变更时，先确认备份、维护窗口和回滚路径。
3. 输入可能含敏感信息时，只引用字段名和脱敏片段，不复制完整凭据。

❌ 不该用：

1. {profile['not_for']}。
2. 用户只要概念解释且没有执行或交付需求。
3. 需要绕过鉴权、证书校验、人工确认或其他安全控制的请求。

## Workflow

Step 1：确认目标、环境、授权范围和不可变约束；信息不足时先产出带假设的只读版本。

Step 2：盘点现状与依赖，只读取必要数据，不记录令牌、密码、Cookie 或完整个人数据。

Step 3：选择最小影响路径，将高风险动作、外部网络调用和可逆步骤明确标注。

Step 4：生成或执行 `{profile['artifact']}`，每一步都绑定输入、预期输出与失败条件。

Step 5：校验结构、事实来源和目标状态；禁止根据缺失证据编造成功结论。

Step 6：失败时停止扩大影响，输出已完成步骤、失败证据、恢复点和下一次安全重试条件。

Step 7：交付摘要、验证证据、剩余风险与后续动作；生产变更必须说明回滚是否已验证。

## Rules

- 默认只读；写操作、高危操作和付费调用必须获得与该动作匹配的明确授权。
- 本技能不收集、不存储、不上传用户凭据；日志和报告不得包含完整 token、密码或密钥。
- 不关闭 TLS 校验，不执行来源不明脚本，不使用管道下载后直接执行。
- 只把真实执行结果写成“已完成”；计划、示例和推断必须显式标注。
- 优先幂等操作；无法幂等时先提供预演、备份和回滚点。

## Validation checklist

- [ ] 目标、环境与授权范围均已写明。
- [ ] `{profile['success']}` 已由可复现证据验证。
- [ ] 敏感数据已脱敏，输出中没有完整凭据。
- [ ] 失败与超时路径已覆盖，未出现无限重试。
- [ ] 变更类任务具有备份或回滚说明。
- [ ] 最终结论区分事实、推断和未验证项。

## Gotchas

1. **授权不等于可达**：有权限但网络、证书或白名单不满足时，仍应停止并报告连接证据。
2. **成功码不等于业务成功**：必须检查 `{profile['success']}`，不能只看命令退出码或 HTTP 200。
3. **重试不等于恢复**：对鉴权失败、参数错误和安全拒绝不得盲目重试。
4. **示例不等于现状**：模板值与占位符不能写成真实环境数据。
5. **输出不等于交付**：还需完成结构校验、风险说明和可重复验证。
6. **跨环境不可照搬**：操作系统、版本、区域和宿主能力不同时必须重新确认参数。

## 渐进式资料

- 做路径选择前读取 `references/decisions/decision-guide.md`。
- 遇到异常、超时或部分成功时读取 `references/operations/failure-matrix.md`。
- 完成交付前读取 `references/operations/validation-checklist.md`。
- 需要可复制输入时，按顺序参考 `examples/basic.md`、`examples/failure.md`、`examples/advanced.md`。
{MARKER_END}"""


def rendered_files(name: str, profile: dict[str, str]) -> dict[Path, str]:
    base = ROOT / "skills" / name
    return {
        base / "references" / "decisions" / "decision-guide.md": f"""# {name} 决策指南

## 目标

本技能用于{profile['purpose']}，主要交付物是 `{profile['artifact']}`。

## 决策树

1. 若授权范围不清晰：只输出只读检查方案和待确认项。
2. 若输入不完整但可安全假设：明确假设，先产出可审查草案。
3. 若存在生产写操作：先验证备份和回滚，再请求动作级确认。
4. 若需要绕过安全控制：停止，给出合规替代路径。
5. 若证据满足 `{profile['success']}`：交付结果并记录验证方式。

## 近似场景边界

- `{profile['near_miss']}` 不属于本技能的直接职责，应转交更合适的专项技能或人工流程。
- 仅做知识问答时，不应触发任何外部写操作。
- 无法取得真实环境证据时，只能交付方案或推断，不能声称运行验证通过。
""",
        base / "references" / "operations" / "failure-matrix.md": f"""# {name} 失败矩阵

| 失败类别 | 识别信号 | 是否重试 | 安全处理 |
|---|---|---:|---|
| 输入缺失 | 必填目标、范围或参数为空 | 否 | 给出带假设草案并列出缺失项 |
| 鉴权失败 | 401/403、凭据缺失或权限不足 | 否 | 脱敏报告，要求重新授权或轮换凭据 |
| 网络/TLS | DNS、超时、证书链失败 | 有条件 | 保留 TLS 校验，检查白名单和出口网络 |
| 参数/版本 | 400、字段不支持、版本不兼容 | 否 | 对照真实版本修正参数，禁止重复提交 |
| 服务限流 | 429、配额不足 | 有条件 | 尊重 Retry-After，限制次数并保留任务标识 |
| 部分成功 | 生成了中间产物但 `{profile['success']}` 未满足 | 否 | 保存恢复点，列出已完成与未完成项 |
| 终态失败 | Failed/Cancelled/Rejected/Error | 否 | 立即停止轮询，输出错误详情和恢复条件 |

重试必须有上限、退避和幂等依据；否则转为人工决策。
""",
        base / "references" / "operations" / "validation-checklist.md": f"""# {name} 交付验证清单

## 输入

- [ ] 目标与非目标明确。
- [ ] 环境、版本、区域与身份来源明确。
- [ ] 高风险动作具有动作级授权。

## 执行

- [ ] 所有外部调用使用可信端点与 TLS 校验。
- [ ] 日志不含完整凭据或个人数据。
- [ ] 重试次数、超时和终态处理可预测。

## 输出

- [ ] `{profile['artifact']}` 格式完整且可复查。
- [ ] `{profile['success']}` 有真实证据。
- [ ] 失败、降级、回滚与剩余风险已说明。
- [ ] 事实、推断、示例和未验证项清晰区分。
""",
        base / "examples" / "basic.md": f"""# 基础场景

## 用户输入

请{profile['basic_prompt']}。先只读检查，输出 `{profile['artifact']}`，不要修改生产配置。

## 预期行为

1. 确认目标与环境。
2. 使用最小权限收集证据。
3. 给出结构化结果、验证状态和未确认项。
""",
        base / "examples" / "failure.md": f"""# 失败恢复场景

## 用户输入

上一次{profile['failure_prompt']}。请根据已有任务标识恢复，不要重新提交可能产生副作用的请求。

## 预期行为

1. 识别失败类别和现有恢复点。
2. 对终态失败立即停止；对可恢复任务使用有限轮询。
3. 输出失败证据、已完成项、未完成项和安全重试条件。
""",
        base / "examples" / "advanced.md": f"""# 高级场景

## 用户输入

请在{profile['advanced_context']}下完成{profile['purpose']}，要求分阶段验证、敏感信息脱敏，并给出回滚路径。

## 预期行为

1. 把任务拆成可验证阶段。
2. 每阶段定义输入、输出、停止条件与回滚点。
3. 最终以 `{profile['success']}` 为验收证据，而不是仅报告“命令执行成功”。
""",
    }


def desired_skill_md(path: Path, name: str, profile: dict[str, str]) -> str:
    current = path.read_text(encoding="utf-8").rstrip()
    if current.startswith("---\n"):
        frontmatter_end = current.find("\n---", 4)
        if frontmatter_end == -1:
            raise RuntimeError(f"{name}: frontmatter is not closed")
        frontmatter = current[4:frontmatter_end]
        if "\nlicense:" not in "\n" + frontmatter:
            current = current[:frontmatter_end] + "\nlicense: Apache-2.0" + current[frontmatter_end:]
    if MARKER_START in current:
        prefix, _, rest = current.partition(MARKER_START)
        _, marker, suffix = rest.partition(MARKER_END)
        if not marker:
            raise RuntimeError(f"{name}: quality contract marker is incomplete")
        current = (prefix.rstrip() + "\n\n" + suffix.lstrip()).rstrip()
    return current + "\n\n" + render_contract(name, profile) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write generated resources")
    args = parser.parse_args()
    profiles = json.loads((ROOT / "quality-profiles.json").read_text(encoding="utf-8"))
    mismatches: list[str] = []
    for name, profile in sorted(profiles.items()):
        skill_md = ROOT / "skills" / name / "SKILL.md"
        if not skill_md.is_file():
            mismatches.append(f"{name}: missing SKILL.md")
            continue
        outputs = rendered_files(name, profile)
        outputs[skill_md] = desired_skill_md(skill_md, name, profile)
        for path, content in outputs.items():
            if path.is_file() and path.read_text(encoding="utf-8") == content:
                continue
            if args.write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            else:
                mismatches.append(str(path.relative_to(ROOT)))
    if mismatches:
        prefix = "generated" if args.write else "out of date"
        print(f"{prefix}: " + ", ".join(mismatches))
    return 0 if args.write or not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
