from __future__ import annotations

from is_auto.core.types import Action, RetryPolicy, VerifySpec


def choose_action(obs: dict) -> Action:
    if obs.get("node_options"):
        kind = "choose_node"
        args = {"index": 0}
    elif obs.get("choice_options"):
        kind = "choose_option"
        args = {"index": 0}
    else:
        kind = "confirm"
        args = {}
    return Action(
        kind=kind,
        args=args,
        verify=VerifySpec(expect_page_id="route_map", timeout_ms=500, retries=1),
        retry_policy=RetryPolicy(max_retry=2, backoff_ms=100),
    )
