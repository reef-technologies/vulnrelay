import pytest
from faker import Faker
from pytest_subprocess import FakeProcess

from vulnrelay.scanners import Scanner
from vulnrelay.services import get_running_images, run_workflow
from vulnrelay.uploader.base import Uploader


def test_get_running_images(fp: FakeProcess):
    fp.register("docker ps --format {{.Image}}", stdout="image1\nimage1\nimage2\n")
    assert set(get_running_images()) == {"image1", "image2"}


class StubUploader(Uploader):
    def __init__(self):
        self.results = []

    def upload_scan_result(self, service, scan_type, content):
        self.results.append((service, scan_type, content))


class StubScanner(Scanner, name="stub"):
    scans: list[str] = []
    result = ""

    def defectdojo_name(self) -> str:
        return "stub"

    def scan_image(self, image_name: str) -> str:
        StubScanner.scans.append(image_name)
        return StubScanner.result


@pytest.fixture
def uploader():
    return StubUploader()


@pytest.fixture
def scan_result(faker: Faker):
    return faker.sentence()


@pytest.fixture
def scanner(scan_result: str):
    instance = StubScanner()
    StubScanner.result = scan_result
    yield instance
    StubScanner.result = ""


def test_run_workflow(scanner: StubScanner, uploader: StubUploader, scan_result: str):
    images = ["image1", "image2"]

    run_workflow(
        images=["image1", "image2"],
        scanner_names=["stub"],
        get_uploader=lambda: uploader,
    )

    assert scanner.scans == images
    assert len(uploader.results) == len(images)
    for image in images:
        assert (image, "stub", scan_result) in uploader.results
