# {feature} — 代码 review 报告

> 产物路径：`develop/features/{feature}/{feature}-review.md`
> 上游：project-context.md、{feature}-design.md、{feature}-requirement.md、tasks/、src/、tests/
> 只报告不修复。blocker 决定能否收工。

- **审查日期**：YYYY-MM-DD
- **审查范围**：{feature} 的实现代码与测试
- **结论**：pass / 需修复

## 1. 需求与方案符合度

> 核对实现是否符合 design 第 4/5/6 章，是否漏掉 requirement 第 4 章验收点。

- `[blocker|major|minor|nit]` {文件:行} {问题} → {建议}

示例：
- `[major] src/auth/login.ts:12` 接口签名与 design 第 4 章 `POST /login` 不符（缺 expiresIn 字段）→ 补齐返回字段
- `[blocker]` 未实现 requirement AC3 的限流兜底 → 补实现

## 2. 测试覆盖与质量

> 核对 task 验收点是否都有测试；边界/异常是否覆盖；TDD 纪律。

- `[blocker]` requirement AC2 无对应测试 → 补测试
- `[minor] tests/auth/login.test.ts` 未覆盖密码错误分支 → 补边界用例
- `[nit]` 部分测试先实现后补，非 TDD → 下次遵守 Red 先行

## 3. 代码质量与规范

> 对照 project-context 第 5 章规范。命名/结构/复杂度/重复/分层。

- `[minor] src/auth/login.ts:45` 函数圈复杂度过高 → 拆分
- `[nit]` 命名 `d` 不达意 → 改为 `duration`
- `[major]` 业务模块反向依赖 API 层，违反分层 → 调整依赖方向

## 4. 安全与性能

> 安全漏洞/性能/错误处理/资源泄漏。对照 project-context 第 7 章非功能约束。

- `[blocker] src/auth/login.ts` 密码明文日志 → 移除日志
- `[major]` 未对输入做校验，存在注入风险 → 加校验
- `[minor]` 循环内重复查库 → 批量查询或缓存

## 5. 修复优先级

> 只报告不修复，但按优先级排出修复顺序，供人决策后续是否回到 dev-implement 修复。
> 排序依据：严重度（blocker > major > minor > nit）+ 依赖关系（被依赖的先修）+ 影响面。

### P0 必须先修（blocker，阻塞交付）

| 序号 | 位置 | 问题 | 建议修复 | 依赖 |
|---|---|---|---|---|
| 1 | src/auth/login.ts | 密码明文日志 | 移除日志 | 无 |

### P1 应修（major，影响正确性/可维护性）

| 序号 | 位置 | 问题 | 建议修复 | 依赖 |
|---|---|---|---|---|
| 2 | src/auth/login.ts | 接口签名不符 | 补齐 expiresIn | 依赖 #1（先修日志同文件） |

### P2 建议修（minor，质量改进）

| 序号 | 位置 | 问题 | 建议修复 | 依赖 |
|---|---|---|---|---|

### P3 可选（nit，风格层面）

| 序号 | 位置 | 问题 | 建议修复 | 依赖 |
|---|---|---|---|---|

### 推荐修复批次

> 按依赖分组，可一次性回到 dev-implement 处理的批次。

- **批次1**（P0+P1 安全与符合度）：#1 #2 — 建议立即修
- **批次2**（P2 质量改进）：随下次迭代
- **批次3**（P3 风格）：有空处理

## 6. 结论

- **Blocker 数**：{N}（P0）
- **Major 数**：{N}（P1）
- **结论**：{pass | 需修复}
  - 有 P0 blocker → **需修复**：先修 P0 批次，建议回到 `/dev-implement` 按修复优先级处理
  - 仅 P1 及以下 → **pass**（附修复建议，由人决定是否立即处理）
  - 全清 → **pass**
- **说明**：（一句话总结，如「2 项 P0 安全问题必须先修，修复后可交付」）
