import logging
import os
import subprocess
import time
from collections.abc import Callable, Iterable

from vulnrelay.core.conf import settings
from vulnrelay.metrics import MetricExporter, MetricNames
from vulnrelay.scanners import Scanner
from vulnrelay.uploader import DefectDojoUploader, Uploader

logger = logging.getLogger(__name__)


def get_running_images() -> Iterable[str]:
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--format",
                "{{.Image}}",
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error("Failed to get running images:\n%s", e.stderr.decode("utf-8"))
        raise
    return set(result.stdout.decode("utf-8").splitlines())


def get_uploader() -> Uploader:
    return DefectDojoUploader(
        url=settings.DD_URL,
        api_key=settings.DD_API_KEY,
        environment=settings.ENV,
        product=settings.DD_PRODUCT,
        engagement=settings.DD_ENGAGEMENT,
    )


def get_metric_exporter() -> MetricExporter:
    return MetricExporter(
        metrics={
            MetricNames.LAST_SCAN_AND_PUSH.value: None,
        },
        path=os.path.join(settings.METRICS_DIR, settings.METRICS_FILENAME),
    )


def run_workflow(
    *,
    images: Iterable[str] | None = None,
    scanner_names: Iterable[str] | None = None,
    get_uploader: Callable[[], Uploader] = get_uploader,
    get_metric_exporter: Callable[[], MetricExporter] = get_metric_exporter,
    scan_host: bool = True,
) -> None:
    images = images or get_running_images()
    scanner_names = scanner_names or settings.SCANNERS
    uploader = get_uploader()
    metric_exporter = get_metric_exporter()

    for scanner_name in scanner_names:
        scanner = Scanner.get_scanner(scanner_name)()

        for image in images:
            logger.info("Scanning image %s with %s", image, scanner_name)
            try:
                result = scanner.scan_image(image)
            except Exception:
                logger.exception("Failed to scan image %s with %s", image, scanner_name)
                continue

            logger.info("Scan successful. Uploading result")

            try:
                uploader.upload_scan_result(
                    service=image,
                    scan_type=scanner.defectdojo_name(),
                    content=result,
                )
            except Exception:
                logger.exception("Failed to upload %s results for %s", scanner_name, image)
                continue

            logger.info("Upload successful")

        if not scan_host:
            continue

        logger.info("Scanning host filesystem with %s", scanner_name)

        try:
            result = scanner.scan_host()
        except Exception:
            logger.exception("Failed to scan host filesystem with %s", scanner_name)
            continue

        logger.info("Scan successful. Uploading result")

        try:
            uploader.upload_scan_result(
                service="host",
                scan_type=scanner.defectdojo_name(),
                content=result,
            )
        except Exception:
            logger.exception("Failed to upload %s results for host fs", scanner_name)
            continue

        logger.info("Upload successful")

    try:
        metric_exporter.save_and_export(
            values={MetricNames.LAST_SCAN_AND_PUSH.value: int(time.time())},
        )
    except Exception:
        logger.exception("Failed to export metrics!")
