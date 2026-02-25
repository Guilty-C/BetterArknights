from __future__ import annotations

from typing import Any

from is_auto.drivers.base import FrameSource, InputSink


class DummyDriver(FrameSource, InputSink):
    def __init__(self) -> None:
        self._step = 0

    def get_frame(self) -> dict[str, Any]:
        self._step += 1
        return {"step": self._step, "page": "route_map"}

    def execute(self, action: dict[str, Any]) -> None:
        _ = action
