#!/usr/bin/env python3
"""
00层跨文档一致性验证脚本
Cross-Document Consistency Validator for 00.超级提示词工程

验证维度:
  C1: QCM Skill引用一致性 — 所有引导文档必须引用 qcm-universal-ai-system-v3.0.skill
  C2: 启动顺序权威声明 — 所有启动协议必须引用 MOTHER-PACK-ACTIVATION-GUIDE.md 为权威来源
  C3: 子系统路径一致性 — 所有文档引用的7个子系统路径必须存在
  C4: SSP版本声明 — 只有 v3.0 AWAKENING 可以是 ACTIVE，其余必须标记 DEPRECATED
  C5: 路由矩阵条目完整性 — 一级路由必须覆盖所有子系统
  C6: 反幻觉铁律数量 — SSP v3.0 的 L10 必须包含12条铁律
  C7: 引导秘书5D雷达 — GUIDE-SECRETARY-PROTOCOL.md 必须包含5个维度
  C8: 意图注册表 — GUIDE-SECRETARY-PROTOCOL.md 必须包含13个意图类型
  C9: 关键文件交叉引用 — 核心文档间必须互相引用
  C10: 模型原生边界 — 所有协议必须声明模型规则优先

Usage:
  python validate_consistency.py [MOTHER_PACK_ROOT]
"""

import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    check_id: str
    description: str
    status: str  # PASS, FAIL, WARN
    details: str = ""
    files_checked: list = field(default_factory=list)


