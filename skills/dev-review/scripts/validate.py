#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度开发流程产物校验脚本

校验 develop/ 流程工作区的结构、上下游产物存在性、命名规范、
CLAUDE.md 引用、以及验收点↔任务覆盖矩阵。供 dev-review 与 dev-flow
做程序化前置校验，避免靠肉眼检查漏项。

用法:
    python validate.py --root <仓库根>                    # 校验项目级结构
    python validate.py --root <仓库根> --feature <name>   # 校验某 feature 全流程产物
    python validate.py --root <仓库根> --feature <name> --stage design  # 校验到某阶段为止

退出码: 0=通过(可有 WARN), 1=有 FAIL。
"""

import argparse
import os
import re
import sys
from pathlib import Path


# ---- 校验结果收集 ---------------------------------------------------------

class Report:
    def __init__(self):
        self.items = []  # (level, msg)  level in OK/WARN/FAIL

    def ok(self, msg):
        self.items.append(("OK", msg))

    def warn(self, msg):
        self.items.append(("WARN", msg))

    def fail(self, msg):
        self.items.append(("FAIL", msg))

    @property
    def failed(self):
        return any(l == "FAIL" for l, _ in self.items)

    def print(self):
        symbol = {"OK": "✓", "WARN": "!", "FAIL": "✗"}
        for level, msg in self.items:
            print(f"  [{symbol[level]} {level}] {msg}")

    def summary(self):
        n_ok = sum(1 for l, _ in self.items if l == "OK")
        n_warn = sum(1 for l, _ in self.items if l == "WARN")
        n_fail = sum(1 for l, _ in self.items if l == "FAIL")
        print(f"\n小结: {n_ok} 通过, {n_warn} 警告, {n_fail} 失败")
        return 0 if n_fail == 0 else 1


# ---- 命名规范 -------------------------------------------------------------

# feature 名：全小写 kebab-case，至少两段或含字母数字（拒绝 t1/ctx 这类无意义短名）
FEATURE_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
# 产物文件名：feature 前缀 + 类型词
PRODUCT_TYPES = [
    "requirement", "design", "implementation-plan", "test-report",
    "implementation-report", "review",
]


def check_feature_name(name, report):
    if not FEATURE_RE.match(name):
        report.fail(f"feature 名 '{name}' 不符合规范：须全小写 kebab-case（如 user-auth）")
        return False
    if len(name) <= 2 or name in {"t1", "t2", "req", "ctx", "des", "imp"}:
        report.fail(f"feature 名 '{name}' 过短/无意义，须有意义（如 user-auth，非 t1）")
        return False
    report.ok(f"feature 名 '{name}' 符合命名规范")
    return True


# ---- 项目级校验 -----------------------------------------------------------

def validate_project(root, report):
    print("== 项目级校验 ==")
    develop = root / "develop"
    if not develop.is_dir():
        report.fail("缺少 develop/ 目录（请先跑 /dev-init）")
        return
    report.ok("develop/ 目录存在")

    ctx = develop / "project-context.md"
    if ctx.is_file():
        report.ok("develop/project-context.md 存在")
        # 校验 8 章节标题存在
        text = ctx.read_text(encoding="utf-8")
        for i in range(1, 9):
            if not re.search(rf"^##\s*{i}[\.、]", text, re.M):
                report.warn(f"project-context.md 缺少第 {i} 章标题")
    else:
        report.fail("缺少 develop/project-context.md（dev-init 核心产物）")

    # CLAUDE.md 是否引用了 project-context.md
    claude_md = root / "CLAUDE.md"
    if claude_md.is_file():
        c = claude_md.read_text(encoding="utf-8")
        if "project-context.md" in c:
            report.ok("CLAUDE.md 已引用 project-context.md（可进入 Claude 上下文）")
        else:
            report.fail("CLAUDE.md 未引用 develop/project-context.md，上下文不会被加载")
    else:
        report.warn("仓库根无 CLAUDE.md（dev-init 应创建并引用 project-context.md）")

    # 全局 ADR 目录
    adr_dir = develop / "adr"
    if adr_dir.is_dir():
        report.ok("develop/adr/ 目录存在")
    else:
        report.warn("缺少 develop/adr/（全局 ADR 目录，dev-init 应建）")

    # features 目录
    feats = develop / "features"
    if feats.is_dir():
        report.ok("develop/features/ 目录存在")
    else:
        report.warn("缺少 develop/features/（dev-init 应建）")


# ---- feature 级校验 -------------------------------------------------------

# 阶段 → 该阶段应产出的文件（相对 feature 目录）
STAGE_PRODUCTS = {
    "requirement": ["{f}-requirement.md"],
    "design":      ["{f}-requirement.md", "{f}-design.md"],
    "implement":   ["{f}-requirement.md", "{f}-design.md"],
    "review":      ["{f}-requirement.md", "{f}-design.md"],
}


def validate_feature(root, feature, stage, report):
    print(f"== feature 校验: {feature}（截至 {stage or '全部'}）==")
    if not check_feature_name(feature, report):
        return

    fdir = root / "develop" / "features" / feature
    if not fdir.is_dir():
        report.fail(f"缺少 feature 目录 develop/features/{feature}/（请先用对应上游 skill 产出）")
        return
    report.ok(f"feature 目录存在: develop/features/{feature}/")

    # 命名规范：目录内 .md 文件须带 {feature}- 前缀（除 adr 子目录内的 ADR）
    for md in fdir.glob("*.md"):
        name = md.name
        if not name.startswith(f"{feature}-"):
            report.fail(f"文件 '{name}' 未带 '{feature}-' 前缀，违反命名规范")
        elif not name.lower() == name:
            report.fail(f"文件名 '{name}' 含大写，须全小写")
        else:
            report.ok(f"产物文件命名规范: {name}")

    # 校验任务文件命名
    tdir = fdir / "tasks"
    if tdir.is_dir():
        for t in tdir.glob("*.md"):
            if not re.match(rf"^{feature}-task-\d+-[a-z0-9-]+\.md$", t.name):
                report.fail(f"任务文件命名不规范: {t.name}（应为 {feature}-task-NN-slug.md）")
            else:
                report.ok(f"任务文件命名规范: {t.name}")

    # 产物存在性（按阶段）
    expected = STAGE_PRODUCTS.get(stage, []) if stage else STAGE_PRODUCTS["review"]
    if not stage:
        expected = STAGE_PRODUCTS["review"]
    for pat in expected:
        path = fdir / pat.format(f=feature)
        if path.is_file():
            report.ok(f"上游产物存在: {path.relative_to(root)}")
        else:
            report.fail(f"缺少上游产物 {path.relative_to(root)}（请先跑对应上游 skill）")

    # 阶段专属产物
    if stage in (None, "implement", "review"):
        plan = fdir / f"{feature}-implementation-plan.md"
        if plan.is_file():
            report.ok(f"实施方案存在: {plan.name}")
        elif stage == "review":
            report.warn(f"缺 {plan.name}（review 前应已由 dev-implement 产出）")

    # 验收点覆盖矩阵：requirement 的 AC ↔ tasks 的验收点
    coverage_matrix(root, feature, fdir, report)


def coverage_matrix(root, feature, fdir, report):
    """尽力解析 requirement 的 AC 编号与 tasks 的验收点，核对覆盖。"""
    print("== 验收点覆盖矩阵 ==")
    req = fdir / f"{feature}-requirement.md"
    if not req.is_file():
        report.warn("无 requirement.md，跳过覆盖矩阵")
        return
    text = req.read_text(encoding="utf-8")
    # 匹配 AC1 / AC2 ... 或 验收点1
    acs = set(re.findall(r"AC\s*(\d+)", text, re.I)) or set(re.findall(r"验收点\s*(\d+)", text))
    if not acs:
        report.warn("requirement.md 未识别到 AC/验收点编号，跳过覆盖矩阵")
        return
    report.ok(f"需求中识别到验收点: {sorted(acs, key=int)}")

    tdir = fdir / "tasks"
    covered = set()
    if tdir.is_dir():
        for t in tdir.glob("*.md"):
            tt = t.read_text(encoding="utf-8")
            covered |= set(re.findall(r"AC\s*(\d+)", tt, re.I))
            covered |= set(re.findall(r"验收点\s*(\d+)", tt))
    missing = acs - covered
    if missing:
        report.fail(f"以下验收点无对应任务覆盖: {sorted(missing, key=int)}")
    else:
        report.ok(f"所有验收点均有任务覆盖: {sorted(acs, key=int)}")
    extra = covered - acs
    if extra:
        report.warn(f"任务引用了需求中不存在的验收点: {sorted(extra, key=int)}")


# ---- main ----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="深度开发流程产物校验")
    ap.add_argument("--root", default=".", help="仓库根路径")
    ap.add_argument("--feature", help="要校验的 feature 名")
    ap.add_argument("--stage", choices=["requirement", "design", "implement", "review"],
                    help="只校验截至该阶段的产物（默认校验全部）")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"错误: 仓库根不存在: {root}")
        sys.exit(2)

    report = Report()
    validate_project(root, report)
    if args.feature:
        print()
        validate_feature(root, args.feature, args.stage, report)

    print()
    report.print()
    sys.exit(report.summary())


if __name__ == "__main__":
    main()
