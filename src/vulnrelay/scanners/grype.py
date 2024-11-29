import logging
import subprocess

from .base import Scanner

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

        logger.info("Running command: %s", cmd)

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error("Grype scan failed:\n%s", e.stderr.decode("utf-8"))
            raise

        output = result.stdout.decode("utf-8")
        logger.debug("Grype scan result: %s", output)

        return output

    def scan_image(self, image_name: str) -> str:
        return self._perform_scan(image_name)

    def scan_host(self) -> str:
        return self._perform_scan("dir:/host", "--volume", "/:/host:ro")
