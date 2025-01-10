from enum import Enum
from typing import Any


class MetricNames(Enum):
    LAST_SCAN_AND_PUSH = "last_successful_scan_push"


class Metric:
    def __init__(self, *, last_output: Any | None = None) -> None:
        self.outputs = []
        if last_output:
            self.outputs.append(last_output)

    @property
    def last_output(self) -> Any | None:
        if len(self.outputs) == 0:
            return None
        return self.outputs[-1]

    def save_output(self, value: Any) -> None:
        self.outputs.append(value)
