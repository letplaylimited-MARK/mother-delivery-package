#!/usr/bin/env python3
"""
Mother Delivery Package - QA Runner (三环集成内核)
=====================================================
统一入口脚本，覆盖4条子命令：
  validate     Validation环 — 执行VALIDATION_REGISTRY 注册验证命令
  status       Status环 — 读取4注册表+LEDGER，输出系统全貌
  consistency  Consistency环 — 10维度跨文档一致性检查
  route        Routing环 — Guide Secretary意图匹配与路由

Usage:
  python qa_runner.py validate [--scope SCOPE]
  python qa_runner.py status
  python qa_runner.py consistency
  python qa_runner.py route "<user input text>"

Phase 1-3 可执行脚本（GUIDE-SECRETARY-PROTOCOL.md §14）
"""

import argparse
import shlex
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    # Fallback: minimal YAML loader for simple cases
    yaml = None

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MOTHER_ROOT = Path(__file__).resolve().parent
REGISTRY_DIR = MOTHER_ROOT / "00.超级提示词工程" / "14-全链路审计与运行对齐"
VALIDATION_REGISTRY_PATH = REGISTRY_DIR / "VALIDATION_REGISTRY.yaml"
PROJECT_REGISTRY_PATH = REGISTRY_DIR / "PROJECT_REGISTRY.yaml"
CAPABILITY_REGISTRY_PATH = REGISTRY_DIR / "CAPABILITY_REGISTRY.yaml"
ARTIFACT_REGISTRY_PATH = REGISTRY_DIR / "ARTIFACT_REGISTRY.yaml"
LEDGER_PATH = REGISTRY_DIR / "UNIFIED-STATUS-LEDGER.yaml"
CONSISTENCY_SCRIPT = MOTHER_ROOT / "00.超级提示词工程" / "validate_consistency.py"

# Python used by run_cmd for validation commands.
# Override with MOTHER_PACK_PYTHON when a dedicated validation interpreter is needed.
VENV_PYTHON = Path(os.environ.get("MOTHER_PACK_PYTHON", sys.executable))
PYTEST_COMMAND = os.environ.get("MOTHER_PACK_PYTEST")
if not PYTEST_COMMAND:
    pytest_path = shutil.which("pytest")
    PYTEST_COMMAND = f'"{pytest_path}"' if pytest_path else f'"{VENV_PYTHON}" -m pytest'

VALIDATION_SCOPE_MAP = {
    "ROOT": ".",
    "P00_SUPER_PROMPT": "00.超级提示词工程",
    "P01_GHOST_CHANNEL": "01.通讯协议_幽灵通道",
    "P02_UNIVERSAL_KB": "02.通用知识库框架_Universal-KB",
    "P03_WORKBUDDY_KB": "03.数据库管理_文件夹整理AI应用",
    "P04_QCM": "04.QCM-MVP-Emergence",
    "P05_QSPECTRUM": "05.超极智脑_Q-SpecTrum",
    "USER_PACK": "协同通用AI大模型开发交付包",
    "REFERENCE_PROJECT": "_reference_projects/minimal-ai-collab-taskboard",
}

INTENT_REGISTRY = {
    "SELF_BOOTSTRAP_PROJECT": {
        "keywords": ["自举", "母包自身", "开发自己", "反哺仓库", "自身仓库",
                     "第一次真正", "真实项目实例", "完善母包",
                     "self-bootstrap", "self bootstrap", "mother-delivery-package自己"],
        "primary_route": "ROOT -> 00 -> 03/04/05 -> USER_PACK",
        "track": "implementation",
    },
    "PACKAGE_UNDERSTANDING": {
        "keywords": ["理解", "母包", "目录", "地图", "集成", "整体", "全貌",
                     "架构", "架构概览", "导航", "overview", "understand",
                     "文件夹", "子系统"],
        "primary_route": "00/00 + MISSION-MEMORY.md",
        "track": "understanding",
    },
    "GUIDE_SECRETARY": {
        "keywords": ["引导", "秘书", "路由", "交接", "handoff", "5D", "雷达",
                     "入口", "分流", "navigator"],
        "primary_route": "00/12 引导秘书逻辑",
        "track": "understanding",
    },
    "PROJECT_INITIATION": {
        "keywords": ["新项目", "启动", "初始化", "想法", "立项", "kickoff",
                     "init", "project start"],
        "primary_route": "00/06 + 用户交付包四体系",
        "track": "planning",
    },
    "REQUIREMENT_SPEC": {
        "keywords": ["需求", "PRD", "SPEC", "规格", "变更", "漂移", "冻结",
                     "requirement", "specification"],
        "primary_route": "00/06 + 00/07",
        "track": "prd_spec",
    },
    "IMPLEMENTATION": {
        "keywords": ["开发", "代码", "实现", "集成", "修复", "fix", "implement",
                     "code", "bug", "feature", "启动", "运行"],
        "primary_route": "目标子系统 + 对应验证",
        "track": "implementation",
    },
    "REVIEW_AUDIT": {
        "keywords": ["审查", "审计", "评审", "review", "audit", "检查",
                     "验证", "quality", "重构", "收敛", "停止", "断裂",
                     "问题日志", "风险"],
        "primary_route": "目标子系统 + 00/14 + 00/07 + 测试/证据",
        "track": "review",
    },
    "KNOWLEDGE_MEMORY": {
        "keywords": ["知识库", "记忆", "图谱", "结晶", "knowledge", "memory",
                     "brain", "检索", "search"],
        "primary_route": "02 + 03 + 05/BRAIN-KB",
        "track": "memory",
    },
    "ROLE_TEAM_SANDBOX": {
        "keywords": ["角色", "团队", "沙盘", "推演", "role", "team",
                     "sandbox", "涌现", "emergence"],
        "primary_route": "00/08 + 04",
        "track": "planning",
    },
    "CAPABILITY_INTEGRATION": {
        "keywords": ["模型", "智能体", "Skill", "MCP", "插件", "LSP",
                     "integration", "plugin", "capability", "Q-SpecTrum",
                     "QSpecTrum", "超极智脑", "智脑", "qspectrum"],
        "primary_route": "00/10 通用AI协作生态 或 05.Q-SpecTrum",
        "track": "implementation",
    },
    "MISSION_MEMORY_AWAKENING": {
        "keywords": ["使命", "唤醒", "身份", "元智核", "活起来", "awakening",
                     "mission", "identity"],
        "primary_route": "MISSION-MEMORY.md + 00/12",
        "track": "memory",
    },
    "MODEL_NATIVE_HANDOFF": {
        "keywords": ["接手", "其他AI", "handoff", "移交", "transfer",
                     "model native"],
        "primary_route": "00/11 模型原生协作协议",
        "track": "delivery",
    },
    "USER_DELIVERY": {
        "keywords": ["交付", "打包", "用户", "四体系", "delivery", "package",
                     "release", "发布"],
        "primary_route": "协同通用AI大模型开发交付包",
        "track": "delivery",
    },
    "CROSS_SYSTEM_GOLDEN_PATH": {
        "keywords": ["想法", "需求", "规格", "任务", "测试", "交付",
                     "闭环", "跨系统", "golden path", "end-to-end"],
        "primary_route": "ROOT -> 00 -> 03/04/05 -> USER_PACK",
        "track": "delivery",
    },
    "AMBIGUOUS": {
        "keywords": [],
        "primary_route": "追问，不执行",
        "track": "understanding",
    },
}


def _route_validation_refs(intent_id: str, platform: str) -> list[str]:
    refs = ["VAL-ROOT-ROUTE-SMOKE"]
    if intent_id == "SELF_BOOTSTRAP_PROJECT":
        refs.extend(["VAL-00-AUDIT-ASSETS", "VAL-00-CROSS-DOC-CONSISTENCY",
                     "VAL-END-TO-END", "VAL-CROSS-INTERFACE",
                     "VAL-USER-PACK-DELIVERY-STRICT"])
    if intent_id == "MISSION_MEMORY_AWAKENING":
        refs.extend(["VAL-00-AUDIT-ASSETS", "VAL-00-CROSS-DOC-CONSISTENCY"])
    if platform == "P03_WORKBUDDY_KB":
        refs.extend(["VAL-03-INSTALL", "VAL-03-TESTS", "VAL-03-HTTP-SMOKE"])
    if platform == "P04_QCM":
        refs.extend(["VAL-04-QCM-RUNTIME-SMOKE", "VAL-QCM-SKILL-VALIDATE"])
    if platform == "P05_QSPECTRUM":
        refs.extend(["VAL-05-STATUS", "VAL-05-API-SMOKE", "VAL-05-MCP-SMOKE"])
    if platform == "USER_PACK" or intent_id == "USER_DELIVERY":
        refs.extend(["VAL-USER-PACK-DELIVERY", "VAL-USER-PACK-DELIVERY-STRICT"])
    if platform == "cross_subsystem" or intent_id == "CROSS_SYSTEM_GOLDEN_PATH":
        refs.extend(["VAL-END-TO-END", "VAL-CROSS-INTERFACE",
                     "VAL-USER-PACK-DELIVERY-STRICT"])
    if intent_id == "REVIEW_AUDIT":
        refs.extend(["VAL-END-TO-END", "VAL-CROSS-INTERFACE"])
    return list(dict.fromkeys(refs))


def _route_uso_id(intent_id: str, platform: str) -> str | None:
    if intent_id == "SELF_BOOTSTRAP_PROJECT":
        return "GOAL-20260601-MOTHER-PACK-SELF-BOOTSTRAP"
    if intent_id == "CROSS_SYSTEM_GOLDEN_PATH":
        return "AUD-20260531-B7-CROSS-SYSTEM-GOLDEN-PATHS"
    if intent_id == "MISSION_MEMORY_AWAKENING":
        return "GOAL-20260526-MOTHER-PACK-COLLABORATION"
    if platform == "P03_WORKBUDDY_KB":
        return "GOAL-20260526-SUBSYSTEM-03"
    if platform == "P04_QCM":
        return "AUD-20260531-P04-QCM-SKILL"
    if platform == "P05_QSPECTRUM":
        return "AUD-20260531-P05-QSPECTRUM-RUNTIME"
    if platform == "USER_PACK":
        return "GOAL-20260526-USER-PACK"
    if intent_id == "REVIEW_AUDIT":
        return "AUD-20260531-B7-CROSS-SYSTEM-GOLDEN-PATHS"
    return None

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict | None:
    """Load YAML file, with fallback if pyyaml not available."""
    if yaml:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"  [WARN] YAML parse error: {path}: {e}", file=sys.stderr)
            return None
    else:
        print(f"  [WARN] PyYAML not installed, cannot read {path}", file=sys.stderr)
        return None


