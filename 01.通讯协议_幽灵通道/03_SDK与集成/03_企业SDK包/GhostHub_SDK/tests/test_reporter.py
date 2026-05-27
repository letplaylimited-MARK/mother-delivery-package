"""
Ghost Hub SDK 测试报告生成器
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field, asdict

sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class ReportTestResult:
    name: str
    status: str
    duration: float
    error: str = ""


@dataclass
class ReportTestSuite:
    name: str
    tests: List[ReportTestResult] = field(default_factory=list)
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    duration: float = 0.0


@dataclass
class ReportTestReport:
    timestamp: str
    total_tests: int
    total_passed: int
    total_failed: int
    total_skipped: int
    total_duration: float
    suites: List[ReportTestSuite] = field(default_factory=list)


class Reporter:
    def __init__(self):
        self.suites: Dict[str, ReportTestSuite] = {}
        self.start_time = time.time()

    def start_suite(self, name: str):
        if name not in self.suites:
            self.suites[name] = ReportTestSuite(name=name)

    def add_result(self, suite_name: str, result: ReportTestResult):
        if suite_name not in self.suites:
            self.start_suite(suite_name)

        suite = self.suites[suite_name]
        suite.tests.append(result)

        if result.status == "PASSED":
            suite.passed += 1
        elif result.status == "FAILED":
            suite.failed += 1
        elif result.status == "SKIPPED":
            suite.skipped += 1

    def generate_report(self) -> ReportTestReport:
        total_duration = time.time() - self.start_time

        all_suites = list(self.suites.values())
        for suite in all_suites:
            suite.duration = sum(t.duration for t in suite.tests)

        return ReportTestReport(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            total_tests=sum(s.passed + s.failed + s.skipped for s in all_suites),
            total_passed=sum(s.passed for s in all_suites),
            total_failed=sum(s.failed for s in all_suites),
            total_skipped=sum(s.skipped for s in all_suites),
            total_duration=total_duration,
            suites=all_suites,
        )

    def save_report(self, filepath: str):
        report = self.generate_report()
        data = asdict(report)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def print_summary(self):
        report = self.generate_report()

        print("\n" + "=" * 70)
        print(" Ghost Hub SDK 测试报告 ")
        print("=" * 70)
        print(f"时间: {report.timestamp}")
        print(f"总耗时: {report.total_duration:.2f}s")
        print("-" * 70)

        print(f"\n总计: {report.total_tests} 测试")
        print(f"  ✓ 通过: {report.total_passed}")
        print(f"  ✗ 失败: {report.total_failed}")
        print(f"  - 跳过: {report.total_skipped}")

        if report.total_tests > 0:
            pass_rate = (report.total_passed / report.total_tests) * 100
            print(f"\n通过率: {pass_rate:.1f}%")

        print("\n" + "-" * 70)
        print("按测试套件:")
        print("-" * 70)

        for suite in report.suites:
            total = suite.passed + suite.failed + suite.skipped
            status_icon = "✓" if suite.failed == 0 else "✗"
            print(f"\n{status_icon} {suite.name} ({suite.passed}/{total}) - {suite.duration:.2f}s")

            for test in suite.tests:
                icon = "✓" if test.status == "PASSED" else "✗" if test.status == "FAILED" else "-"
                print(f"    {icon} {test.name} ({test.duration:.3f}s)")
                if test.error:
                    print(f"      Error: {test.error[:50]}...")

        print("\n" + "=" * 70)


def run_and_report():
    import pytest

    reporter = Reporter()

    test_classes = [
        (
            "IntentionBank",
            [
                "test_intent_matching_pipeline",
                "test_multi_intent_parsing",
                "test_task_graph_construction",
                "test_template_domain_filtering",
            ],
        ),
        (
            "NoUIAdapter",
            [
                "test_device_lifecycle",
                "test_protocol_adapters",
                "test_batch_command_execution",
                "test_scene_execution",
                "test_intent_to_command_conversion",
            ],
        ),
        (
            "AgentFederation",
            [
                "test_agent_registration",
                "test_routing_strategies",
                "test_task_distribution",
                "test_collaborative_session",
                "test_message_broadcast",
            ],
        ),
        (
            "CrossComponent",
            [
                "test_intent_to_device_control",
                "test_intent_to_agent_routing",
                "test_multi_agent_task_flow",
            ],
        ),
        (
            "FullWorkflow",
            [
                "test_hr_interview_workflow",
                "test_iot_control_workflow",
                "test_multi_domain_workflow",
            ],
        ),
        (
            "EdgeCases",
            [
                "test_empty_intent",
                "test_unknown_domain",
                "test_device_not_found",
                "test_agent_not_found",
                "test_invalid_scene",
            ],
        ),
    ]

    from ghost_hub_sdk.tests import test_integration

    for suite_name, test_names in test_classes:
        for test_name in test_names:
            start = time.time()
            try:
                test_func = getattr(test_integration, test_name)
                test_func()
                status = "PASSED"
                error = ""
            except Exception as e:
                status = "FAILED"
                error = str(e)

            duration = time.time() - start
            result = ReportTestResult(
                name=test_name,
                status=status,
                duration=duration,
                error=error,
            )
            reporter.add_result(suite_name, result)

    reporter.print_summary()
    reporter.save_report("test_report.json")

    return reporter


if __name__ == "__main__":
    run_and_report()
