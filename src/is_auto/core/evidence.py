from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


def create_run_dir(base_dir: str | Path) -> Path:
    root = Path(base_dir)
    root.mkdir(parents=True, exist_ok=True)
    run_dir = root / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def create_episode_dir(run_dir: str | Path, idx: int) -> Path:
    episode_dir = Path(run_dir) / f"episode_{idx:04d}"
    episode_dir.mkdir(parents=True, exist_ok=True)
    return episode_dir


def append_event(run_dir: str | Path, episode_dir: str | Path, event_dict: dict[str, Any]) -> None:
    payload = {"episode_dir": str(Path(episode_dir).name), **event_dict}
    with (Path(run_dir) / "metadata.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _get_git_commit() -> str | None:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        return out
    except Exception:
        return None


def write_run_manifest(run_dir: str | Path, profile_text: str) -> dict[str, Any]:
    manifest = {
        "git_commit": _get_git_commit(),
        "profile_hash": hashlib.sha256(profile_text.encode("utf-8")).hexdigest(),
        "started_at": datetime.now().isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "python": platform.python_version(),
        },
    }
    out = Path(run_dir) / "run_manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest
