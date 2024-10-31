import logging
import subprocess

from .base import Scanner

logger = logging.getLogger(__name__)


class Grype(Scanner, name="grype"):
    docker_image = "anchore/grype:latest"

    def defectdojo_name(self) -> str:
        return "Anchore Grype"

    def scan_image(self, image_name: str) -> str:
        cmd = [
            "docker",
            "run",
            "--volume",
            "/var/run/docker.sock:/var/run/docker.sock:ro",
            "--volume",
            "grype-cache:/root/.cache/grype",
            self.docker_image,
            image_name,
            "-o",
            "json",
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
