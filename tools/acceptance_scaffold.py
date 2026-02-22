from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "pyproject.toml",
    ".gitignore",
    ".editorconfig",
    "ruff.toml",
    "configs/profile.example.yaml",
    "docs/DEV_SETUP.md",
    "docs/WORKFLOW.md",
    "docs/ARCHITECTURE.md",
    "src/is_auto/__main__.py",
    "src/is_auto/cli.py",
    "src/is_auto/core/types.py",
    "src/is_auto/core/contract.py",
    "src/is_auto/core/evidence.py",
    "src/is_auto/fsm/fsm.py",
    "src/is_auto/drivers/base.py",
    "src/is_auto/drivers/dummy.py",
    "src/is_auto/perception/page_id.py",
    "src/is_auto/decision/policy_v0.py",
    "src/is_auto/actuation/primitives.py",
    "tools/acceptance_scaffold.py",
    "tests/test_contract.py",
    "tests/test_evidence.py",
]


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def has_large_files() -> bool:
    for p in Path(".").rglob("*"):
        if p.is_file() and ".git" not in p.parts and p.stat().st_size > 1_000_000:
            return True
    return False


def main() -> int:
    deductions: list[str] = []
    score = 10

    missing = [f for f in REQUIRED_FILES if not Path(f).exists()]
    if missing:
        score -= 2
        deductions.append(f"missing_files:{missing}")

    rc, out = run([sys.executable, "-m", "compileall", "-q", "src/is_auto"])
    if rc != 0:
        score -= 2
        deductions.append("compileall_failed")

    rc_help, _ = run([sys.executable, "-m", "is_auto", "--help"])
    rc_smoke, smoke_out = run([sys.executable, "-m", "is_auto", "smoke", "--out", "runs"])
    rc_contract, _ = run(
        [sys.executable, "-m", "is_auto", "validate-contract", "--example-out", "runs/_contract_examples"]
    )
    rc_script, _ = run(["is_auto", "--help"])
    if any(code != 0 for code in [rc_help, rc_smoke, rc_contract, rc_script]):
        score -= 2
        deductions.append("cli_commands_failed")

    run_dirs = sorted([p for p in Path("runs").glob("20*/") if p.is_dir()])
    evidence_ok = False
    if run_dirs:
        latest = run_dirs[-1]
        evidence_ok = all((latest / n).exists() for n in ["metadata.jsonl", "run.log", "run_manifest.json"]) and any(
            latest.glob("episode_0001")
        )
    if not evidence_ok:
        score -= 2
        deductions.append("evidence_chain_missing")

    if has_large_files():
        score -= 2
        deductions.append("large_files_present")

    if not Path("docs/WORKFLOW.md").exists() or not Path("docs/DEV_SETUP.md").exists():
        score -= 1
        deductions.append("collab_docs_missing")

    rc_status, status_out = run(["git", "status", "--porcelain"])
    _ = rc_status
    if "tmp" in status_out.lower():
        score -= 1
        deductions.append("temporary_files_in_git_status")

    fatal = any(x in deductions for x in ["cli_commands_failed", "large_files_present"])
    passed = score >= 9 and not fatal
    report = {
        "score": score,
        "max_score": 10,
        "passed": passed,
        "deductions": deductions,
        "smoke_output": smoke_out.strip().splitlines()[-1] if smoke_out.strip() else "",
        "compileall_output": out.strip(),
    }
    print(f"ACCEPTANCE_JSON={json.dumps(report, ensure_ascii=False)}")
    if passed:
        print("PASS")
        return 0
    print("FAIL", deductions)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
