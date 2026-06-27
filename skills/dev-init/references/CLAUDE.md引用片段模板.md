# CLAUDE.md 引用片段模板

> dev-init 在仓库根 `CLAUDE.md` 中写入此片段，使 `develop/project-context.md`
> 被加载进 Claude 上下文并要求遵循。
> 已有 CLAUDE.md 则**增量追加**到文件中，不覆盖既有内容。
> 本文件本身不是产物，只是片段蓝本。

## 写入 CLAUDE.md 的片段

```markdown
## 项目上下文（深度开发流程）

本项目使用深度开发流程（init→requirement→design→implement→review）。
所有产物在 `develop/` 目录下，流程产物与代码分离。

**必须先读并遵循 `develop/project-context.md`**：
该文件是项目的单一事实来源（技术栈、架构、文件结构、编码规范、术语、
非功能约束、边界）。每次会话开始、以及进行任何需求/设计/实现/review 前，
先读该文件并按其规范执行。若产生新的全局约定或术语，回写该文件。

### 流程与产物路径

| 环节 | 产物 | 路径 |
|---|---|---|
| init | 项目上下文 | develop/project-context.md |
| requirement | 需求规格 | develop/features/{feature}/{feature}-requirement.md |
| design | 技术方案 | develop/features/{feature}/{feature}-design.md |
| implement | 任务 + 代码 | develop/features/{feature}/tasks/ + src/ tests/ |
| review | review 报告 | develop/features/{feature}/{feature}-review.md |
| 决策记录 | ADR | develop/adr/（全局）、develop/features/{f}/adr/（功能级） |

### 命名规范

- 全部小写；feature 级文件带 `{feature}-` 前缀
- 文件名有意义、不简单（如 `user-auth-requirement.md`）

### 上下游依赖

需求(requirement)→方案(design)→实现(implement)→评审(review)。
每个环节的 skill 在其 SKILL.md 中声明读取的上游产物路径与产出的下游路径。
```

## 注意

- 片段中的「必须先读并遵循 `develop/project-context.md`」是核心——没有这句，文件不会被自动遵循。
- 若用户已有 CLAUDE.md 内容，追加在末尾或合适章节，保留原有指令。
- 路径用相对仓库根的 `develop/...` 形式。
