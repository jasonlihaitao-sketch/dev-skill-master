# dev-skill-master

一套「深度开发流程」自定义 Claude Skill 合集，作者自行开发与维护。

流程把一个功能从想法到交付拆成 5 个阶段，每阶段一个 skill，由 `dev-flow` 路由，防止跳步、防止缺上游就开工。

## 流程链路

```
dev-init → dev-requirement → dev-design → dev-implement → dev-review
 项目初始化   需求分析(访谈)    方案设计      任务+TDD+实现   代码 review
```

每个产物是下一阶段的上游；缺产物就说明上一步没做，先补上一步。

## 目录结构

```
dev-skill-master/
├── README.md
├── LICENSE                  MIT
├── .gitignore
├── install.sh               仓库 → ~/.claude/skills/   (让 Claude 读到仓库最新版)
├── capture.sh               ~/.claude/skills/ → 仓库   (本地改动抓回仓库)
└── skills/
    ├── dev-init/            项目初始化：develop/ 骨架 + project-context.md
    ├── dev-flow/            流程编排入口与路由器
    ├── dev-requirement/     需求分析：混合访谈 + Given-When-Then 验收标准
    ├── dev-design/          方案设计：8 章节技术方案 + ADR
    ├── dev-implement/       任务设计 + 红绿 TDD + 实现
    └── dev-review/          代码 review 闸门：四维度 + 修复优先级
```

各 skill 的 `SKILL.md` 含完整入参、上下游声明与执行步骤；`references/`、`scripts/` 为其模板与校验脚本。

> 注：`devex-review` 不在本仓库内——它是 gstack 插件的 skill，非本合集所有，也不在 `dev-flow` 链路中。

## 真相源与同步

**仓库是真相源，永远最新。** 本地 `~/.claude/skills/dev-*` 是被覆盖的测试副本，Claude 实际读取它来运行/测试。

两个同步脚本，均为 **diff 冲突即停、报错** 语义——绝不无声覆盖另一边的新改动：

| 脚本 | 方向 | 何时用 |
|---|---|---|
| `install.sh` | 仓库 → `~/.claude/skills/` | 在仓库改完(或异地 `git pull` 后)，让 Claude 用上最新版去测试 |
| `capture.sh` | `~/.claude/skills/` → 仓库 | 你直接在本地改了 skill、测好后把改动抓回仓库 |

脚本若检测到目标侧存在「源没有的新改动」(会被覆盖丢失)，会停下并列出冲突文件，由你手动处理后再跑。

## 用法

```bash
# 仓库 → 本地(Claude 读取最新版)
./install.sh

# 本地 → 仓库(抓回改动后，记得 git commit/push)
./capture.sh
git add -A && git commit -m "..." && git push
```

## 安装到新机器

```bash
git clone <repo-url> dev-skill-master
cd dev-skill-master
./install.sh
```

## 许可证

MIT，见 [LICENSE](./LICENSE)。
