from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FrameSource(ABC):
    @abstractmethod
    def get_frame(self) -> dict[str, Any]:
        raise NotImplementedError


class InputSink(ABC):
    @abstractmethod
    def execute(self, action: dict[str, Any]) -> None:
        raise NotImplementedError
