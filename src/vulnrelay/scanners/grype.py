import logging
import subprocess

from .base import Scanner, ScannerError

logger = logging.getLogger(__name__)


class Grype(Scanner, name="grype"):
    docker_image = "anchore/grype:latest"

    def defectdojo_name(self) -> str:
        return "Anchore Grype"

    def _perform_scan(self, grype_args: list[str], *, extra_run_args: list[str] | None = None) -> str:
        extra_run_args = extra_run_args or []

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
            *grype_args,
        ]

        logger.debug("Running command: %s", cmd)

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            errout = e.stderr.decode("utf-8")
            raise ScannerError(f"{errout}\nSubprocess command:\n{cmd}")

        output = result.stdout.decode("utf-8")
        logger.debug("Scan result: %s", output)

        return output

    def scan_image(self, image_name: str) -> str:
        return self._perform_scan([image_name])

    def scan_host(self) -> str:
        excluded_dirs = [
            "./proc",
            "./sys",
            "./tmp",
            "./var",
            "./home",
        ]

        grype_args = ["dir:/host"]

        for _dir in excluded_dirs:
            grype_args.extend(["--exclude", _dir])

        return self._perform_scan(grype_args, extra_run_args=["--volume", "/:/host:ro"])
