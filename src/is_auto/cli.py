from __future__ import annotations

import argparse
import json
from pathlib import Path


from is_auto.actuation.primitives import execute_action
from is_auto.core.contract import validate_action, validate_obs
from is_auto.core.evidence import append_event, create_episode_dir, create_run_dir, write_run_manifest
from is_auto.core.logging import setup_logger
from is_auto.decision.policy_v0 import choose_action
from is_auto.drivers.dummy import DummyDriver
from is_auto.fsm.fsm import State, next_state


def _make_dummy_obs(page_id: str, confidence: float, step: int) -> dict:
    return {
        "page_id": page_id,
        "confidence": confidence,
        "run_state": {
            "season": "IS-SAMPLE",
            "difficulty": "normal",
            "floor": 1,
            "node_index": step,
        },
        "resources": {"hope": 3, "ingot": 10},
        "node_options": [{"type": "battle", "bbox": [10, 10, 100, 100], "conf": 0.9}],
        "choice_options": [{"text": "take relic", "bbox": [20, 20, 120, 120], "conf": 0.8}],
    }


def cmd_smoke(args: argparse.Namespace) -> int:
    run_dir = create_run_dir(args.out)
    episode_dir = create_episode_dir(run_dir, 1)
    logger = setup_logger(run_dir / "run.log")
    profile_text = "profile=dummy"
    manifest = write_run_manifest(run_dir, profile_text)
    logger.info("manifest=%s", manifest)

    driver = DummyDriver()
    state = State.ENTRY
    for step in range(1, 11):
        frame = driver.get_frame()
        page_id = frame["page"]
        obs = _make_dummy_obs(page_id, 0.99, step)
        ok, errors = validate_obs(obs)
        if not ok:
            raise ValueError(f"obs invalid: {errors}")
        action = choose_action(obs).to_dict()
        ok, errors = validate_action(action)
        if not ok:
            raise ValueError(f"action invalid: {errors}")
        execute_action(driver, action)
        state = next_state(state, step)
        event = {
            "step": step,
            "state": state.value,
            "obs_page_id": obs["page_id"],
            "action_kind": action["kind"],
        }
        append_event(run_dir, episode_dir, event)
        logger.info("event=%s", event)
    print(f"SMOKE_OK run_dir={run_dir}")
    return 0


def cmd_validate_contract(args: argparse.Namespace) -> int:
    out_dir = Path(args.example_out)
    out_dir.mkdir(parents=True, exist_ok=True)
    obs = _make_dummy_obs("route_map", 0.98, 1)
    action = choose_action(obs).to_dict()
    (out_dir / "obs.example.json").write_text(json.dumps(obs, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "action.example.json").write_text(
        json.dumps(action, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    ok_obs, err_obs = validate_obs(obs)
    ok_act, err_act = validate_action(action)
    if not (ok_obs and ok_act):
        print("OBS_ERRORS", err_obs)
        print("ACTION_ERRORS", err_act)
        return 1
    print(f"CONTRACT_OK out={out_dir}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    profile_path = Path(args.profile)
    data = {}
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip()
    key_fields = {
        "profile_name": data.get("profile_name"),
        "season": data.get("season"),
        "difficulty": data.get("difficulty"),
        "seed": data.get("seed"),
        "model_id": data.get("model_id"),
        "dry_run": args.dry_run,
    }
    print(json.dumps(key_fields, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="is_auto")
    sub = p.add_subparsers(dest="cmd", required=True)

    smoke = sub.add_parser("smoke")
    smoke.add_argument("--out", default="runs")
    smoke.set_defaults(func=cmd_smoke)

    vc = sub.add_parser("validate-contract")
    vc.add_argument("--example-out", required=True)
    vc.set_defaults(func=cmd_validate_contract)

    run = sub.add_parser("run")
    run.add_argument("--profile", required=True)
    run.add_argument("--dry-run", action="store_true")
    run.set_defaults(func=cmd_run)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)
