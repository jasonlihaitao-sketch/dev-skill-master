---
name: dev-review
description: 代码 review 闸门。读取方案、任务、实现代码与测试，按四维度（需求与方案符合度/测试覆盖与质量/代码质量与规范/安全与性能）审查，产出带修复优先级的结构化发现清单，只报告不修复。深度开发流程最后一步。当实现完成、要交付前做质量审查时使用——即使用户只说「看看这代码写得怎么样」「检查一下质量」「能上线吗」，只要是审查已完成的实现，都应走本 skill 的四维度 + 优先级，而非泛泛点评。
---

# Dev Review — 代码 review

实现之后的闸门。只报告不修复，修复与否由人决定。

## 何时使用

- `/dev-implement` 已完成一个 feature 的任务与代码
- 需要在交付前做质量审查

## 上下游依赖

本 skill 是流程链 `init → requirement → design → implement → review` 的最后一环。

**读取（上游产物）**：
- `develop/project-context.md` — 编码规范(第5章)/架构(第4章)/非功能约束(第7章)，据此判断符合度（dev-init 产出）
- `develop/features/{feature}/{feature}-design.md` — 接口/数据/类设计，核对实现是否符合方案（dev-design 产出）
- `develop/features/{feature}/{feature}-requirement.md` — 第 4 章验收标准，核对验收点覆盖（dev-requirement 产出）
- `develop/features/{feature}/tasks/` — 任务验收点，核对测试覆盖（dev-implement 产出）
- `src/`、`tests/` — 实现代码与测试，审查对象（dev-implement 产出）

**产出**：
- `develop/features/{feature}/{feature}-review.md` — 结构化发现清单，含结论 pass/需修复

## 入参

通过 args 传入。`feature` 必填，其余可选覆盖（传了用传的，不传按命名规范推导）。

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| feature | 是 | — | feature 名，推导产物与上游路径 |
| design | 否 | develop/features/{feature}/{feature}-design.md | 技术方案路径（上游，核对符合度） |
| requirement | 否 | develop/features/{feature}/{feature}-requirement.md | 需求规格路径（上游，核对验收点） |
| context | 否 | develop/project-context.md | 全局上下文路径（上游，规范/约束） |

**路径推导规则**（未传覆盖时按此推导）：
- 全局上下文：`develop/project-context.md`
- 需求（上游）：`develop/features/{feature}/{feature}-requirement.md`
- 方案（上游）：`develop/features/{feature}/{feature}-design.md`
- 任务（上游）：`develop/features/{feature}/tasks/`
- 代码（审查对象）：仓库根 `src/`、`tests/`
- review 产物：`develop/features/{feature}/{feature}-review.md`

传入的覆盖参数优先于推导值。

## review 四维度（全必查，每维对应报告一章）

1. **需求与方案符合度** — 实现是否符合 design 的接口/数据/类设计；是否漏掉 requirement 验收点
2. **测试覆盖与质量** — 测试是否覆盖所有验收点与边界；TDD 纪律是否遵守；有无漏测
3. **代码质量与规范** — 命名/结构/复杂度/重复/分层，对照 project-context 第 5 章
4. **安全与性能** — 安全漏洞/性能问题/错误处理/资源泄漏

检查清单见 references/review检查清单.md。

## 报告格式

`{feature}-review.md`，结构化发现清单（见 references/review报告模板.md）：
- 按四维度分章列发现，每条：`- [blocker|major|minor|nit] 位置 问题 建议`
- **修复优先级**章节：按严重度+依赖排出 P0/P1/P2/P3 顺序与推荐修复批次，供人决策
- 结尾结论：pass / 需修复

## 处置

**只报告不修复**。发现的问题列出供人决策，不自动改代码、不强制回到 implement。若用户要求修复，再回到 `/dev-implement`。

## 执行步骤

0. **校验上游就绪**：确认 `{feature}-design.md`、`src/` 实现代码与测试已存在（dev-implement 已完成）。若实现还没做，提示用户「请先用 `/dev-implement feature={name}` 完成实现与测试报告」，没有代码可审的 review 没有意义。可调用 `scripts/validate.py feature={name}` 程序化校验产物齐全与命名规范。
1. **读上游**：project-context + design + requirement + tasks + 实现代码与测试。
2. **按四维度审查**：对照 references/review检查清单.md 逐项检查。
3. **写报告**：用 references/review报告模板.md，按维度分章列发现，每条标严重度。
4. **排修复优先级**：按严重度（blocker>major>minor>nit）+ 依赖关系 + 影响面，排出 P0/P1/P2/P3 顺序与推荐修复批次。
5. **给结论**：有 P0 blocker → 需修复；仅 P1 及以下 → pass（附修复建议）。
6. **不修复**：列出问题与优先级即止。如用户要修，引导回 dev-implement 按优先级处理。

## 命名规范

- 全部小写，带 `{feature}-` 前缀：`{feature}-review.md`
- 文件名有意义、不简单

## 参考

- `references/review报告模板.md` — 结构化发现清单报告模板
- `references/review检查清单.md` — 四维度检查清单
- `scripts/validate.py` — 程序化校验产物存在性、命名规范、上下游齐全、验收点覆盖矩阵。用法：`python scripts/validate.py --root <仓库根> --feature <name>`，退出码 0 通过/1 有失败
