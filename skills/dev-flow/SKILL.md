---
name: dev-flow
description: 深度开发流程的编排入口与路由器。判断当前在流程哪个阶段（init→requirement→design→implement→review）、上游产物是否就绪，并引导调用对应的 skill。当用户说出一句需求却不知道该用哪个 skill、或想确认「下一步做什么」「流程走到哪了」时使用。即使用户没明确说要用流程，只要提到「开发一个功能/做需求/写方案/实现/审查代码」且仓库已有 develop/ 目录，都应优先用本 skill 定位阶段，避免跳步。
---

# Dev Flow — 流程编排入口

不直接产出代码或文档，而是**判断阶段 + 校验上游 + 路由**到对应的 dev-* skill。是整套深度开发流程的「调度器」，防止跳步、防止缺上游就开工。

## 何时使用

- 用户说出一句开发需求，但没指明用哪个 skill
- 用户问「下一步该做什么」「流程走到哪了」
- 仓库已有 `develop/` 目录，进入新一轮开发
- 想确认某个环节的前置条件是否满足

## 流程链路

```
dev-init → dev-requirement → dev-design → dev-implement → dev-review
(初始化)   (需求分析)          (方案设计)   (任务+TDD+实现)  (代码review)
```

## 执行步骤

1. **探查现状**：检查仓库根是否有 `develop/project-context.md`，以及 `develop/features/{feature}/` 下各环节产物是否已存在。
2. **判断阶段**：按下表定位用户当前处在哪个环节。
3. **校验上游就绪**：确认该环节的上游产物存在；缺失则**停下，引导用户先跑上游 skill**，不要凭空开工。
4. **路由**：明确告诉用户当前阶段、上游是否就绪、应调用哪个 skill，并把该 skill 的入参（至少 `feature`）准备好。

## 阶段判定表

| 当前要做 | 调用 skill | 必备上游（须存在） | 产物 |
|---|---|---|---|
| 仓库无 develop/ 或无 project-context.md | dev-init | 无 | project-context.md、目录骨架、CLAUDE.md 引用 |
| 有想法要敲定需求 | dev-requirement | develop/project-context.md | {feature}-requirement.md |
| 需求已定要做技术方案 | dev-design | {feature}-requirement.md | {feature}-design.md、ADR |
| 方案已定要落地 | dev-implement | {feature}-design.md（+requirement.md） | {feature}-implementation-plan.md → 代码 → 测试报告/实施报告 |
| 实现完成要审查 | dev-review | {feature}-design.md + src/tests + 报告 | {feature}-review.md |

> 判定依据：缺哪个产物，就说明上一步没做。先补上一步。

## 上游缺失时的处理（重要）

不要在上游缺失时硬做当前环节。例如：
- 用户要做方案设计，但没有 requirement.md → 提示「请先用 `/dev-requirement feature={name}` 产出需求规格」
- 用户要实现，但没有 design.md → 提示「请先用 `/dev-design feature={name}` 产出技术方案」
- 用户要做 review，但实现还没完成 → 提示「请先用 `/dev-implement feature={name}` 完成实现与测试报告」

判定产物是否存在可调用 `dev-review/scripts/validate.py`（若已实现）做程序化校验，也可直接查文件。

## 入参

可选传入 `feature`（已知要做的功能名）以加速定位。未传则通过探查 + 询问确定。

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| feature | 否 | 探查/询问 | 当前要做的 feature 名，用于定位产物路径 |

## 上下文卫生

dev-flow 本身是轻量调度，不持有大上下文。路由到具体 skill 后，由该 skill 在自己的 session 内工作。跨 session 接力靠 `develop/project-context.md` 与各 feature 产物文件。

## 参考

- 各 dev-* skill 的 SKILL.md（含各自入参与上下游声明）
- `../dev-review/scripts/validate.py` — 程序化校验产物存在性与命名规范（若已实现）
