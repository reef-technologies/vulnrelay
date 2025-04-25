import argparse
import logging

from vulnrelay.core.conf import settings
from vulnrelay.scanners.utils import validate_scanner
from vulnrelay.services import run_workflow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main() -> None:
    if not settings.DD_URL:
        logging.warning("No DefectDojo URL configured. Skipping scanning")

    parser = argparse.ArgumentParser()
    parser.add_argument("--scanners", nargs="+", help="List of scanners to run")
    parser.add_argument("--images", nargs="+", help="List of images to scan")
    parser.add_argument("--scan-host", action="store_true", default=False, help="Do not scan host filesystem")

    namespace = parser.parse_args()

    if namespace.scanners:
        for scanner in namespace.scanners:
            try:
                validate_scanner(scanner)
            except ValueError as e:
                raise SystemExit(e)

    scan_host = namespace.scan_host or settings.SCAN_HOST

    if scan_host:
        logging.warning("Host scanning enabled. This may consume a lot of resources and take a long time")

    run_workflow(
        images=namespace.images,
        scanner_names=namespace.scanners,
        scan_host=scan_host,
    )


if __name__ == "__main__":
    main()