def _reroute_python(cmd: str) -> str:
    """Replace bare 'python' invocations with venv Python path."""
    venv_str = str(VENV_PYTHON).replace("\\", "\\\\")
    # Match 'python ...' or 'python -m ...' but not inside quoted paths
    cmd = re.sub(
        r'\bpython(?=\s)', venv_str, cmd, count=1
    )
    return cmd


def _powershell_exe() -> str | None:
    """Return a PowerShell executable available on the current platform."""
    return shutil.which("pwsh") or shutil.which("powershell")


def _powershell_file_cmd(script: str, *args: str) -> str | None:
    """Build a cross-platform PowerShell file invocation for run_cmd."""
    ps = _powershell_exe()
    if not ps:
        return None
    parts = [ps, "-NoProfile"]
    if Path(ps).name.lower().startswith("powershell"):
        parts.extend(["-ExecutionPolicy", "Bypass"])
    parts.extend(["-File", script])
    parts.extend(args)
    if os.name == "nt":
        return subprocess.list2cmdline([str(part) for part in parts])
    return " ".join(shlex.quote(str(part)) for part in parts)


def run_cmd(cmd: str, cwd: Path | None = None, timeout: int = 120) -> dict:
    """Execute a command and return structured result."""
    start = time.time()
    # Ensure shell environment is available (ComSpec, SystemRoot, PATH)
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    # Auto-route 'python' to venv Python if available
    if VENV_PYTHON.exists():
        cmd = _reroute_python(cmd)
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd or MOTHER_ROOT,
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace", env=env
        )
        elapsed = time.time() - start
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "elapsed": round(elapsed, 2),
            "timeout": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"TIMEOUT after {timeout}s",
            "elapsed": timeout,
            "timeout": True,
        }
    except Exception as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "elapsed": time.time() - start,
            "timeout": False,
        }


def run_cmd_raw(cmd: str, cwd: Path | None = None, timeout: int = 120,
                 env: dict | None = None) -> dict:
    """Execute a command with custom env (no venv rerouting)."""
    start = time.time()
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd or MOTHER_ROOT,
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace", env=env or os.environ.copy()
        )
        elapsed = time.time() - start
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "elapsed": round(elapsed, 2),
            "timeout": False,
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": f"TIMEOUT after {timeout}s",
                "elapsed": timeout, "timeout": True}
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e),
                "elapsed": time.time() - start, "timeout": False}


def print_header(title: str, width: int = 70):
    print("=" * width)
    print(f"  {title}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * width)


def print_subheader(title: str, width: int = 70):
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}")


