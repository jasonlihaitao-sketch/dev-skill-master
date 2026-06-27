---
name: dev-implement
description: 任务设计+TDD+实现的合一闭环。读取技术方案，先产出代码级实施方案（精确到文件/签名/测试用例），阐述后询问是否执行，确认才按严格红绿 TDD 落地（后端无例外）。深度开发流程第四步。当用户说「开始实现/写代码/落地这个功能/把方案做出来」，或方案已定要进入编码时使用——即使用户没提 TDD，只要要在已有方案基础上写代码，都应使用本 skill 走代码级方案+红绿测试，而非直接裸写。
---

# Dev Implement — 任务设计 + TDD + 实现

两阶段：**先产出代码级实施方案 → 阐述后询问是否执行 → 确认才 TDD 落地**。
一个 feature 一个 session 内完成。

## 何时使用

- `{feature}-design.md` 已完成（dev-design 产出）
- 需要把方案落地为通过测试的代码

## 上下游依赖

本 skill 是流程链 `init → requirement → design → implement → review` 的第四环。

**读取（上游产物）**：
- `develop/features/{feature}/{feature}-design.md` — 接口设计(第4章)/数据设计(第5章)/类设计(第6章)，据此拆任务（dev-design 产出）
- `develop/features/{feature}/{feature}-requirement.md` — 第 4 章验收标准，据此写任务验收点与失败测试（dev-requirement 产出）
- `develop/project-context.md` — 编码规范(第5章)/架构(第4章)/文件结构(第3章)，据此约束实现（dev-init 产出）

**产出（下游输入）**：
- `develop/features/{feature}/{feature}-implementation-plan.md` — **代码级实施方案**（方案阶段产物），供用户确认与 dev-review 核对符合度
- `develop/features/{feature}/tasks/{feature}-task-NN-{slug}.md` — 逐任务执行追踪（执行阶段产出），供 dev-review 追溯验收点覆盖
- `src/`、`tests/` — 通过测试的实现代码（执行阶段产出），供 dev-review 审查
- `develop/features/{feature}/{feature}-test-report.md` — **测试报告**（执行完成后产出），交付依据，供 dev-review 核对覆盖与 AI 决策差异
- `develop/features/{feature}/{feature}-implementation-report.md` — **实施报告**（执行完成后产出），交付依据，供 dev-review 核对符合度与 AI 决策差异

**下游 skill 如何消费本产物**：
- `dev-review`：读实施方案+实施报告核对代码符合度；读 tasks+测试报告核对测试覆盖；读两份报告的「AI 决策差异」章节审查执行期偏离；读 src/tests 审查质量与安全

## 入参

通过 args 传入。`feature` 必填，其余可选覆盖（传了用传的，不传按命名规范推导）。

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| feature | 是 | — | feature 名，推导产物与上游路径 |
| design | 否 | develop/features/{feature}/{feature}-design.md | 技术方案路径（上游，拆任务依据） |
| requirement | 否 | develop/features/{feature}/{feature}-requirement.md | 需求规格路径（上游，验收标准） |
| context | 否 | develop/project-context.md | 全局上下文路径（上游，编码规范/架构） |

**路径推导规则**（未传覆盖时按此推导）：
- 全局上下文：`develop/project-context.md`
- 需求（上游）：`develop/features/{feature}/{feature}-requirement.md`
- 方案（上游）：`develop/features/{feature}/{feature}-design.md`
- 实施方案产物：`develop/features/{feature}/{feature}-implementation-plan.md`
- 任务追踪产物：`develop/features/{feature}/tasks/{feature}-task-NN-{slug}.md`
- 测试报告产物：`develop/features/{feature}/{feature}-test-report.md`
- 实施报告产物：`develop/features/{feature}/{feature}-implementation-report.md`
- 代码产物：仓库根 `src/`、`tests/`（按 project-context 第 3 章文件结构）

传入的覆盖参数优先于推导值。

## 两阶段流程

### 阶段 0：校验上游就绪

