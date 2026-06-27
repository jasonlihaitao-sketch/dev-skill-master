---
name: dev-requirement
description: 需求分析。混合式访谈收敛用户想法，产出需求规格（验收标准强制 Given-When-Then），是下游方案设计与 TDD 测试的依据。深度开发流程第二步。当用户提出功能想法、要敲定需求时使用——即使用户只是随口说「我想做个登录」或「加个 XX 功能」，只要还没形成可测的验收标准，都应先用本 skill 把需求敲定，而非直接跳到设计或实现。
---

# Dev Requirement — 需求分析

需求源头质量闸。产物是方案设计和 TDD 验收测试的依据。

## 何时使用

- 用户提出一个功能想法，需要把需求敲定到可测、可设计
- `/dev-init` 已完成（develop/ 与 project-context.md 已存在）

## 上下游依赖

本 skill 是流程链 `init → requirement → design → implement → review` 的第二环。

**读取（上游产物）**：
- `develop/project-context.md` — 校验技术栈/约束/术语一致性（dev-init 产出）

**产出（下游输入）**：
- `develop/features/{feature}/{feature}-requirement.md` — 供 dev-design 读取做技术决策；其第 4 章「验收标准」供 dev-implement 翻译为 TDD 失败测试

**下游 skill 如何消费本产物**：
- `dev-design`：读 `{feature}-requirement.md` 全文，据此产出 `{feature}-design.md`
- `dev-implement`：读第 4 章验收标准，逐条翻译为任务验收点（task 模板第 3 字段）与失败测试

## 入参

通过 args 传入。`feature` 必填，其余可选覆盖（传了用传的，不传按命名规范推导）。

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| feature | 是 | — | feature 名，推导产物与上游路径 |
| context | 否 | develop/project-context.md | 全局上下文路径（上游，校验技术栈/约束） |

**路径推导规则**（未传覆盖时按此推导）：
- 全局上下文：`develop/project-context.md`
- 需求产物：`develop/features/{feature}/{feature}-requirement.md`

传入的覆盖参数优先于推导值。

## 产出文件

`develop/features/{feature}/{feature}-requirement.md`（7 章节，见 references/需求模板.md）：
1. 背景与目标 / 2. 用户故事 / 3. 功能范围（做/不做） / 4. 验收标准（**强制 Given-When-Then**） / 5. 非功能需求 / 6. 边界与约束 / 7. 待澄清问题

## 执行步骤

0. **校验上游就绪**：确认 `develop/project-context.md` 存在（dev-init 产物）。缺失则停下，提示用户「请先用 `/dev-init` 完成项目初始化」，不要在无项目上下文时凭空开工——没有它，需求的非功能约束与术语无据可依。
1. **读上下文**：读 `develop/project-context.md`，确认技术栈、非功能约束、术语。
2. **确定 feature 名**：向用户确认一个 kebab-case 的 feature 名（如 `user-auth`）。
3. **建目录**：创建 `develop/features/{feature}/`。
4. **混合式访谈**：
   - 先让用户自由描述想法
   - 用 references/需求模板.md 逐章识别缺口
   - 针对性追问三处关键缺口：**验收标准**（必须可测）、**边界**（不做什么）、**非功能需求**
   - 其余字段填表补齐
5. **强制验收标准**：第 4 章每条必须 Given-When-Then，不可用模糊自然语言。无法写成 GWT 的，说明需求未清晰，回到追问。
6. **写文件**：按模板填 `develop/features/{feature}/{feature}-requirement.md`。
7. **HTML 预览**：用 `doc-to-html` 把刚写的 `{feature}-requirement.md` 转成同名 `.html` 并在浏览器打开，供用户审阅效果。调用：`node ~/.claude/skills/doc-to-html/scripts/render.mjs develop/features/{feature}/{feature}-requirement.md`。
8. **回写上下文**：若访谈中发现新的全局术语/约束，回写 `develop/project-context.md` 第 6/7 章。

## 命名规范

- 全部小写
- feature 级文件带 `{feature}-` 前缀
- 文件名有意义、不简单（`user-auth-requirement.md`，非 `req.md`）

## 参考

- `references/需求模板.md` — 7 章节需求模板