class ConsistencyValidator:
    def __init__(self, root: Path):
        self.root = root
        self.results: list[CheckResult] = []
        self.subsystems = [
            "00.超级提示词工程",
            "01.通讯协议_幽灵通道",
            "02.通用知识库框架_Universal-KB",
            "03.数据库管理_文件夹整理AI应用",
            "04.QCM-MVP-Emergence",
            "05.超极智脑_Q-SpecTrum",
            "协同通用AI大模型开发交付包",
        ]
        self.qcm_skill_file = "qcm-universal-ai-system-v3.0.skill"

    def _read(self, rel_path: str) -> str:
        full = self.root / rel_path
        if not full.exists():
            return ""
        return full.read_text(encoding="utf-8", errors="replace")

    def _add(self, check_id: str, desc: str, status: str,
             details: str = "", files: list | None = None):
        self.results.append(CheckResult(
            check_id=check_id, description=desc, status=status,
            details=details, files_checked=files or []
        ))

    def check_c1_qcm_skill_reference(self):
        """C1: 所有引导文档必须引用QCM Skill文件"""
        guide_docs = [
            "MOTHER-PACK-ACTIVATION-GUIDE.md",
            "00.超级提示词工程/01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md",
            "00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md",
            ("00.超级提示词工程/15-超级系统提示词工程/"
             "SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md"),
        ]
        qcm_ref = "qcm-universal-ai-system-v3.0.skill"
        missing = []
        for doc in guide_docs:
            content = self._read(doc)
            if qcm_ref not in content:
                missing.append(doc)

        if not missing:
            self._add("C1", "QCM Skill引用一致性", "PASS",
                      "所有4个引导文档均引用QCM Skill文件", guide_docs)
        else:
            self._add("C1", "QCM Skill引用一致性", "FAIL",
                      f"以下文档未引用QCM Skill: {missing}", guide_docs)

    def check_c2_activation_guide_authority(self):
        """C2: 所有启动协议必须引用ACTIVATION-GUIDE为权威来源"""
        startup_docs = [
            "00.超级提示词工程/01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md",
            "00.超级提示词工程/12-引导秘书逻辑/"
            "MISSION-MEMORY-AWAKENING-PROTOCOL.md",
            ("00.超级提示词工程/15-超级系统提示词工程/"
             "SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md"),
        ]
        ref = "MOTHER-PACK-ACTIVATION-GUIDE.md"
        missing = []
        for doc in startup_docs:
            content = self._read(doc)
            if ref not in content:
                missing.append(doc)
            elif "权威" not in content and "authoritative" not in content.lower():
                missing.append(f"{doc} (无权威声明)")

        if not missing:
            self._add("C2", "启动顺序权威声明", "PASS",
                      "所有启动协议均引用ACTIVATION-GUIDE为权威来源",
                      startup_docs)
        else:
            self._add("C2", "启动顺序权威声明", "FAIL",
                      f"以下文档缺少权威引用: {missing}", startup_docs)

    def check_c3_subsystem_paths(self):
        """C3: 所有子系统路径必须实际存在"""
        missing = []
        for sub in self.subsystems:
            if not (self.root / sub).is_dir():
                missing.append(sub)

        if not missing:
            self._add("C3", "子系统路径完整性", "PASS",
                      f"全部{len(self.subsystems)}个子系统目录存在",
                      self.subsystems)
        else:
            self._add("C3", "子系统路径完整性", "FAIL",
                      f"缺失子系统目录: {missing}", self.subsystems)

    def check_c4_ssp_versions(self):
        """C4: SSP版本声明正确性"""
        ssp_dir = self.root / "00.超级提示词工程/15-超级系统提示词工程"
        issues = []
        active_found = False

        if not ssp_dir.exists():
            self._add("C4", "SSP版本声明", "FAIL", "SSP目录不存在")
            return

        for f in ssp_dir.iterdir():
            if not f.name.startswith("SUPER-SYSTEM-PROMPT"):
                continue
            content = f.read_text(encoding="utf-8", errors="replace")
            # Only check first 200 chars for DEPRECATED (header area)
            header = content[:200]
            is_v3 = "v3.0" in f.name or "AWAKENING" in f.name

            if is_v3:
                if "DEPRECATED" in header:
                    issues.append(f"{f.name}: v3.0不应标记DEPRECATED")
                else:
                    active_found = True
            else:
                # v1.0 or v2.x should be DEPRECATED in header
                if "DEPRECATED" not in header:
                    issues.append(f"{f.name}: 旧版未标记DEPRECATED")

        if not issues and active_found:
            self._add("C4", "SSP版本声明", "PASS",
                      "v3.0 AWAKENING活跃, 旧版已标记DEPRECATED")
        elif not active_found:
            self._add("C4", "SSP版本声明", "FAIL",
                      "未找到活跃的v3.0 AWAKENING版本")
        else:
            self._add("C4", "SSP版本声明", "FAIL",
                      f"版本声明问题: {issues}")

    def check_c5_routing_matrix_coverage(self):
        """C5: 路由矩阵一级路由必须覆盖所有子系统"""
        content = self._read(
            "00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md"
        )
        uncovered = []
        for sub in self.subsystems:
            short = sub.split(".")[0].replace("0", "") if sub[0].isdigit() else sub[:4]
            # Check if any recognizable part of the subsystem name appears
            parts = [p for p in re.split(r"[_\-./]", sub) if len(p) > 1]
            found = any(p in content for p in parts if len(p) > 2)
            if not found and sub not in content:
                uncovered.append(sub)

        if not uncovered:
            self._add("C5", "路由矩阵覆盖度", "PASS",
                      "一级路由覆盖所有子系统")
        else:
            self._add("C5", "路由矩阵覆盖度", "WARN",
                      f"以下子系统可能未被一级路由覆盖: {uncovered}")

    def check_c6_anti_hallucination_rules(self):
        """C6: SSP v3.0 L10必须包含12条铁律"""
        content = self._read(
            "00.超级提示词工程/15-超级系统提示词工程/"
            "SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md"
        )
        # Count numbered rules in L10 section
        l10_match = re.search(
            r"L10.*?铁律.*?\n(.*?)(?=\n---|\n##|\Z)", content, re.DOTALL
        )
        if l10_match:
            rules_text = l10_match.group(1)
            numbered = re.findall(r"^\d+\.", rules_text, re.MULTILINE)
            count = len(numbered)
            if count == 12:
                self._add("C6", "反幻觉铁律数量", "PASS",
                          f"L10包含{count}条铁律")
            else:
                self._add("C6", "反幻觉铁律数量", "FAIL",
                          f"L10包含{count}条铁律, 期望12条")
        else:
            self._add("C6", "反幻觉铁律数量", "FAIL",
                      "未找到L10铁律章节")

    def check_c7_5d_radar(self):
        """C7: 引导秘书必须包含5D雷达"""
        content = self._read(
            "00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md"
        )
        dimensions = ["Track", "Platform", "People", "Style", "Supplement"]
        missing = [d for d in dimensions if d not in content]
        if not missing:
            self._add("C7", "5D雷达维度", "PASS",
                      "全部5个雷达维度存在")
        else:
            self._add("C7", "5D雷达维度", "FAIL",
                      f"缺失维度: {missing}")

    def check_c8_intent_registry(self):
        """C8: 意图注册表必须包含13个意图类型"""
        content = self._read(
            "00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md"
        )
        # Look for intent IDs in the intent registry table
        intent_pattern = re.findall(
            r"\| `([A-Z_]+)` ", content
        )
        # Deduplicate
        intents = list(set(intent_pattern))
        # Known required intents (from the spec)
        required = [
            "PACKAGE_UNDERSTANDING", "GUIDE_SECRETARY", "PROJECT_INITIATION",
            "REQUIREMENT_SPEC", "IMPLEMENTATION", "REVIEW_AUDIT",
            "KNOWLEDGE_MEMORY", "ROLE_TEAM_SANDBOX", "CAPABILITY_INTEGRATION",
            "MISSION_MEMORY_AWAKENING", "MODEL_NATIVE_HANDOFF",
            "USER_DELIVERY", "AMBIGUOUS",
        ]
        missing = [r for r in required if r not in intents]
        if not missing:
            self._add("C8", "意图注册表完整性", "PASS",
                      f"全部{len(required)}个意图类型存在")
        else:
            self._add("C8", "意图注册表完整性", "FAIL",
                      f"缺失意图: {missing}")

    def check_c9_cross_references(self):
        """C9: 关键文档间必须互相引用"""
        checks = [
            ("MASTER-ORCHESTRATOR", "GUIDE-SECRETARY-PROTOCOL",
             "00.超级提示词工程/01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md",
             "GUIDE-SECRETARY-PROTOCOL"),
            ("MASTER-ORCHESTRATOR", "ROUTING-MATRIX",
             "00.超级提示词工程/01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md",
             "ROUTING-MATRIX"),
            ("GUIDE-SECRETARY", "ROUTING-MATRIX",
             "00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md",
             "ROUTING-MATRIX"),
            ("SSP-v3", "GUIDE-SECRETARY",
             "00.超级提示词工程/15-超级系统提示词工程/"
             "SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md",
             "引导秘书"),
            ("AWAKENING-PROTOCOL", "GUIDE-SECRETARY",
             "00.超级提示词工程/12-引导秘书逻辑/"
             "MISSION-MEMORY-AWAKENING-PROTOCOL.md",
             "GUIDE-SECRETARY"),
        ]
        missing = []
        for name, target, doc, ref in checks:
            content = self._read(doc)
            if not content:
                missing.append(f"{name}->{target}: 文件不存在")
            elif ref not in content:
                missing.append(f"{name}->{target}: 未引用{ref}")

        if not missing:
            self._add("C9", "关键文档交叉引用", "PASS",
                      "所有关键文档间互相引用正确")
        else:
            self._add("C9", "关键文档交叉引用", "FAIL",
                      f"缺失引用: {missing}")

    def check_c10_model_native_boundary(self):
        """C10: 所有协议必须声明模型规则优先"""
        docs = [
            ("ACTIVATION-GUIDE",
             "MOTHER-PACK-ACTIVATION-GUIDE.md"),
            ("MASTER-ORCHESTRATOR",
             "00.超级提示词工程/01-总控提示词/"
             "MASTER-ORCHESTRATOR-PROMPT.md"),
            ("GUIDE-SECRETARY",
             "00.超级提示词工程/12-引导秘书逻辑/"
             "GUIDE-SECRETARY-PROTOCOL.md"),
            ("AWAKENING-PROTOCOL",
             "00.超级提示词工程/12-引导秘书逻辑/"
             "MISSION-MEMORY-AWAKENING-PROTOCOL.md"),
            ("SSP-v3",
             "00.超级提示词工程/15-超级系统提示词工程/"
             "SUPER-SYSTEM-PROMPT-v3.0-AWAKENING.md"),
        ]
        missing = []
        boundary_keywords = ["模型", "系统规则", "优先", "边界"]
        for name, doc in docs:
            content = self._read(doc)
            if not content:
                missing.append(f"{name}: 文件不存在")
                continue
            found = sum(1 for kw in boundary_keywords if kw in content)
            if found < 2:
                missing.append(f"{name}: 模型原生边界声明不足({found}/3)")

        if not missing:
            self._add("C10", "模型原生边界声明", "PASS",
                      "所有协议均声明模型规则优先")
        else:
            self._add("C10", "模型原生边界声明", "WARN",
                      f"边界声明不足: {missing}")

    def run_all(self) -> list[CheckResult]:
        self.check_c1_qcm_skill_reference()
        self.check_c2_activation_guide_authority()
        self.check_c3_subsystem_paths()
        self.check_c4_ssp_versions()
        self.check_c5_routing_matrix_coverage()
        self.check_c6_anti_hallucination_rules()
        self.check_c7_5d_radar()
        self.check_c8_intent_registry()
        self.check_c9_cross_references()
        self.check_c10_model_native_boundary()
        return self.results


