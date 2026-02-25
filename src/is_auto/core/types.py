from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class RunState:
    season: str
    difficulty: str
    floor: int
    node_index: int


@dataclass(slots=True)
class ResourceState:
    hope: int
    ingot: int


@dataclass(slots=True)
class OptionBox:
    type: str
    bbox: list[int]
    conf: float


@dataclass(slots=True)
class ChoiceOption:
    text: str
    bbox: list[int]
    conf: float


@dataclass(slots=True)
class Obs:
    page_id: str
    confidence: float
    run_state: RunState
    resources: ResourceState
    node_options: list[OptionBox]
    choice_options: list[ChoiceOption]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class VerifySpec:
    expect_page_id: str | None
    timeout_ms: int
    retries: int


@dataclass(slots=True)
class RetryPolicy:
    max_retry: int
    backoff_ms: int


@dataclass(slots=True)
class Action:
    kind: str
    args: dict[str, Any]
    verify: VerifySpec
    retry_policy: RetryPolicy

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
