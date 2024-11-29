import logging
import subprocess

from .base import Scanner, ScannerError

logger = logging.getLogger(__name__)


class Grype(Scanner, name="grype"):
    docker_image = "anchore/grype:latest"

    def defectdojo_name(self) -> str:
        return "Anchore Grype"

    def _perform_scan(self, target: str, *extra_run_args: str) -> str:
        cmd = [
            "docker",
            "run",
            "--rm",
            "--volume",
            "/var/run/docker.sock:/var/run/docker.sock:ro",
            "--volume",
            "grype-cache:/root/.cache/grype",
            "-e",
            "GRYPE_DB_CACHE_DIR=/root/.cache/grype",
            *extra_run_args,
            self.docker_image,
            "-o",
            "json",
            target,
        ]

        logger.debug("Running command: %s", cmd)

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise ScannerError("Command:\n%s\nReturned:%s\n", cmd, e.stderr.decode("utf-8")) from e

        output = result.stdout.decode("utf-8")
        logger.debug("Scan result: %s", output)

        return output

    def scan_image(self, image_name: str) -> str:
        return self._perform_scan(image_name)

    def scan_host(self) -> str:
        return self._perform_scan("dir:/host", "--volume", "/:/host:ro")