def print_report(results: list[CheckResult]):
    pass_count = sum(1 for r in results if r.status == "PASS")
    fail_count = sum(1 for r in results if r.status == "FAIL")
    warn_count = sum(1 for r in results if r.status == "WARN")
    total = len(results)

    print("=" * 70)
    print("  00层跨文档一致性验证报告")
    print("  Cross-Document Consistency Validation Report")
    print("=" * 70)
    print(f"  总检查项: {total}  |  "
          f"PASS: {pass_count}  |  FAIL: {fail_count}  |  WARN: {warn_count}")
    print("=" * 70)

    for r in results:
        icon = {"PASS": "+", "FAIL": "X", "WARN": "!"}[r.status]
        print(f"\n  [{icon}] {r.check_id}: {r.description}")
        print(f"      状态: {r.status}")
        if r.details:
            print(f"      详情: {r.details}")
        if r.files_checked:
            for f in r.files_checked[:3]:
                print(f"      文件: {f}")
            if len(r.files_checked) > 3:
                print(f"      ...及另外{len(r.files_checked)-3}个文件")

    print("\n" + "=" * 70)
    if fail_count == 0 and warn_count == 0:
        print("  结果: ALL CLEAR - 全部通过")
    elif fail_count == 0:
        print(f"  结果: PASS WITH WARNINGS - {warn_count}个警告需关注")
    else:
        print(f"  结果: ACTION REQUIRED - {fail_count}个失败项需修复")
    print("=" * 70)

    return 0 if fail_count == 0 else 1


def main():
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])
    else:
        root = Path(__file__).resolve().parent.parent.parent

    if not (root / "MISSION-MEMORY.md").exists():
        print(f"错误: 未在 {root} 找到 MISSION-MEMORY.md")
        print("用法: python validate_consistency.py [母交付包根目录]")
        sys.exit(1)

    validator = ConsistencyValidator(root)
    results = validator.run_all()
    exit_code = print_report(results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
