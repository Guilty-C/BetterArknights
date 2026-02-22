from is_auto.cli import _make_dummy_obs
from is_auto.core.contract import validate_action, validate_obs
from is_auto.decision.policy_v0 import choose_action


def test_contract_valid() -> None:
    obs = _make_dummy_obs("route_map", 0.9, 1)
    action = choose_action(obs).to_dict()
    assert validate_obs(obs)[0]
    assert validate_action(action)[0]


def test_contract_invalid() -> None:
    ok, errors = validate_obs({"page_id": 1})
    assert not ok
    assert errors