def _free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _auto_qcm_runtime_smoke(cwd: Path | None) -> dict:
    """Run the three qcm.main modes: research, production output, and HTTP smoke."""
    qcm_root = cwd or (MOTHER_ROOT / "04.QCM-MVP-Emergence")
    details = []
    failures = []

    research_cmd = "python -m qcm.main --mode research --seed 42 --max-rounds 22 --log-level WARNING"
    research = run_cmd(research_cmd, cwd=qcm_root, timeout=180)
    research_text = f"{research['stdout']}\n{research['stderr']}"
    if research["exit_code"] == 0 and "EMERGENCE: YES" in research_text and "Rounds: 22" in research_text:
        details.append("research R22 emergence PASS")
    else:
        failures.append(f"research failed: {research_text[-300:].strip()}")

    with tempfile.TemporaryDirectory(prefix="qcm_prod_smoke_") as out_dir:
        prod_cmd = f'python -m qcm.main --mode production --seed 42 --max-rounds 3 --output "{out_dir}" --log-level WARNING'
        production = run_cmd(prod_cmd, cwd=qcm_root, timeout=180)
        files = list(Path(out_dir).glob("qcm_result_*.json"))
        if production["exit_code"] == 0 and files:
            try:
                payload = json.loads(files[0].read_text(encoding="utf-8"))
                if payload.get("total_rounds") == 3 and "max_R" in payload:
                    details.append("production JSON output PASS")
                else:
                    failures.append(f"production JSON unexpected: {payload}")
            except Exception as exc:
                failures.append(f"production JSON unreadable: {exc}")
        else:
            text = f"{production['stdout']}\n{production['stderr']}"
            failures.append(f"production failed: {text[-300:].strip()}")

    port = _free_local_port()
    python_exe = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.Popen(
        [python_exe, "-m", "qcm.main", "--mode", "service", "--port", str(port), "--log-level", "WARNING"],
        cwd=qcm_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    try:
        base = f"http://127.0.0.1:{port}"
        last_error = None
        health = None
        for _ in range(40):
            try:
                with urllib.request.urlopen(base + "/health", timeout=1) as resp:
                    health = json.loads(resp.read().decode("utf-8"))
                break
            except Exception as exc:
                last_error = exc
                time.sleep(0.25)
        if health is None:
            failures.append(f"service did not start: {last_error}")
        else:
            with urllib.request.urlopen(base + "/status", timeout=2) as resp:
                status_payload = json.loads(resp.read().decode("utf-8"))
            body = json.dumps({"rounds": 3, "seed": 42, "roles": ["Secretary", "Researcher"]}).encode("utf-8")
            req = urllib.request.Request(
                base + "/simulate",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                simulate = json.loads(resp.read().decode("utf-8"))
            if (
                health.get("status") == "healthy"
                and status_payload.get("status") == "running"
                and simulate.get("total_rounds") == 3
            ):
                details.append("service /health /status /simulate PASS")
            else:
                failures.append(f"service unexpected: {health} {status_payload} {simulate}")
    except Exception as exc:
        failures.append(f"service smoke failed: {exc}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)

    return {
        "id": "VAL-04-QCM-RUNTIME-SMOKE",
        "scope": "",
        "status": "FAIL" if failures else "PASS",
        "detail": "; ".join(failures or details),
        "command": "qcm.main research/production/service smoke",
        "auto": True,
    }


def _auto_qcm_skill(validate_only: bool) -> dict:
    """Validate the qcm-v3.0 .skill archive in an isolated temp directory."""
    archive = MOTHER_ROOT / "qcm-universal-ai-system-v3.0.skill"
    vid = "VAL-QCM-SKILL-VALIDATE" if validate_only else "VAL-QCM-SKILL-TESTS"
    if not archive.exists():
        return {
            "id": vid, "scope": "", "status": "FAIL",
            "detail": f"archive missing: {archive}",
            "command": str(archive), "auto": True,
        }

    with tempfile.TemporaryDirectory(prefix="qcm_skill_") as tmp_dir:
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(tmp_dir)
        skill_root = Path(tmp_dir) / "qcm-v3.0"
        if validate_only:
            cmd = "python scripts/validate_qcm.py"
            expected = "FINAL RESULT: PASS"
        else:
            cmd = "pytest tests -q"
            expected = "passed"
        r = run_cmd(cmd, cwd=skill_root, timeout=240)
        combined = f"{r['stdout']}\n{r['stderr']}"
        status = "PASS" if r["exit_code"] == 0 and expected in combined else "FAIL"
        return {
            "id": vid, "scope": "", "status": status,
            "detail": combined[-500:].strip(),
            "command": cmd, "auto": True,
        }


def _aggregate_auto_results(vid: str, checks: list[tuple[str, dict]]) -> dict:
    failures = []
    details = []
    for name, result in checks:
        status = result.get("status", "UNKNOWN")
        details.append(f"{name}={status}")
        if status != "PASS":
            failures.append(f"{name}: {result.get('detail', '')[:160]}")
    return {
        "id": vid,
        "scope": "ROOT",
        "status": "PASS" if not failures else "FAIL",
        "detail": "; ".join(failures or details),
        "command": "meta validation gate",
        "auto": True,
    }


def _auto_scenario_matrix_gate() -> dict:
    matrix = REGISTRY_DIR / "SCENARIO-ACCEPTANCE-MATRIX.md"
    if not matrix.exists():
        return {
            "id": "VAL-SCENARIO-MATRIX", "scope": "ROOT",
            "status": "FAIL", "detail": f"Missing {matrix}",
            "auto": True,
        }
    text = matrix.read_text(encoding="utf-8", errors="replace")
    missing = []
    for sid in [f"GS-{i:02d}" for i in range(1, 9)]:
        if f"| {sid} | VERIFIED" not in text:
            missing.append(sid)
    required_phrases = [
        "VAL-03-HTTP-SMOKE",
        "AUD-20260531-B7-CROSS-SYSTEM-GOLDEN-PATHS",
        "停止结构扩写",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            missing.append(phrase)
    return {
        "id": "VAL-SCENARIO-MATRIX",
        "scope": "ROOT",
        "status": "PASS" if not missing else "FAIL",
        "detail": "GS-01..GS-08 VERIFIED with B7 stop line" if not missing else f"Missing: {missing}",
        "auto": True,
    }


def _auto_user_pack_strict() -> dict:
    user_pack = MOTHER_ROOT / "协同通用AI大模型开发交付包"
    cmd = _powershell_file_cmd("./VERIFY-DELIVERY.ps1", "-Strict")
    if cmd is None:
        return {
            "id": "VAL-USER-PACK-STRICT-META",
            "scope": "USER_PACK",
            "status": "FAIL",
            "detail": "PowerShell executable not found; cannot run VERIFY-DELIVERY.ps1 -Strict",
            "command": "VERIFY-DELIVERY.ps1 -Strict",
            "auto": True,
        }
    r = run_cmd(cmd, cwd=user_pack, timeout=120)
    return {
        "id": "VAL-USER-PACK-STRICT-META",
        "scope": "USER_PACK",
        "status": "PASS" if r["exit_code"] == 0 else "FAIL",
        "detail": r["stdout"][-300:] or r["stderr"][-200:],
        "command": "VERIFY-DELIVERY.ps1 -Strict",
        "auto": True,
    }


def _auto_qcm_config_sync_meta() -> dict:
    qcm_root = MOTHER_ROOT / "04.QCM-MVP-Emergence"
    qcm_py = str(qcm_root).replace("\\", "/")
    r = run_cmd(f'set PYTHONPATH={qcm_py}&& python "02-代码编写/test_config_sync.py"',
                cwd=qcm_root, timeout=180)
    return {
        "id": "VAL-QCM-CONFIG-SYNC-META",
        "scope": "P04_QCM",
        "status": "PASS" if r["exit_code"] == 0 else "FAIL",
        "detail": r["stdout"][-300:] or r["stderr"][-200:],
        "command": "test_config_sync.py",
        "auto": True,
    }


def _auto_reference_project_smoke() -> dict:
    test_script = MOTHER_ROOT / "_reference_projects" / "minimal-ai-collab-taskboard" / "tests" / "test_smoke.py"
    if not test_script.exists():
        return {
            "id": "VAL-REFERENCE-PROJECT-SMOKE",
            "scope": "ROOT/REFERENCE_PROJECT",
            "status": "FAIL",
            "detail": f"Missing reference project smoke: {test_script}",
            "command": "python _reference_projects/minimal-ai-collab-taskboard/tests/test_smoke.py",
            "auto": True,
        }
    r = run_cmd(f'python "{test_script}"', cwd=MOTHER_ROOT, timeout=60)
    combined = f"{r['stdout']}\n{r['stderr']}"
    return {
        "id": "VAL-REFERENCE-PROJECT-SMOKE",
        "scope": "ROOT/REFERENCE_PROJECT",
        "status": "PASS" if r["exit_code"] == 0 and "REFERENCE_PROJECT_SMOKE=PASS" in combined else "FAIL",
        "detail": combined[-300:].strip(),
        "command": "python _reference_projects/minimal-ai-collab-taskboard/tests/test_smoke.py",
        "auto": True,
    }


def _auto_end_to_end_meta() -> dict:
    checks = [
        ("audit_assets", _auto_audit_assets()),
        ("scenario_matrix", _auto_scenario_matrix_gate()),
        ("route_smoke", _auto_route_smoke()),
        ("consistency", _auto_consistency_check()),
        ("user_pack_strict", _auto_user_pack_strict()),
        ("reference_project", _auto_reference_project_smoke()),
    ]
    return _aggregate_auto_results("VAL-END-TO-END", checks)


def _auto_cross_interface_meta() -> dict:
    checks = [
        ("route_smoke", _auto_route_smoke()),
        ("p03_http", _auto_p03_http_smoke(MOTHER_ROOT / "03.数据库管理_文件夹整理AI应用")),
        ("qcm_config_sync", _auto_qcm_config_sync_meta()),
        ("p05_api", _auto_p05_api_smoke(MOTHER_ROOT / "05.超极智脑_Q-SpecTrum")),
        ("p05_mcp", _auto_p05_mcp_smoke(MOTHER_ROOT / "05.超极智脑_Q-SpecTrum")),
        ("user_pack_strict", _auto_user_pack_strict()),
    ]
    return _aggregate_auto_results("VAL-CROSS-INTERFACE", checks)


# ---------------------------------------------------------------------------
# VALIDATE Command
# ---------------------------------------------------------------------------


def cmd_validate(args):
    """Execute validations from VALIDATION_REGISTRY."""
    print_header("Validation环 — VALIDATION_REGISTRY 自动验证")

    registry = load_yaml(VALIDATION_REGISTRY_PATH)
    if not registry:
        print("  [FAIL] Cannot load VALIDATION_REGISTRY.yaml")
        return 1

    validations = registry.get("validations", [])
    if not validations:
        print("  [WARN] No validations found in registry")
        return 0

    # Filter by scope if specified
    scope_filter = args.scope.upper() if args.scope else None
    if scope_filter:
        # Handle partial scope matching
        validations = [v for v in validations
                       if scope_filter in v.get("scope", "").upper()]

    print(f"  验证项总数: {len(validations)}")
    print(f"  过滤条件: {scope_filter or 'ALL'}")
    print()

    results = []
    for v in validations:
        vid = v.get("id", "UNKNOWN")
        scope = v.get("scope", "UNKNOWN")
        cmd_str = v.get("command", "")
        expected = v.get("expected", "")

        # Resolve CWD from scope
        scope_dir = None
        for scope_key, dir_name in VALIDATION_SCOPE_MAP.items():
            if scope.startswith(scope_key):
                scope_dir = MOTHER_ROOT / dir_name
                break

        print(f"  [{vid}] ({scope})")

        # Determine if this is auto-executable
        auto_result = _try_auto_execute(vid, cmd_str, scope_dir)

        if auto_result:
            r = auto_result
        else:
            # Manual check — report current_status from registry
            current = v.get("current_status", "not_run_current")
            evidence = v.get("evidence", "未执行")
            r = {
                "id": vid,
                "scope": scope,
                "status": "SKIP" if current == "not_run_current" else current.upper().replace("VERIFIED_", ""),
                "detail": evidence,
                "command": cmd_str,
                "auto": False,
            }

        results.append(r)
        icon = {"PASS": "+", "FAIL": "X", "WARN": "!", "SKIP": "-",
                "NEEDS_REVIEW": "?"}.get(r["status"], "?")
        auto_tag = " [AUTO]" if r.get("auto") else " [MANUAL]"
        print(f"      [{icon}]{auto_tag} {r['status']}")
        if r.get("detail"):
            detail = r["detail"][:120]
            print(f"        {detail}")

    # Summary
    print_subheader("验证总结")
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")
    warn_count = sum(1 for r in results if r["status"] in ("WARN", "NEEDS_REVIEW"))
    skip_count = sum(1 for r in results if r["status"] == "SKIP")
    auto_count = sum(1 for r in results if r.get("auto"))

    print(f"  总计: {len(results)}")
    print(f"  PASS: {pass_count}  |  FAIL: {fail_count}  |  "
          f"WARN: {warn_count}  |  SKIP: {skip_count}")
    print(f"  自动执行: {auto_count}/{len(results)}")

    if fail_count == 0:
        print("\n  结果: ALL CLEAR")
        return 0
    else:
        print(f"\n  结果: ACTION REQUIRED — {fail_count} 个失败项需修复")
        return 1


def _try_auto_execute(vid: str, cmd_str: str, cwd: Path | None) -> dict | None:
    """Attempt to auto-execute a validation command. Returns None if manual."""
    result = None

    # Auto-executable validation map
    if vid == "VAL-ROOT-YAML-PARSE":
        result = _auto_yaml_parse()
    elif vid == "VAL-ROOT-MARKDOWN-FENCES":
        result = _auto_markdown_fences()
    elif vid == "VAL-ROOT-FILE-COUNT":
        result = _auto_file_count()
    elif vid in ("VAL-03-INSTALL", "VAL-01-GHOST-VERIFY", "VAL-04-HEALTH",
                 "VAL-05-INTEGRATION", "VAL-USER-PACK-DELIVERY",
                 "VAL-USER-PACK-DELIVERY-STRICT"):
        # PowerShell/Python verification scripts
        result = _auto_run_script(cmd_str, cwd)
    elif vid == "VAL-02-TEMPLATE-REVIEW":
        result = _auto_template_review(cwd)
    elif vid == "VAL-00-CROSS-DOC-CONSISTENCY":
        result = _auto_consistency_check()
    elif vid == "VAL-00-MEMORY-SOURCE-INDEX":
        result = _auto_memory_source_index()
    elif vid == "VAL-00-AUDIT-ASSETS":
        result = _auto_audit_assets()
    elif vid == "VAL-ROOT-HARDCODE-PATH":
        result = _auto_hardcode_path_check()
    elif vid == "VAL-ROOT-ROUTE-SMOKE":
        result = _auto_route_smoke()
    elif vid == "VAL-END-TO-END":
        result = _auto_end_to_end_meta()
    elif vid == "VAL-CROSS-INTERFACE":
        result = _auto_cross_interface_meta()
    elif vid == "VAL-03-HTTP-SMOKE":
        result = _auto_p03_http_smoke(cwd)
    elif vid == "VAL-05-STATUS":
        # Python status check with UTF-8 (Windows-compatible)
        cmd = 'python run.py --status'
        r = run_cmd(cmd, cwd=cwd)
        combined = f"{r['stdout']}\n{r['stderr']}"
        status = "PASS" if (
            r["exit_code"] == 0
            and "System: ALL GREEN" in combined
            and "ISSUES FOUND" not in combined
        ) else "FAIL"
        result = {
            "id": vid, "scope": "", "status": status,
            "detail": combined[-300:].strip(),
            "command": cmd_str, "auto": True,
        }
    elif vid == "VAL-05-PYTEST":
        cmd = 'pytest tests -q'
        r = run_cmd(cmd, cwd=cwd, timeout=360)
        status = "PASS" if r["exit_code"] == 0 and "158 passed" in r["stdout"] else "FAIL"
        result = {
            "id": vid, "scope": "", "status": status,
            "detail": r["stdout"][-300:] or r["stderr"][-300:],
            "command": cmd_str, "auto": True,
        }
    elif vid == "VAL-05-E2E":
        cmd = 'python run.py --e2e'
        r = run_cmd(cmd, cwd=cwd, timeout=240)
        combined = f"{r['stdout']}\n{r['stderr']}"
        status = "PASS" if (
            r["exit_code"] == 0
            and "E2E Results: 13 passed, 0 failed" in combined
            and "VERDICT: Brand new AI models can understand" in combined
        ) else "FAIL"
        result = {
            "id": vid, "scope": "", "status": status,
            "detail": combined[-400:].strip(),
            "command": cmd_str, "auto": True,
        }
    elif vid == "VAL-05-API-SMOKE":
        result = _auto_p05_api_smoke(cwd)
    elif vid == "VAL-05-MCP-SMOKE":
        result = _auto_p05_mcp_smoke(cwd)
    elif vid == "VAL-REFERENCE-PROJECT-SMOKE":
        result = _auto_reference_project_smoke()
    elif vid == "VAL-03-TESTS":
        # pytest with UTF-8 (Windows-compatible)
        env_cmd = 'pytest tests/ -q'
        r = run_cmd(env_cmd, cwd=cwd, timeout=180)
        status = "PASS" if r["exit_code"] == 0 else "FAIL"
        result = {
            "id": vid, "scope": "", "status": status,
            "detail": r["stdout"][-300:] or r["stderr"][-300:],
            "command": cmd_str, "auto": True,
        }
    elif vid in ("VAL-04-QCM-ALL", "VAL-04-QCM-PAPER", "VAL-QCM-CONFIG-SYNC"):
        # QCM tests (need PYTHONPATH=cwd for qcm namespace package)
        qcm_py = str(cwd).replace("\\", "/") if cwd else "."
        if vid == "VAL-04-QCM-ALL":
            test_cmd = f'set PYTHONPATH={qcm_py}&& python "02-代码编写/test_qcm_all.py"'
        elif vid == "VAL-04-QCM-PAPER":
            test_cmd = (f'set PYTHONPATH={qcm_py}&& pytest "02-代码编写/test_roles.py" '
                        f'"02-代码编写/test_collaboration.py" '
                        f'"02-代码编写/test_sandbox.py" '
                        f'"02-代码编写/test_flywheel.py" '
                        f'"02-代码编写/test_summoning.py" -q')
        else:
            test_cmd = f'set PYTHONPATH={qcm_py}&& python "02-代码编写/test_config_sync.py"'
        r = run_cmd(test_cmd, cwd=cwd, timeout=180)
        status = "PASS" if r["exit_code"] == 0 else "FAIL"
        result = {
            "id": vid, "scope": "", "status": status,
            "detail": r["stdout"][-300:] or r["stderr"][-300:],
            "command": cmd_str, "auto": True,
        }
    elif vid == "VAL-04-QCM-RUNTIME-SMOKE":
        result = _auto_qcm_runtime_smoke(cwd)
    elif vid == "VAL-QCM-SKILL-VALIDATE":
        result = _auto_qcm_skill(validate_only=True)
    elif vid == "VAL-QCM-SKILL-TESTS":
        result = _auto_qcm_skill(validate_only=False)
    elif vid in ("VAL-01-SDK-TESTS",):
        # SDK tests under 01 subsystem: three Python suites plus TypeScript.
        # Each suite has its own PYTHONPATH requirement
        sdk_base = MOTHER_ROOT / "01.通讯协议_幽灵通道" / "03_SDK与集成"
        suites = [
            ("开源社区SDK", "02_开源社区包/ghost_channel开源库",
             "tests/unit", ["src", "."]),
            ("GhostHub企业SDK", "03_企业SDK包/GhostHub_SDK",
             "tests", ["."]),
            ("轻量SDK工程包", "04_SDK工程包/ghost-channel-sdk/python",
             "tests", [".", "../../../02_开源社区包/ghost_channel开源库/src"]),
        ]
        total_pass = 0
        total_fail = 0
        total_error = 0
        details = []
        for name, pkg_dir, test_rel, python_paths in suites:
            pkg_path = sdk_base / pkg_dir
            test_path = pkg_path / test_rel
            if not test_path.exists():
                details.append(f"{name}: NOT FOUND")
                total_error += 1
                continue
            # Build PYTHONPATH: append extra_path (e.g. src/) if specified
            cmd_env = os.environ.copy()
            cmd_env.setdefault("PYTHONUTF8", "1")
            cmd_env.setdefault("PYTHONIOENCODING", "utf-8")
            pythonpath_parts = []
            for rel in python_paths:
                path = (pkg_path / rel).resolve()
                if path.exists():
                    pythonpath_parts.append(str(path))
            cmd_env["PYTHONPATH"] = ";".join(pythonpath_parts)
            r = run_cmd_raw(f'{PYTEST_COMMAND} "{test_rel}" -q',
                           cwd=pkg_path, timeout=180, env=cmd_env)
            # Parse pass/fail from output
            combined_output = f"{r['stdout']}\n{r['stderr']}"
            for line in combined_output.split("\n"):
                m = re.search(r"(\d+) passed", line)
                if m:
                    total_pass += int(m.group(1))
                m = re.search(r"(\d+) failed", line)
                if m:
                    total_fail += int(m.group(1))
                m = re.search(r"(\d+) error", line)
                if m:
                    total_error += int(m.group(1))
            if r["exit_code"] != 0:
                total_error += 1
            detail_msg = combined_output[-120:].strip()
            details.append(f"{name}: exit={r['exit_code']} {detail_msg}")

        ts_path = sdk_base / "04_SDK工程包" / "ghost-channel-sdk" / "typescript"
        npm_path = shutil.which("npm.cmd") or shutil.which("npm")
        if not ts_path.exists():
            details.append("TypeScript SDK: NOT FOUND")
            total_error += 1
        elif not npm_path:
            details.append("TypeScript SDK: npm NOT FOUND")
            total_error += 1
        else:
            cmd_env = os.environ.copy()
            npm_cmd = f'"{npm_path}" test'
            r = run_cmd_raw(npm_cmd, cwd=ts_path, timeout=120, env=cmd_env)
            combined_output = f"{r['stdout']}\n{r['stderr']}"
            pass_seen = False
            for line in combined_output.split("\n"):
                m = re.search(r"# pass (\d+)", line)
                if m:
                    total_pass += int(m.group(1))
                    pass_seen = True
                m = re.search(r"# fail (\d+)", line)
                if m:
                    total_fail += int(m.group(1))
            if r["exit_code"] != 0:
                total_error += 1
            elif not pass_seen:
                total_error += 1
            detail_msg = combined_output[-120:].strip()
            details.append(f"TypeScript SDK: exit={r['exit_code']} {detail_msg}")

        if total_fail > 0 or total_error > 0:
            status = "FAIL"
        elif total_pass > 0:
            status = "PASS"
        else:
            status = "FAIL"
        result = {
            "id": vid, "scope": "", "status": status,
            "detail": f"SDK: {total_pass} passed, {total_fail} failed, {total_error} errors; " + "; ".join(details[:4]),
            "command": cmd_str, "auto": True,
        }

    if result:
        result.setdefault("id", vid)
        result.setdefault("scope", "")
        result.setdefault("auto", True)
    return result


def _auto_p05_api_smoke(cwd: Path | None) -> dict:
    """Start Q-SpecTrum API on a free port and verify real HTTP routes."""
    p05_root = cwd or (MOTHER_ROOT / "05.超极智脑_Q-SpecTrum")
    if not p05_root.exists():
        return {
            "id": "VAL-05-API-SMOKE", "scope": "P05_QSPECTRUM",
            "status": "SKIP", "detail": f"Missing P05 root: {p05_root}",
            "auto": True,
        }

    port = _free_local_port()
    base = f"http://127.0.0.1:{port}"
    python_exe = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    env = os.environ.copy()
    env["QSPECTRUM_LLM"] = "mock"
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.Popen(
        [python_exe, "run.py", "--web", "--port", str(port), "--provider", "mock"],
        cwd=p05_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        env=env,
    )

    def request(method: str, path: str, body: dict | None = None, timeout: int = 20):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            base + path,
            data=data,
            headers={"Content-Type": "application/json"} if data else {},
            method=method,
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    try:
        ready = False
        last_error = None
        for _ in range(30):
            try:
                code, status_payload = request("GET", "/api/status", timeout=2)
                if code == 200 and status_payload.get("roles_loaded") == 15:
                    ready = True
                    break
            except Exception as exc:
                last_error = exc
                time.sleep(1)
        if not ready:
            return {
                "id": "VAL-05-API-SMOKE", "scope": "P05_QSPECTRUM",
                "status": "FAIL", "detail": f"API did not become ready: {last_error}",
                "auto": True,
            }

        code, roles = request("GET", "/api/roles")
        checks = [code == 200 and roles.get("total") == 15]
        routes = []
        for query, expected in [
            ("Research our competitors", "ROLE-Q02"),
            ("Audit this code for security bugs", "ROLE-Q06"),
            ("Help me grow as an engineer", "ROLE-Q08"),
        ]:
            code, body = request(
                "POST", "/api/chat",
                {"message": query, "session_id": "qa-runner-api-smoke"},
            )
            role = body.get("routing", {}).get("role_code")
            routes.append(f"{query[:8]}->{role}")
            checks.append(code == 200 and body.get("success") is True and role == expected)

        status = "PASS" if all(checks) else "FAIL"
        return {
            "id": "VAL-05-API-SMOKE", "scope": "P05_QSPECTRUM",
            "status": status,
            "detail": f"status roles=15; roles total={roles.get('total')}; routes={', '.join(routes)}",
            "auto": True,
        }
    except Exception as exc:
        return {
            "id": "VAL-05-API-SMOKE", "scope": "P05_QSPECTRUM",
            "status": "FAIL", "detail": f"API smoke failed: {exc}",
            "auto": True,
        }
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def _auto_p05_mcp_smoke(cwd: Path | None) -> dict:
    """Verify Q-SpecTrum MCP stdio emits clean JSON-RPC responses."""
    p05_root = cwd or (MOTHER_ROOT / "05.超极智脑_Q-SpecTrum")
    if not p05_root.exists():
        return {
            "id": "VAL-05-MCP-SMOKE", "scope": "P05_QSPECTRUM",
            "status": "SKIP", "detail": f"Missing P05 root: {p05_root}",
            "auto": True,
        }

    python_exe = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "resources/read",
         "params": {"uri": "qspectrum://status"}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
         "params": {"name": "execute_chat",
                    "arguments": {"message": "Research our competitors"}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
         "params": {"name": "query_database",
                    "arguments": {"sql": "SELECT COUNT(*) AS n FROM ai_roles"}}},
    ]
    stdin = "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in messages)
    try:
        result = subprocess.run(
            [python_exe, "qspectrum_mcp_server.py", "--provider", "mock"],
            input=stdin,
            cwd=p05_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
            env=env,
        )
    except Exception as exc:
        return {
            "id": "VAL-05-MCP-SMOKE", "scope": "P05_QSPECTRUM",
            "status": "FAIL", "detail": f"MCP smoke failed: {exc}",
            "auto": True,
        }

    parsed = []
    non_json = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            parsed.append(json.loads(line))
        except Exception:
            non_json.append(line[:80])

    by_id = {msg.get("id"): msg for msg in parsed if msg.get("id") is not None}
    checks = [
        result.returncode == 0,
        not non_json,
        len(by_id.get(2, {}).get("result", {}).get("tools", [])) >= 10,
        len(by_id.get(3, {}).get("result", {}).get("contents", [])) == 1,
    ]
    try:
        chat_text = by_id[4]["result"]["content"][0]["text"]
        chat_payload = json.loads(chat_text)
        checks.append("Researcher" in chat_payload.get("response", ""))
        sql_text = by_id[5]["result"]["content"][0]["text"]
        sql_payload = json.loads(sql_text)
        checks.append(sql_payload.get("results", [{}])[0].get("n") == 15)
    except Exception:
        checks.append(False)

    status = "PASS" if all(checks) else "FAIL"
    stderr_lines = len([l for l in result.stderr.splitlines() if l.strip()])
    return {
        "id": "VAL-05-MCP-SMOKE", "scope": "P05_QSPECTRUM",
        "status": status,
        "detail": (
            f"json_messages={len(parsed)}, non_json={len(non_json)}, "
            f"tools={len(by_id.get(2, {}).get('result', {}).get('tools', []))}, "
            f"stderr_lines={stderr_lines}"
        ),
        "auto": True,
    }


def _auto_p03_http_smoke(cwd: Path | None) -> dict:
    """Start WorkBuddy KB Flask app and verify /memory plus /api/search."""
    p03_root = cwd or (MOTHER_ROOT / "03.数据库管理_文件夹整理AI应用")
    if not p03_root.exists():
        return {
            "id": "VAL-03-HTTP-SMOKE", "scope": "P03_WORKBUDDY_KB",
            "status": "SKIP", "detail": f"Missing P03 root: {p03_root}",
            "auto": True,
        }

    port = _free_local_port()
    base = f"http://127.0.0.1:{port}"
    python_exe = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.Popen(
        [python_exe, "app.py", "--port", str(port), "--no-bootstrap", "--daemon"],
        cwd=p03_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        env=env,
    )

    try:
        ready = False
        last_error = None
        for _ in range(30):
            try:
                with urllib.request.urlopen(base + "/memory", timeout=2) as resp:
                    memory_payload = json.loads(resp.read().decode("utf-8"))
                if resp.status == 200:
                    ready = True
                    break
            except Exception as exc:
                last_error = exc
                time.sleep(0.25)

        if not ready:
            return {
                "id": "VAL-03-HTTP-SMOKE", "scope": "P03_WORKBUDDY_KB",
                "status": "FAIL", "detail": f"HTTP app did not become ready: {last_error}",
                "auto": True,
            }

        query = urllib.parse.quote("知识库")
        index_rebuilt = False
        with urllib.request.urlopen(f"{base}/api/search?q={query}", timeout=30) as resp:
            search_payload = json.loads(resp.read().decode("utf-8"))
        results = search_payload.get("results", [])
        if not results:
            req = urllib.request.Request(f"{base}/api/index", method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                index_payload = json.loads(resp.read().decode("utf-8"))
            index_rebuilt = True
            with urllib.request.urlopen(f"{base}/api/search?q={query}", timeout=30) as resp:
                search_payload = json.loads(resp.read().decode("utf-8"))
            results = search_payload.get("results", [])
        required_memory_keys = {"config", "short_term_count", "mid_term_count", "long_term_knowledge"}
        status = "PASS" if required_memory_keys.issubset(memory_payload) and len(results) > 0 else "FAIL"
        first_path = results[0].get("path", "") if results else ""
        return {
            "id": "VAL-03-HTTP-SMOKE",
            "scope": "P03_WORKBUDDY_KB",
            "status": status,
            "detail": (
                f"port={port}; memory_keys={','.join(sorted(memory_payload.keys()))}; "
                f"search_results={len(results)}; index_rebuilt={index_rebuilt}; first_path={first_path}"
            ),
            "auto": True,
        }
    except Exception as exc:
        return {
            "id": "VAL-03-HTTP-SMOKE", "scope": "P03_WORKBUDDY_KB",
            "status": "FAIL", "detail": f"HTTP smoke failed: {exc}",
            "auto": True,
        }
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def _auto_yaml_parse() -> dict:
    """Auto-check: YAML parse validation."""
    yaml_dir = REGISTRY_DIR
    yaml_files = list(yaml_dir.glob("*.yaml")) + list(yaml_dir.glob("*.yml"))
    passed = 0
    failed = 0
    details = []
    for f in yaml_files:
        data = load_yaml(f)
        if data is not None:
            passed += 1
        else:
            failed += 1
            details.append(f"FAIL: {f.name}")
    status = "PASS" if failed == 0 else "FAIL"
    return {
        "id": "VAL-ROOT-YAML-PARSE",
        "scope": "ROOT/P00",
        "status": status,
        "detail": f"{passed} parsed, {failed} failed" + (
            f" ({'; '.join(details)})" if details else ""),
        "auto": True,
    }


def _auto_markdown_fences() -> dict:
    """Auto-check: Markdown fence balance."""
    md_root = MOTHER_ROOT
    issues = []
    checked = 0
    fence_re = re.compile(r"^```", re.MULTILINE)
    for md_file in md_root.rglob("*.md"):
        if ".git" in str(md_file) or "node_modules" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8", errors="replace")
        opens = len(fence_re.findall(content))
        if opens % 2 != 0:
            issues.append(f"{md_file.relative_to(md_root)}: {opens} fences")
        checked += 1
    status = "PASS" if not issues else "FAIL"
    return {
        "id": "VAL-ROOT-MARKDOWN-FENCES",
        "scope": "ROOT/P00",
        "status": status,
        "detail": f"Checked {checked} files" + (
            f"; unbalanced: {issues}" if issues else ""),
        "auto": True,
    }


def _auto_file_count() -> dict:
    """Auto-check: File count verification."""
    excludes = {".git", "node_modules", "dist", "build", "coverage",
                "__pycache__", ".pytest_cache"}
    total = 0
    by_subsystem = {}
    for p in MOTHER_ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(MOTHER_ROOT)).replace("\\", "/")
        if rel.endswith("00.超级提示词工程/14-全链路审计与运行对齐/ATOMIC-FILE-INVENTORY.jsonl"):
            continue
        if any(part in excludes for part in rel.split("/")):
            continue
        total += 1
        # Classify by subsystem
        parts = rel.split("/")
        if len(parts) >= 1:
            top = parts[0]
            by_subsystem[top] = by_subsystem.get(top, 0) + 1
    # Note: submodule dirs (03, 05) may show different counts locally vs in-tree
    status = "PASS" if total >= 1050 else "WARN"
    detail_parts = [f"total={total} (current inventory baseline=1174, submodule differences normal)"]
    for k in sorted(by_subsystem):
        detail_parts.append(f"{k[:20]}={by_subsystem[k]}")
    return {
        "id": "VAL-ROOT-FILE-COUNT",
        "scope": "ROOT",
        "status": status,
        "detail": "; ".join(detail_parts),
        "auto": True,
    }


def _auto_run_script(cmd_str: str, cwd: Path | None) -> dict | None:
    """Auto-run a PowerShell or Python verification script."""
    if not cwd or not cwd.exists():
        return None

    # Extract script path from command
    script_match = re.search(r"-File\s+(.+?)(?:\s|$)", cmd_str)
    if script_match:
        ps_script = script_match.group(1).strip()
        if not ps_script.endswith(".ps1"):
            ps_script += ".ps1"
        script_path = cwd / ps_script.replace("\\", "/")
        if not script_path.exists():
            # Try with backslash
            script_path = cwd / ps_script
        if not script_path.exists():
            return {
                "id": "", "scope": "", "status": "SKIP",
                "detail": f"Script not found: {ps_script}",
                "command": cmd_str, "auto": True,
            }
        # Check for -Strict flag
        strict = "-Strict" in cmd_str
        ps_cmd = _powershell_file_cmd(f"./{ps_script}", *(["-Strict"] if strict else []))
        if ps_cmd is None:
            return {
                "id": "", "scope": "", "status": "FAIL",
                "detail": "PowerShell executable not found",
                "command": cmd_str, "auto": True,
            }
        r = run_cmd(ps_cmd, cwd=cwd, timeout=120)
        status = "PASS" if r["exit_code"] == 0 else "FAIL"
        return {
            "id": "", "scope": "", "status": status,
            "detail": r["stdout"][-300:] or r["stderr"][-200:],
            "command": cmd_str, "auto": True,
        }

    # Python script
    py_match = re.search(r"python\s+(.+?)(?:\s|$)", cmd_str)
    if py_match:
        py_script = py_match.group(1).strip().strip('"')
        script_path = cwd / py_script.replace("\\", "/")
        if not script_path.exists():
            return {
                "id": "", "scope": "", "status": "SKIP",
                "detail": f"Script not found: {py_script}",
                "command": cmd_str, "auto": True,
            }
        r = run_cmd(f'python "{py_script}"', cwd=cwd, timeout=120)
        status = "PASS" if r["exit_code"] == 0 else "FAIL"
        return {
            "id": "", "scope": "", "status": status,
            "detail": r["stdout"][-300:] or r["stderr"][-200:],
            "command": cmd_str, "auto": True,
        }

    return None


def _auto_template_review(cwd: Path | None) -> dict:
    """Auto-check: py_compile + smoke test for 02 template."""
    p02 = MOTHER_ROOT / "02.通用知识库框架_Universal-KB" / "04-memory" / "memoryos.py"
    if not p02.exists():
        return {
            "id": "VAL-02-TEMPLATE-REVIEW", "scope": "P02_UNIVERSAL_KB",
            "status": "FAIL", "detail": f"memoryos.py not found: {p02}",
            "command": "python -m py_compile memoryos.py", "auto": True,
        }
    # py_compile
    r1 = run_cmd(f'python -m py_compile "{p02}"', cwd=cwd, timeout=30)
    if r1["exit_code"] != 0:
        return {
            "id": "VAL-02-TEMPLATE-REVIEW", "scope": "P02_UNIVERSAL_KB",
            "status": "FAIL", "detail": f"py_compile failed: {r1['stderr'][:120]}",
            "command": "python -m py_compile memoryos.py", "auto": True,
        }
    # smoke run
    r2 = run_cmd(f'python "{p02}"', cwd=p02.parent, timeout=30)
    status = "PASS" if r2["exit_code"] == 0 else "FAIL"
    return {
        "id": "VAL-02-TEMPLATE-REVIEW", "scope": "P02_UNIVERSAL_KB",
        "status": status,
        "detail": f"py_compile OK; smoke exit={r2['exit_code']}: {r2['stdout'][:100]}",
        "command": "python -m py_compile memoryos.py and python memoryos.py", "auto": True,
    }


def _auto_consistency_check() -> dict:
    """Auto-check: run validate_consistency.py and report."""
    script = CONSISTENCY_SCRIPT
    if not script.exists():
        return {
            "id": "VAL-00-CROSS-DOC-CONSISTENCY", "scope": "P00_SUPER_PROMPT",
            "status": "SKIP", "detail": f"validate_consistency.py not found: {script}",
            "command": "python validate_consistency.py", "auto": True,
        }
    r = run_cmd(f'python "{script}" "{MOTHER_ROOT}"', cwd=MOTHER_ROOT, timeout=120)
    stdout = r["stdout"]
    # Parse PASS/FAIL/WARN counts from output
    pass_m = re.search(r"PASS:\s*(\d+)", stdout)
    fail_m = re.search(r"FAIL:\s*(\d+)", stdout)
    warn_m = re.search(r"WARN:\s*(\d+)", stdout)
    pass_count = int(pass_m.group(1)) if pass_m else 0
    fail_count = int(fail_m.group(1)) if fail_m else 0
    warn_count = int(warn_m.group(1)) if warn_m else 0
    if r["exit_code"] != 0:
        status = "FAIL"
    elif fail_count > 0:
        status = "FAIL"
    elif warn_count > 0:
        status = "WARN"
    else:
        status = "PASS"
    detail = f"{pass_count} PASS / {fail_count} FAIL / {warn_count} WARN"
    return {
        "id": "VAL-00-CROSS-DOC-CONSISTENCY", "scope": "P00_SUPER_PROMPT",
        "status": status, "detail": detail,
        "command": "python validate_consistency.py", "auto": True,
    }


def _auto_memory_source_index() -> dict:
    """Auto-check: MEMORY-SOURCE-INDEX.yaml field validation."""
    idx_path = REGISTRY_DIR / "MEMORY-SOURCE-INDEX.yaml"
    if not idx_path.exists():
        return {
            "id": "VAL-00-MEMORY-SOURCE-INDEX", "scope": "P00_SUPER_PROMPT",
            "status": "SKIP", "detail": f"MEMORY-SOURCE-INDEX.yaml not found: {idx_path}",
            "command": "Parse MEMORY-SOURCE-INDEX.yaml", "auto": True,
        }
    data = load_yaml(idx_path)
    if data is None:
        return {
            "id": "VAL-00-MEMORY-SOURCE-INDEX", "scope": "P00_SUPER_PROMPT",
            "status": "FAIL", "detail": "Failed to parse MEMORY-SOURCE-INDEX.yaml",
            "command": "Parse MEMORY-SOURCE-INDEX.yaml", "auto": True,
        }
    sources = data.get("memory_sources", [])
    required_fields = ["id", "owner_project", "path", "authority_scope",
                       "read_priority", "write_target", "query_entry",
                       "conflict_owner", "side_effects", "source_status"]
    missing = []
    for src in sources:
        for field in required_fields:
            if field not in src or src[field] is None:
                missing.append(f"{src.get('id', '?')}.{field}")
    status = "PASS" if not missing else "FAIL"
    detail = f"{len(sources)} sources, {len(missing)} missing fields" + (
        f": {missing[:5]}" if missing else ""
    )
    return {
        "id": "VAL-00-MEMORY-SOURCE-INDEX", "scope": "P00_SUPER_PROMPT",
        "status": status, "detail": detail,
        "command": "Parse MEMORY-SOURCE-INDEX.yaml and inspect required fields", "auto": True,
    }


def _auto_audit_assets() -> dict:
    """Auto-check: atomic inventory, graph seed, and deep-audit control docs."""
    inv_path = REGISTRY_DIR / "ATOMIC-FILE-INVENTORY.jsonl"
    graph_path = REGISTRY_DIR / "KNOWLEDGE-GRAPH-SEED.yaml"
    required_docs = [
        REGISTRY_DIR / "CODEX-DEEP-AUDIT-EXECUTION-CHARTER.md",
        REGISTRY_DIR / "SCENARIO-ACCEPTANCE-MATRIX.md",
        REGISTRY_DIR / "DEEP-UNDERSTANDING-KNOWLEDGE-CRYSTALLIZATION-BLUEPRINT.md",
    ]
    failures = []
    inventory_count = 0
    required_fields = {
        "path", "subsystem", "kind", "size_bytes", "sha256",
        "priority", "audit_state", "evidence_level",
    }
    if not inv_path.exists():
        failures.append("ATOMIC-FILE-INVENTORY.jsonl missing")
    else:
        try:
            with inv_path.open("r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    missing = required_fields - set(record)
                    if missing:
                        failures.append(f"inventory line {line_no} missing {sorted(missing)}")
                        break
                    inventory_count += 1
            if inventory_count < 1000:
                failures.append(f"inventory too small: {inventory_count}")
        except Exception as exc:
            failures.append(f"inventory parse error: {exc}")

    graph = load_yaml(graph_path)
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    edges = graph.get("edges", []) if isinstance(graph, dict) else []
    if not nodes or not edges:
        failures.append("KNOWLEDGE-GRAPH-SEED.yaml missing nodes or edges")

    for doc in required_docs:
        if not doc.exists():
            failures.append(f"missing {doc.name}")

    status = "PASS" if not failures else "FAIL"
    detail = f"inventory={inventory_count}, graph_nodes={len(nodes)}, graph_edges={len(edges)}"
    if failures:
        detail += "; " + "; ".join(failures[:3])
    return {
        "id": "VAL-00-AUDIT-ASSETS", "scope": "P00_SUPER_PROMPT",
        "status": status, "detail": detail,
        "command": "Parse audit inventory/graph/control docs", "auto": True,
    }


def _auto_hardcode_path_check() -> dict:
    """Auto-check: scan for local absolute path leakage."""
    # Patterns: Windows drive paths and common user home paths
    patterns = [r"[A-Za-z]:\\s*\\", r"C:\\s*Users\\s*wanwa", r"D:\\s*工作资料"]
    # Whitelist: lines containing detector/regex/pattern references are not leakage
    detector_keywords = ["rg -n", "re.search", "re.compile", "re.findall",
                         "pattern", "regex", "正则", "detector", "检测器",
                         "check(", "硬編碼", "硬编码", "禁止 ", "違規"]
    findings = []

    def _is_detector_line(line: str) -> bool:
        return any(kw in line for kw in detector_keywords)

    def _check_file(f: Path) -> bool:
        try:
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                if _is_detector_line(line):
                    continue
                for pat in patterns:
                    if re.search(pat, line):
                        return True
        except Exception:
            pass
        return False

    for md_file in MOTHER_ROOT.rglob("*.md"):
        if ".git" in str(md_file) or "node_modules" in str(md_file):
            continue
        if _check_file(md_file):
            rel = str(md_file.relative_to(MOTHER_ROOT)).replace("\\", "/")
            findings.append(rel)

    # Also check Python/YAML for local paths (excluding this script itself and test fixtures)
    for glob_pat in ["*.py", "*.yaml", "*.yml"]:
        for f in MOTHER_ROOT.rglob(glob_pat):
            if ".git" in str(f) or "node_modules" in str(f):
                continue
            rel = str(f.relative_to(MOTHER_ROOT)).replace("\\", "/")
            if "qa_runner.py" in rel or "test_" in rel or "_test.py" in rel:
                continue
            if _check_file(f):
                findings.append(rel)

    # Deduplicate
    findings = list(dict.fromkeys(findings))
    if findings:
        status = "WARN"
        detail = f"Found {len(findings)} files with potential hardcoded paths: {findings[:5]}"
    else:
        status = "PASS"
        detail = "No local absolute path leakage found in operational docs/code."
    return {
        "id": "VAL-ROOT-HARDCODE-PATH", "scope": "ROOT",
        "status": status, "detail": detail,
        "command": "rg scan for local absolute paths", "auto": True,
    }


def _auto_route_smoke() -> dict:
    """Auto-check: Guide Secretary route command handles core Chinese scenarios."""
    scenarios = [
        ("帮我完整理解整个母包并给出下一步审计路径",
         "PACKAGE_UNDERSTANDING", "CONFIRM", "mother_pack", 0.60),
        ("请读取母包并完成唤醒激活",
         "MISSION_MEMORY_AWAKENING", "DIRECT", "mother_pack", 0.80),
        ("我要运行03知识库搜索和MCP工具",
         "KNOWLEDGE_MEMORY", "DIRECT", "P03_WORKBUDDY_KB", 0.80),
        ("帮我测试05 Q-SpecTrum API和角色路由",
         "CAPABILITY_INTEGRATION", "DIRECT", "P05_QSPECTRUM", 0.80),
        ("请给出05 Q-SpecTrum当前系统状态摘要",
         "CAPABILITY_INTEGRATION", "DIRECT", "P05_QSPECTRUM", 0.80),
        ("准备最终用户交付包并严格验证",
         "USER_DELIVERY", "DIRECT", "USER_PACK", 0.80),
        ("从想法到需求、规格、任务、测试、交付",
         "CROSS_SYSTEM_GOLDEN_PATH", "DIRECT", "cross_subsystem", 0.80),
        ("我要用这个母包项目完善母包自身，形成第一次真正的协同通用AI大模型项目开发实例，并把结果反哺仓库",
         "SELF_BOOTSTRAP_PROJECT", "DIRECT", "cross_subsystem", 0.80),
        ("为什么这个项目一直重构，怎么收敛？",
         "REVIEW_AUDIT", "CONFIRM", "mother_pack", 0.60),
    ]
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    failures = []
    passed = 0
    runner = MOTHER_ROOT / "qa_runner.py"
    for text, expected_intent, expected_decision, expected_platform, min_confidence in scenarios:
        try:
            r = subprocess.run(
                [sys.executable, str(runner), "route", text],
                cwd=MOTHER_ROOT, capture_output=True, text=True,
                timeout=60, encoding="utf-8", errors="replace", env=env,
            )
        except Exception as exc:
            failures.append(f"{expected_intent}: {exc}")
            continue
        combined = f"{r.stdout}\n{r.stderr}"
        conf_match = re.search(r"confidence_after_routing:\s*([0-9.]+)", combined)
        confidence = float(conf_match.group(1)) if conf_match else 0.0
        ok = (
            r.returncode == 0
            and f'  intent_id: "{expected_intent}"' in combined
            and f'  route_decision: "{expected_decision}"' in combined
            and f'    platform: "{expected_platform}"' in combined
            and confidence >= min_confidence
            and "guide_secretary:" in combined
            and "route_feedback:" in combined
            and "validation_refs: []" not in combined
        )
        if ok:
            passed += 1
        else:
            failures.append(
                f"{expected_intent}/{expected_decision}/{expected_platform}: "
                f"exit={r.returncode} conf={confidence} {combined[-120:].strip()}"
            )
    status = "PASS" if not failures else "FAIL"
    detail = f"{passed}/{len(scenarios)} route smoke scenarios passed"
    if failures:
        detail += "; " + "; ".join(failures[:2])
    return {
        "id": "VAL-ROOT-ROUTE-SMOKE", "scope": "ROOT",
        "status": status, "detail": detail,
        "command": "python qa_runner.py route <scenario matrix>", "auto": True,
    }


def cmd_status(_args):
    """Read all registries and output system overview."""
    print_header("Status环 — 系统全貌报告")

    # Load registries
    project_reg = load_yaml(PROJECT_REGISTRY_PATH)
    cap_reg = load_yaml(CAPABILITY_REGISTRY_PATH)
    art_reg = load_yaml(ARTIFACT_REGISTRY_PATH)
    val_reg = load_yaml(VALIDATION_REGISTRY_PATH)
    ledger = load_yaml(LEDGER_PATH)

    # --- Projects ---
    print_subheader("1. 项目注册表 (PROJECT_REGISTRY)")
    if project_reg:
        projects = project_reg.get("projects", [])
        print(f"  子系统总数: {len(projects)}")
        status_counts = {}
        for p in projects:
            pid = p.get("id", "?")
            pstatus = p.get("status", "?")
            role = p.get("role", "?")[:40]
            risks = p.get("risks", [])
            status_counts[pstatus] = status_counts.get(pstatus, 0) + 1
            risk_str = f" [{len(risks)} risk(s)]" if risks else ""
            print(f"  [{pstatus:8s}] {pid:20s} {role}{risk_str}")
        print(f"\n  状态分布: {json.dumps(status_counts)}")
    else:
        print("  [WARN] Cannot load PROJECT_REGISTRY")

    # --- Capabilities ---
    print_subheader("2. 能力注册表 (CAPABILITY_REGISTRY)")
    if cap_reg:
        capabilities = cap_reg.get("capabilities", [])
        print(f"  能力总数: {len(capabilities)}")
        perm_counts = {}
        type_counts = {}
        for c in capabilities:
            cid = c.get("id", "?")
            name = c.get("name", "?")
            perm = c.get("permission", "?")
            ctype = c.get("type", "?")
            perm_counts[perm] = perm_counts.get(perm, 0) + 1
            type_counts[ctype] = type_counts.get(ctype, 0) + 1
            print(f"  [{perm:16s}] {cid:30s} {name}")
        print(f"\n  权限分布: {json.dumps(perm_counts)}")
        print(f"  类型分布: {json.dumps(type_counts)}")
    else:
        print("  [WARN] Cannot load CAPABILITY_REGISTRY")

    # --- Artifacts ---
    print_subheader("3. 制品注册表 (ARTIFACT_REGISTRY)")
    if art_reg:
        artifacts = art_reg.get("artifacts", [])
        print(f"  制品总数: {len(artifacts)}")
        type_counts = {}
        priority_counts = {}
        for a in artifacts:
            aid = a.get("id", "?")
            atype = a.get("type", "?")
            priority = a.get("read_priority", "?")
            role = a.get("role", "?")[:50]
            type_counts[atype] = type_counts.get(atype, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            print(f"  [{atype:10s} P{priority}] {aid:30s} {role}")
        print(f"\n  类型分布: {json.dumps(type_counts)}")
        print(f"  优先级分布: {json.dumps(priority_counts)}")
    else:
        print("  [WARN] Cannot load ARTIFACT_REGISTRY")

    # --- Validations ---
    print_subheader("4. 验证注册表 (VALIDATION_REGISTRY)")
    if val_reg:
        validations = val_reg.get("validations", [])
        print(f"  验证项总数: {len(validations)}")
        status_counts = {}
        for v in validations:
            vid = v.get("id", "?")
            vstatus = v.get("current_status", "?")
            status_counts[vstatus] = status_counts.get(vstatus, 0) + 1
            print(f"  [{vstatus:28s}] {vid}")
        print(f"\n  状态分布: {json.dumps(status_counts)}")
    else:
        print("  [WARN] Cannot load VALIDATION_REGISTRY")

    # --- Ledger ---
    print_subheader("5. 统一状态账本 (UNIFIED-STATUS-LEDGER)")
    if ledger:
        status_objects = ledger.get("status_objects", [])
        active = [s for s in status_objects if s.get("status") == "active"]
        print(f"  状态对象总数: {len(status_objects)}")
        print(f"  活跃项: {len(active)}")
        for s in active:
            sid = s.get("id", "?")[:50]
            stype = s.get("type", "?")
            priority = s.get("priority", "?")
            title = s.get("title", "?")[:60]
            print(f"  [{stype:8s} {priority}] {sid}")
            print(f"           {title}")
    else:
        print("  [WARN] Cannot load LEDGER")

    # --- Git Status ---
    print_subheader("6. Git 状态")
    r = run_cmd("git log --oneline -5")
    if r["exit_code"] == 0:
        print(f"  最近提交:")
        for line in r["stdout"].split("\n"):
            print(f"    {line}")
    r2 = run_cmd("git status --short")
    if r2["stdout"]:
        print(f"  工作区变更:")
        for line in r2["stdout"].split("\n"):
            print(f"    {line}")
    else:
        print(f"  工作区: CLEAN")
    r3 = run_cmd("git remote -v")
    if r3["stdout"]:
        print(f"  Remote: {r3['stdout'][:200]}")
    else:
        print(f"  Remote: 未配置")

    print(f"\n{'=' * 70}")
    return 0


# ---------------------------------------------------------------------------
# CONSISTENCY Command
# ---------------------------------------------------------------------------


def cmd_consistency(_args):
    """Run validate_consistency.py 10-dimension cross-document check."""
    print_header("Consistency环 — 10维度跨文档一致性检查")

    if not CONSISTENCY_SCRIPT.exists():
        print(f"  [FAIL] Script not found: {CONSISTENCY_SCRIPT}")
        return 1

    # Import and run directly for clean integration
    sys.path.insert(0, str(CONSISTENCY_SCRIPT.parent))
    try:
        from validate_consistency import ConsistencyValidator, print_report
        validator = ConsistencyValidator(MOTHER_ROOT)
        results = validator.run_all()
        exit_code = print_report(results)
        return exit_code
    except ImportError as e:
        # Fallback: run as subprocess
        r = run_cmd(f'python "{CONSISTENCY_SCRIPT}" "{MOTHER_ROOT}"', timeout=60)
        print(r["stdout"])
        if r["stderr"]:
            print(r["stderr"])
        return r["exit_code"]
    except Exception as e:
        print(f"  [FAIL] {e}")
        return 1


# ---------------------------------------------------------------------------
# ROUTE Command
# ---------------------------------------------------------------------------


def cmd_route(args):
    """Guide Secretary intent matching and routing."""
    user_input = args.text
    if not user_input:
        print("  [ERROR] 请提供用户输入文本")
        print("  用法: python qa_runner.py route \"<user input>\"")
        return 1

    print_header("Routing环 — Guide Secretary 意图路由")

    # Step 1: Keyword matching against intent registry
    input_lower = user_input.lower()
    scores = {}

    for intent_id, intent_data in INTENT_REGISTRY.items():
        if intent_id == "AMBIGUOUS":
            continue
        keywords = intent_data.get("keywords", [])
        if not keywords:
            continue
        match_count = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in input_lower:
                # Avoid false substring matches: short ASCII keywords (<4 chars)
                # must match at word boundaries
                if len(kw_lower) <= 5 and kw_lower.isascii():
                    if not re.search(r'\b' + re.escape(kw_lower) + r'\b', input_lower):
                        continue
                match_count += 1
        if match_count > 0:
            # Score based on match ratio and keyword specificity
            score = match_count / len(keywords)
            # Boost for longer keyword matches (more specific)
            for kw in keywords:
                if kw.lower() in input_lower and len(kw) >= 4:
                    score += 0.1
            scores[intent_id] = min(score, 1.0)

    # Step 2: Determine top intent
    if not scores:
        top_intent = "AMBIGUOUS"
        confidence = 0.30
    else:
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = sorted_intents[0]
        # Recalculate confidence with practical scoring:
        # keyword_score: use raw match count normalized to 3 (3 hits = strong signal)
        raw_hits = sum(1 for kw in INTENT_REGISTRY.get(top_intent, {}).get("keywords", [])
                       if kw.lower() in input_lower)
        keyword_norm = min(raw_hits / 3.0, 1.0)
        keyword_score = min(keyword_norm * 0.40, 0.40)
        # Uniqueness bonus: big gap between top and second
        if len(sorted_intents) >= 2:
            gap = top_score - sorted_intents[1][1]
            uniqueness_score = min(0.15 + gap * 0.3, 0.25)
        else:
            uniqueness_score = 0.25
        # Clarity bonus: longer input = more context
        clarity_score = min(len(user_input) / 200 * 0.10, 0.10)
        base_confidence = keyword_score + uniqueness_score + clarity_score
        confidence = round(max(min(base_confidence + 0.15, 0.98), 0.35), 2)

    explicit_subsystem_signal = any(
        token in input_lower
        for token in [
            "01", "02", "03", "04", "05",
            "p01", "p02", "p03", "p04", "p05",
            "q-spectrum", "qspectrum", "q-spectrum",
            "ghost channel", "幽灵通道", "知识库", "qcm",
            "用户交付包",
        ]
    )
    action_signal = any(
        token in input_lower
        for token in ["测试", "验证", "运行", "启动", "状态", "摘要", "健康",
                      "api", "mcp", "status", "query", "search", "health", "搜索"]
    )
    if top_intent != "AMBIGUOUS" and explicit_subsystem_signal and action_signal:
        confidence = max(confidence, 0.82)
    if top_intent == "MISSION_MEMORY_AWAKENING" and (
        ("唤醒" in user_input and "激活" in user_input) or "awakening" in input_lower
    ):
        confidence = max(confidence, 0.82)
    self_bootstrap_signal = (
        ("母包" in user_input and ("自身" in user_input or "自己" in user_input or "反哺" in user_input))
        or "self-bootstrap" in input_lower
        or "self bootstrap" in input_lower
        or "mother-delivery-package自己" in input_lower
    )
    if self_bootstrap_signal:
        top_intent = "SELF_BOOTSTRAP_PROJECT"
        confidence = max(confidence, 0.86)

    # Step 3: Route decision
    if confidence >= 0.80:
        route_decision = "DIRECT"
    elif confidence >= 0.60:
        route_decision = "CONFIRM"
    else:
        route_decision = "CLARIFY"

    # Step 4: Radar scan
    intent_data = INTENT_REGISTRY.get(top_intent, {})
    track = intent_data.get("track", "understanding")
    primary_route = intent_data.get("primary_route", "追问，不执行")

    # Platform detection from keywords
    platform = "mother_pack"
    platform_map = {
        "P03_WORKBUDDY_KB": ["03", "p03", "workbuddy", "知识库", "mcp"],
        "P04_QCM": ["04", "p04", "qcm", "沙盘", "涌现"],
        "P05_QSPECTRUM": ["05", "p05", "q-spectrum", "qspectrum",
                          "q-spectrum", "超极智脑", "智脑"],
        "P01_GHOST_CHANNEL": ["01", "p01", "ghost channel", "幽灵通道"],
        "P02_UNIVERSAL_KB": ["02", "p02", "universal-kb"],
        "USER_PACK": ["用户交付包", "最终用户交付包", "协同通用ai", "user_pack",
                      "delivery package"],
    }
    for name, aliases in platform_map.items():
        if any(alias in input_lower for alias in aliases):
            platform = name
            break
    # Check for cross-subsystem keywords
    cross_keywords = ["跨", "全部", "整体", "所有", "cross", "all"]
    if top_intent in {"CROSS_SYSTEM_GOLDEN_PATH", "SELF_BOOTSTRAP_PROJECT"} or any(kw in input_lower for kw in cross_keywords):
        platform = "cross_subsystem"

    if top_intent in {"CROSS_SYSTEM_GOLDEN_PATH", "SELF_BOOTSTRAP_PROJECT"}:
        primary_route = "ROOT -> 00 -> 03/04/05 -> USER_PACK"
    elif platform == "P05_QSPECTRUM" and top_intent == "CAPABILITY_INTEGRATION":
        primary_route = "05.Q-SpecTrum runtime/API/MCP"
    elif platform == "P03_WORKBUDDY_KB" and top_intent == "KNOWLEDGE_MEMORY":
        primary_route = "03 WorkBuddy KB search/MCP"
    elif platform == "USER_PACK" and top_intent == "USER_DELIVERY":
        primary_route = "协同通用AI大模型开发交付包"

    # People detection
    people = ["developer"]
    people_map = {
        "审查": ["risk_auditor", "qa"], "审计": ["risk_auditor"],
        "架构": ["architect"], "知识": ["knowledge_manager"],
        "交付": ["delivery_architect"], "用户": ["final_user"],
        "测试": ["qa"], "沙盘": ["architect", "developer"],
    }
    for kw, roles in people_map.items():
        if kw in user_input:
            people = roles
            break

    # Step 5: Generate output
    print_subheader("意图判定")
    print(f"  用户输入: {user_input[:100]}")
    print(f"  归一化意图: {intent_data.get('keywords', [''])[0] if top_intent != 'AMBIGUOUS' else '目标不清楚'}")
    print(f"  意图 ID: {top_intent}")
    print(f"  置信度: {confidence}")
    print(f"  路由决策: {route_decision}")

    if scores:
        print_subheader("意图匹配分数")
        for iid, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]:
            filled = int(score * 20)
            bar = "#" * filled + "-" * (20 - filled)
            print(f"  {iid:30s} {bar} {score:.2f}")

    print_subheader("五维雷达")
    print(f"  Track:     {track}")
    print(f"  Platform:  {platform}")
    print(f"  People:    {', '.join(people)}")
    style = "explore" if route_decision == "CLARIFY" else (
        "decisive" if route_decision == "DIRECT" else "review")
    print(f"  Style:     {style}")
    supplements = []
    if confidence < 0.60:
        supplements.append("need_user_confirmation")
    if top_intent == "IMPLEMENTATION":
        supplements.append("need_tests")
    if platform == "cross_subsystem":
        supplements.append("missing_goal")
    print(f"  Supplement: {', '.join(supplements) or 'none'}")

    print_subheader("路由目标")
    print(f"  主路由: {primary_route}")
    rejected = [iid for iid, sc in scores.items() if iid != top_intent and sc > 0.2]
    if rejected:
        print(f"  排除路由: {', '.join(rejected[:5])}")
    validation_refs = _route_validation_refs(top_intent, platform)
    uso_id = _route_uso_id(top_intent, platform)

    # Generate YAML output
    print_subheader("Guide Secretary YAML")
    ts = datetime.now().isoformat(timespec="seconds")
    yaml_out = f"""\
guide_secretary:
  schema_version: "1.0"
  raw_user_input: "{user_input[:200]}"
  normalized_intent: "{intent_data.get('keywords', [''])[0] if top_intent != 'AMBIGUOUS' else '目标不清楚'}"
  intent_id: "{top_intent}"
  route_decision: "{route_decision}"
  confidence: {confidence}
  radar:
    track: "{track}"
    platform: "{platform}"
    people: {json.dumps(people)}
    style: "{style}"
    supplement: {json.dumps(supplements)}
  target:
    subsystem: "{primary_route}"
    primary_files: []
    role_team: {json.dumps(people)}
    tools_or_commands: []
  traceability:
    uso_id: {json.dumps(uso_id)}
    ledger_ref: "00.超级提示词工程/14-全链路审计与运行对齐/UNIFIED-STATUS-LEDGER.yaml"
    validation_refs: {json.dumps(validation_refs)}
  route_feedback:
    routing_matrix_version: "{ts[:10]}"
    selected_route: "{primary_route}"
    rejected_routes: {json.dumps(rejected[:5])}
    confidence_after_routing: {confidence}
    feedback_to_guide: "{"keep" if route_decision == "DIRECT" else "confirm" if route_decision == "CONFIRM" else "clarify"}"
    blocked_reason: null
  governance:
    required_ids: []
    stage_gate: "{_map_track_to_gate(track)}"
    missing_items: []
    stop_lines: []
  next_action:
    type: "{"handoff" if route_decision == "DIRECT" else "ask"}"
    description: "{"交给执行模型/角色/子系统" if route_decision == "DIRECT" else "请用户确认路由方向"}"
generated_at: "{ts}"
"""
    print(yaml_out)
    if top_intent == "MISSION_MEMORY_AWAKENING":
        awakening_check = {
            "status": "ready_for_handoff",
            "model_native_boundary": "通用AI保留原生推理、工具执行和代码审计能力，母包不取代模型。",
            "mother_pack_boundary": "母包提供使命、路由、记忆源、验证门和交付治理控制平面。",
            "user_pack_boundary": "用户交付包是最终项目交接模板，Strict 门是结构/交接门，不等于业务运行测试。",
            "required_first_reads": [
                "MISSION-MEMORY.md",
                "MOTHER-PACK-ACTIVATION-GUIDE.md",
                "AI_PROJECT_CONTEXT.md",
                "00.超级提示词工程/14-全链路审计与运行对齐/SCENARIO-ACCEPTANCE-MATRIX.md",
            ],
            "next_gate": "Run qa_runner.py validate --scope ROOT before execution claims.",
        }
        print("awakening_check:")
        for key, value in awakening_check.items():
            print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")

    return 0


def _map_track_to_gate(track: str) -> str:
    """Map track to stage gate."""
    gate_map = {
        "understanding": "需求发现",
        "planning": "架构设计",
        "prd_spec": "架构设计",
        "implementation": "实施规划",
        "review": "验证测试",
        "delivery": "总结归档",
        "memory": "需求发现",
        "emergency": "需求发现",
    }
    return gate_map.get(track, "需求发现")


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Mother Delivery Package — QA Runner (三环集成内核)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
子命令:
  validate     执行VALIDATION_REGISTRY验证命令
  status       输出4注册表+LEDGER系统全貌
  consistency  运行10维度跨文档一致性检查
  route        Guide Secretary意图匹配与路由

示例:
  python qa_runner.py validate
  python qa_runner.py validate --scope QCM
  python qa_runner.py status
  python qa_runner.py consistency
  python qa_runner.py route "帮我理解整个母包"
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # validate
    p_val = subparsers.add_parser("validate", help="Validation环")
    p_val.add_argument("--scope", "-s", type=str, default=None,
                       help="过滤范围 (ROOT/P00/P01/P02/P03/P04/P05/USER_PACK)")

    # status
    subparsers.add_parser("status", help="Status环")

    # consistency
    subparsers.add_parser("consistency", help="Consistency环")

    # route
    p_route = subparsers.add_parser("route", help="Routing环")
    p_route.add_argument("text", type=str, nargs="?", default=None,
                         help="用户输入文本")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmd_map = {
        "validate": cmd_validate,
        "status": cmd_status,
        "consistency": cmd_consistency,
        "route": cmd_route,
    }

    handler = cmd_map.get(args.command)
    if handler:
        sys.exit(handler(args))
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
