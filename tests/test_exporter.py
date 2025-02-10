import tempfile
import time
from pathlib import Path

from vulnrelay.metrics.exporter import MetricExporter
from vulnrelay.metrics.metric import MetricNames


def test_export_metrics():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "test.prom"
        metric_exporter = MetricExporter(path=path)
        timestamp = time.time()
        metric_exporter.save_and_export(
            values={
                MetricNames.LAST_SCAN_AND_PUSH: timestamp,
            },
        )

        with open(path) as file:
            contents: str = file.read()
            assert contents == f"{MetricNames.LAST_SCAN_AND_PUSH.value} {timestamp}"
