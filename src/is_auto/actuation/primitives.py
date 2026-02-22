from __future__ import annotations

from is_auto.drivers.base import InputSink


def execute_action(driver: InputSink, action: dict) -> None:
    driver.execute(action)
