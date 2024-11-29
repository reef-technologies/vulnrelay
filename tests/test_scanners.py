import pytest
from pytest_subprocess import FakeProcess

from vulnrelay.scanners.grype import Grype


@pytest.fixture
def grype_scanner():
    return Grype()


def test_scan_image(fp: FakeProcess, grype_scanner: Grype):
    output = "foo"
    image = "image1"

    fp.register(
        ["docker", "run", "--rm", fp.any()],
        stdout=output,
    )
    assert grype_scanner.scan_image(image) == output

    assert "/var/run/docker.sock:/var/run/docker.sock:ro" in fp.calls[0]
    assert grype_scanner.docker_image in fp.calls[0]


def test_scan_host(fp: FakeProcess, grype_scanner: Grype):
    output = "foo"

    fp.register(
        ["docker", "run", fp.any()],
        stdout=output,
    )
    assert grype_scanner.scan_host() == output

    assert "/var/run/docker.sock:/var/run/docker.sock:ro" in fp.calls[0]
    assert grype_scanner.docker_image in fp.calls[0]
