import argparse
import logging

from vulnrelay.scanners.utils import validate_scanner
from vulnrelay.services import run_workflow

logging.basicConfig(level=logging.DEBUG)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanners", nargs="+", help="List of scanners to run")
    parser.add_argument("--images", nargs="+", help="List of images to scan")

    namespace = parser.parse_args()

    if namespace.scanners:
        for scanner in namespace.scanners:
            try:
                validate_scanner(scanner)
            except ValueError as e:
                raise SystemExit(e)

    run_workflow(images=namespace.images, scanner_names=namespace.scanners)


if __name__ == "__main__":
    main()
