from __future__ import annotations

from typing import Any


_ACTION_KINDS = {"click", "confirm", "scroll", "choose_node", "choose_option"}


def _check_bbox(path: str, bbox: Any, errors: list[str]) -> None:
    if not isinstance(bbox, list) or len(bbox) != 4 or not all(isinstance(v, int) for v in bbox):
        errors.append(f"{path} must be [int,int,int,int]")


def validate_obs(obs: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(obs.get("page_id"), str):
        errors.append("page_id must be str")
    conf = obs.get("confidence")
    if not isinstance(conf, (int, float)) or not 0 <= float(conf) <= 1:
        errors.append("confidence must be float in [0,1]")

    run_state = obs.get("run_state")
    for key, typ in {"season": str, "difficulty": str, "floor": int, "node_index": int}.items():
        if not isinstance(run_state, dict) or not isinstance(run_state.get(key), typ):
            errors.append(f"run_state.{key} must be {typ.__name__}")

    resources = obs.get("resources")
    for key in ("hope", "ingot"):
        if not isinstance(resources, dict) or not isinstance(resources.get(key), int):
            errors.append(f"resources.{key} must be int")

    node_options = obs.get("node_options")
    if not isinstance(node_options, list):
        errors.append("node_options must be list")
    else:
        for i, item in enumerate(node_options):
            if not isinstance(item, dict) or not isinstance(item.get("type"), str):
                errors.append(f"node_options[{i}].type must be str")
                continue
            _check_bbox(f"node_options[{i}].bbox", item.get("bbox"), errors)
            if not isinstance(item.get("conf"), (int, float)):
                errors.append(f"node_options[{i}].conf must be float")

    choice_options = obs.get("choice_options")
    if not isinstance(choice_options, list):
        errors.append("choice_options must be list")
    else:
        for i, item in enumerate(choice_options):
            if not isinstance(item, dict) or not isinstance(item.get("text"), str):
                errors.append(f"choice_options[{i}].text must be str")
                continue
            _check_bbox(f"choice_options[{i}].bbox", item.get("bbox"), errors)
            if not isinstance(item.get("conf"), (int, float)):
                errors.append(f"choice_options[{i}].conf must be float")

    return (len(errors) == 0, errors)


def validate_action(action: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if action.get("kind") not in _ACTION_KINDS:
        errors.append("kind invalid")
    if not isinstance(action.get("args"), dict):
        errors.append("args must be dict")

    verify = action.get("verify")
    if not isinstance(verify, dict):
        errors.append("verify must be dict")
    else:
        if verify.get("expect_page_id") is not None and not isinstance(verify.get("expect_page_id"), str):
            errors.append("verify.expect_page_id must be str or null")
        for key in ("timeout_ms", "retries"):
            if not isinstance(verify.get(key), int):
                errors.append(f"verify.{key} must be int")

    retry = action.get("retry_policy")
    if not isinstance(retry, dict):
        errors.append("retry_policy must be dict")
    else:
        for key in ("max_retry", "backoff_ms"):
            if not isinstance(retry.get(key), int):
                errors.append(f"retry_policy.{key} must be int")

    return (len(errors) == 0, errors)
