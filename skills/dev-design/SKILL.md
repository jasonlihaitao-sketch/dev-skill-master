---
name: dev-design
description: 方案设计。读取需求规格，产出技术方案（8章节，含功能设计[按功能拆分、标注新增或改动、流程图/时序图、类与前端交互设计]、数据与接口设计），重大决策写 ADR。深度开发流程第三步。当需求已敲定、要做技术方案时使用——即使用户说「设计一下怎么实现」「画个架构」「接口怎么定」，只要要基于已有需求做技术决策，都应先用本 skill 走完方案再实现，避免边写代码边设计。
---

# Dev Design — 方案设计

技术决策环节。产物供任务设计拆解、dev-review 核对。

## 何时使用

- `{feature}-requirement.md` 已完成（dev-requirement 产出）
- 需要把需求落到可拆解、可实现的技术方案

## 上下游依赖

本 skill 是流程链 `init → requirement → design → implement → review` 的第三环。

**读取（上游产物）**：
- `develop/features/{feature}/{feature}-requirement.md` — 需求与验收标准（dev-requirement 产出）
- `develop/project-context.md` — 技术栈/架构/约束/规范（dev-init 产出）

**产出（下游输入）**：
- `develop/features/{feature}/{feature}-design.md` — 8 章节。供 dev-implement 据此拆任务、写测试；供 dev-review 核对实现是否符合方案
- `develop/features/{feature}/adr/{feature}-adr-NN-{slug}.md` — 功能级重大决策（仅重大决策写）
- `develop/adr/adr-NN-{slug}.md` — 跨功能重大决策（如技术选型，仅重大决策写）

**下游 skill 如何消费本产物**：
- `dev-implement`：读 design 第 3 章总体设计 / 第 4 章功能设计 / 第 5 章数据与接口设计，拆为任务；任务模板第 2 字段引用 design 段落
- `dev-review`：读 design 全文，核对实现是否符合功能设计/接口/数据/类设计，验收点是否覆盖

## 入参

通过 args 传入。`feature` 必填，其余可选覆盖（传了用传的，不传按命名规范推导）。

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| feature | 是 | — | feature 名，推导产物与上游路径 |
| requirement | 否 | develop/features/{feature}/{feature}-requirement.md | 需求规格路径（上游） |
| context | 否 | develop/project-context.md | 全局上下文路径（上游） |

**路径推导规则**（未传覆盖时按此推导）：
- 全局上下文：`develop/project-context.md`
- 需求（上游）：`develop/features/{feature}/{feature}-requirement.md`
- 方案产物：`develop/features/{feature}/{feature}-design.md`
- 功能级 ADR 产物：`develop/features/{feature}/adr/{feature}-adr-NN-{slug}.md`
- 全局 ADR 产物：`develop/adr/adr-NN-{slug}.md`

传入的覆盖参数优先于推导值。

## 产出文件

### {feature}-design.md（8 章节，见 references/方案模板.md + 方案填写规范.md）
1. 方案概览 / 2. 技术选型（含被否方案及理由）/ 3. 总体设计（mermaid 架构图 + 核心数据流）/ 4. 功能设计（按功能拆分，每个功能含 (a)功能概述 (b)流程图或时序图 (c)具体功能设计，含具体类——类设计有则加无则省）/ 5. 数据设计与接口设计（数据模型+ER图、接口契约、类图）/ 6. 影响面与风险 / 7. 回滚策略 / 8. 关联 ADR

### ADR（仅重大决策，见 references/ADR模板.md）
- 功能级：`develop/features/{feature}/adr/{feature}-adr-01-{slug}.md`
- 全局级：`develop/adr/adr-01-{slug}.md`

## 执行步骤

0. **校验上游就绪**：确认 `{feature}-requirement.md` 与 `develop/project-context.md` 都存在。任一缺失则停下，提示用户「请先用 `/dev-requirement feature={name}` 产出需求规格」（或缺 project-context 则提示 `/dev-init`）。没有需求规格就做方案是无源之水——方案的验收标准、功能范围都应来自需求。
1. **读上游**：读 `{feature}-requirement.md` 全文 + `project-context.md`。
2. **按方案模板填 8 章**：参考方案填写规范.md 的每章填法与 mermaid 代码示例。
3. **按功能拆分第 4 章**：对齐 requirement 功能范围，每个功能写 (a) 功能概述 (b) 流程图或时序图 (c) 具体功能设计。其中：每个功能标注**新增或改动**类型，改动的功能必须列**改动清单**（改动对象/类型/内容/影响范围）；涉及前端的功能加**交互设计**（用 ASCII 体现界面布局与交互流程）；具体的类——类设计有则加无则省。
4. **图必填**：第 3 章总体设计架构图、第 4 章每功能的流程图/时序图、第 5 章 ER 图与类图——用 mermaid，不可用纯文字替代。
5. **接口/数据/类强制结构化**：第 5 章用接口签名/类型定义、表结构/字段定义、类图 + 职责。下游 implement 与 review 直接据此。
6. **技术选型留痕**：第 2 章列被否方案及理由。
7. **重大决策写 ADR**：选型、架构折中等重大决策开 ADR（references/ADR模板.md），并在 design 第 8 章关联。非重大决策不写 ADR，避免噪音。
8. **HTML 预览**：用 `doc-to-html` 把刚写的 `{feature}-design.md` 转成同名 `.html` 并在浏览器打开，供用户审阅效果。调用：`node ~/.claude/skills/doc-to-html/scripts/render.mjs develop/features/{feature}/{feature}-design.md`。
9. **回写上下文**：若产生新的全局架构约定/术语，回写 `project-context.md`。

## 命名规范

- 全部小写，feature 级带 `{feature}-` 前缀
- ADR 编号两位起：`adr-01-{slug}.md`
- 文件名有意义、不简单

## 参考

- `references/方案模板.md` — 8 章节方案模板（填空蓝本）
- `references/方案填写规范.md` — 每章填法 + mermaid 架构图/ER图/类图/时序图代码示例
- `references/ADR模板.md` — 决策记录模板
