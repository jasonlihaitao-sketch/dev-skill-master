---
name: dev-init
description: 项目初始化。建立 develop/ 流程工作区骨架、生成 project-context.md（8章节结构化字段表）、在 CLAUDE.md 中引用使其进入 Claude 上下文、落地目录约定与工程配置。深度开发流程起点。当用户在新/已有仓库首次启动深度开发流程、或要建立项目上下文载体时使用——即使用户只是说「开始一个新项目」「给这个仓库加上开发流程」，只要仓库还没有 develop/project-context.md，都应先用本 skill 初始化。
---

# Dev Init — 项目初始化

深度开发流程的起点。建立全流程共享的目录骨架与长期上下文载体 `project-context.md`。

## 何时使用

- 新仓库或已有仓库首次接入深度开发流程
- 需要建立后续 skill（requirement/design/implement/review）共同读取的项目上下文

## 上下游依赖

本 skill 是流程链 `init → requirement → design → implement → review` 的第一环，无上游。

**产出（下游输入）**：
- `develop/` 目录骨架 — 全流程产物的存放结构
- `develop/project-context.md` — 全局上下文，供所有下游 skill 启动时读取
- 仓库根 `CLAUDE.md` 中的引用 — 使 project-context.md 进入 Claude 上下文
- 代码骨架（仓库根 `src/`）+ 工程配置 — 供 dev-implement 落地代码、dev-review 检查质量

**下游 skill 如何消费本产物**：
- `dev-requirement` / `dev-design` / `dev-implement` / `dev-review`：启动时先读 `develop/project-context.md`

## 入参

init 是流程起点，无上游产物。入参可选：

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| project | 否 | 交互确认 | 项目名，写入 project-context.md 第 1 章标题 |
| root | 否 | 当前工作目录 | 仓库根路径，develop/ 建在其下 |

其余信息（技术栈、架构、规范等）通过交互访谈填充。无必填入参。

## 产出

1. `develop/` 目录骨架（见 references/目录布局.md）
2. `develop/project-context.md`（8 章节，见 references/项目上下文模板.md）
3. **仓库根 `CLAUDE.md` 中引用 `develop/project-context.md`**（见 references/CLAUDE.md引用片段模板.md）——这是让 project-context.md 真正进入 Claude 上下文的关键。project-context.md 本身放在 develop/ 下不会自动加载，必须在 CLAUDE.md 里显式指向并要求遵循。
4. 代码骨架（从 references/代码骨架模板.md 拷到仓库根 `src/`）
5. 工程配置（从 references/工程配置模板.md 落地 lint/format/git hooks/CI）

## 执行步骤

1. **读项目现状**：检查仓库根是否已有 `src/` `tests/` `package.json` 等，判断技术栈。本 skill 技术栈通用，不预设具体框架。
2. **确认目录布局**：向用户说明 `develop/` 只放流程产物，代码留仓库根。按 references/目录布局.md 创建骨架。
3. **生成 project-context.md**：用 references/项目上下文模板.md，逐章访谈或填空。8 章必须齐全，不可留空章（无内容写「待定」并列入待澄清）。
4. **写 CLAUDE.md 引用**（关键）：在仓库根 `CLAUDE.md` 中加入对 `develop/project-context.md` 的引用与「必须遵循」说明，使该文件被加载进 Claude 上下文。已有 CLAUDE.md 则增量追加（不覆盖既有内容）。片段见 references/CLAUDE.md引用片段模板.md。
5. **落地代码骨架**：把通用骨架拷到仓库根，不进 `develop/`。
6. **落地工程配置**：lint/format/CI，保证后续 TDD 与 review 有自动化质量基线。
7. **建 ADR 目录**：创建 `develop/adr/`（全局）与 `develop/features/`。ADR 格式由 dev-design skill 负责（见其 references/ADR模板.md）。

## 命名规范（全流程统一，必须遵守）

- 全部小写
- feature 级文件带 `{feature}-` 前缀（如 `user-auth-requirement.md`）
- 全局文件（project-context / 全局 ADR）不带前缀
- 文件名有意义、不简单（禁止 `req.md` `ctx.md` 这类）

## 上下文卫生

`project-context.md` 是全流程只读 + 增量更新的载体。后续每个 skill 启动时先读它。init 完成后，它的维护权归各 skill：requirement/design/implement 若产生新的全局约定或术语，回写本文件。

## 参考

- `references/目录布局.md` — 目录布局
- `references/项目上下文模板.md` — 8 章节上下文模板
- `references/CLAUDE.md引用片段模板.md` — CLAUDE.md 引用片段模板（让 context 进上下文）
- `references/代码骨架模板.md` — 通用代码骨架
- `references/工程配置模板.md` — 工程配置模板
