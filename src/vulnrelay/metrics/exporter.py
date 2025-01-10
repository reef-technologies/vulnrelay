import os
import shutil
from typing import Any

from .metric import Metric


class MetricExporter:
    def __init__(self, *, metrics: dict[str, Metric], path: str) -> None:
        self.metrics: dict[str, Metric] = metrics
        self.path = path
        self.check_dir()

    def _get_export_content(self) -> str:
        return "\n".join([f"{name} {metric.last_output}" for name, metric in self.metrics.items()])

    def check_dir(self) -> None:
        dir = os.path.dirname(self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def export_all(self) -> None:
        content = self._get_export_content()
        path = self.path
        temp_file = f"{path}.tmp"

        if os.path.exists(path):
            os.remove(path)

        with open(temp_file, "w") as file:
            file.write(content)

        try:
            shutil.move(temp_file, path)
        except Exception as e:
            os.remove(temp_file)
            raise e

    def save_and_export(self, *, values: dict[str, Any]) -> None:
        for name, value in values.items():
            self.metrics[name].save_output(value=value)
        self.export_all()
