import os
import shutil
from pathlib import Path
from typing import Any


class MetricExporter:
    def __init__(self, *, metrics: dict[str, Any], path: str) -> None:
        self.metrics: dict[str, Any] = metrics
        self.path = path
        self._check_dir()

    def _get_export_content(self) -> str:
        return "\n".join([f"{name} {metric}" for name, metric in self.metrics.items()])

    def _check_dir(self) -> None:
        dir_path = Path(self.path).parent
        dir_path.mkdir(parents=True, exist_ok=True)

    def export_all(self) -> None:
        content = self._get_export_content()
        path = self.path
        temp_file = f"{path}.tmp"

        with open(temp_file, "w") as file:
            file.write(content)

        try:
            shutil.move(temp_file, path)
        except Exception as e:
            os.remove(temp_file)
            raise e

    def save_and_export(self, *, values: dict[str, Any]) -> None:
        for name, value in values.items():
            self.metrics[name] = value
            self.export_all()