确认 `{feature}-design.md`、`{feature}-requirement.md`、`develop/project-context.md` 都存在。任一缺失则停下并引导到上游 skill：缺 design → `/dev-design`，缺 requirement → `/dev-requirement`，缺 project-context → `/dev-init`。没有技术方案就实现，会让任务拆解与 TDD 测试失去依据，代码很可能偏离需求。

### 阶段一：产出代码级实施方案

```
读 design + requirement + project-context
  → 拆任务（任务清单 + 依赖 + 执行顺序）
  → 逐任务填到代码级（涉及文件/函数签名/伪代码/数据结构/测试用例/TDD红绿步骤）
  → 写 {feature}-implementation-plan.md（用 references/实施方案模板.md）
  → 向用户阐述方案要点
  → 一次性询问：是否执行？
```

实施方案必须精确到代码级，严格遵循红绿 TDD（references/TDD纪律.md）：
- **后端代码：严格红绿，无例外**
- **前端代码：尽量红绿，UI 视图层可酌情**（须在方案中注明「前端 UI，TDD 酌情」并写明替代验证方式）

### 阶段二：执行（确认后）

用户确认「执行」后，按实施方案第 2.2 执行顺序逐任务走 TDD 闭环：

```
对每个任务：
  建 tasks/{feature}-task-NN.md（追踪状态）
  → Red：写失败测试（据方案测试用例）→ 运行确认红
  → Green：写最小实现（据方案代码级设计）→ 运行确认绿
  → Refactor：重构（测试不变）→ 运行确认仍绿
  → 实施方案 2.1 任务清单该任务状态更新为「已完成」（进行中时标「进行中」）
  → task 文件记录 Red/Green/Refactor 证据
→ 全部任务完成 → 产出测试报告 + 实施报告 → 交付
```

### 阶段三：交付报告（执行完成后）

全部任务完成后，产出两份报告，作为交付依据：

- **测试报告** `{feature}-test-report.md`（references/测试报告模板.md）：测试结果总览、验收点覆盖矩阵、用例清单、覆盖率、TDD 执行情况、未覆盖/已知问题。
- **实施报告** `{feature}-implementation-report.md`（references/实施报告模板.md）：实施总览、完成任务清单、代码变更、与方案符合度、遗留问题、验证结果。

**AI 决策差异披露（两份报告必填章节）**：执行期间 AI 若对测试或实现做出与原实施方案不同的决断（改签名、增删文件、调整逻辑、拆分任务、改变测试策略等），必须在对应报告的「AI 决策差异」章节逐条记录——决策点、原方案、AI 实际做法、原因、影响，并标注需回写的上游文档。无偏离则写「无」。透明披露执行期偏离，供 dev-review 与用户审查。

## TDD 严格度

全程强制 Red→Green→Refactor，硬检查点见 references/TDD纪律.md：
1. 无失败测试不许写实现
2. 必须实际运行测试确认红
3. Green 后只许重构，不许改测试逻辑
4. 一个任务的红绿循环不混入下一个任务

后端无例外；前端 UI 视图层难测可酌情，但须注明并给替代验证。

## 执行粒度

一 feature 一 session：方案与执行在同一会话。任务过多接近 smart zone 时，用 handoff 切新 session 继续（每个新 session 重读 design + 实施方案 + 未完成任务）。

## 命名规范

- 全部小写，带 `{feature}-` 前缀
- 任务编号两位起：`{feature}-task-01-{slug}.md`
- slug 有意义（如 `login-flow`，非 `t1`）

## 参考

- `references/实施方案模板.md` — 代码级实施方案模板（方案阶段核心产物，含带状态的任务清单）
- `references/任务模板.md` — 逐任务执行追踪模板（执行阶段）
- `references/TDD纪律.md` — TDD 硬检查点规则 + 前后端适用度
- `references/测试报告模板.md` — 执行完成后的测试报告模板（含 AI 决策差异）
- `references/实施报告模板.md` — 执行完成后的实施报告模板（含 AI 决策差异）
