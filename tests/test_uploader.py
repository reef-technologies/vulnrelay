import pytest
from faker import Faker
from responses import RequestsMock, matchers

from vulnrelay.uploader.defectdojo import DefectDojoUploader


@pytest.fixture
def url(faker: Faker):
    return faker.url().removesuffix("/")


@pytest.fixture
def username(faker: Faker):
    return faker.word()


@pytest.fixture
def password(faker: Faker):
    return faker.word()


@pytest.fixture
def environment(faker: Faker):
    return faker.word()


@pytest.fixture
def product(faker: Faker):
    return faker.word()


@pytest.fixture
def engagement(faker: Faker):
    return faker.word()


@pytest.fixture
def token(faker: Faker):
    return faker.pystr()


@pytest.fixture
def dd_uploader(url: str, username: str, password: str, environment: str, product: str, engagement: str):
    return DefectDojoUploader(
        url=url,
        username=username,
        password=password,
        environment=environment,
        product=product,
        engagement=engagement,
    )


def test_authenticate(
    dd_uploader: DefectDojoUploader, responses: RequestsMock, url: str, username: str, password: str, token: str
):
    auth_url = f"{url}/api/v2/api-token-auth/"

    responses.post(
        auth_url,
        match=[
            matchers.body_matcher(f"username={username}&password={password}"),
        ],
        json={"token": token},
    )

    dd_uploader.authenticate()
    assert dd_uploader.session.headers["Authorization"] == f"Token {token}"


def test_upload_image_result(
    dd_uploader: DefectDojoUploader,
    responses: RequestsMock,
    url: str,
    token: str,
    environment: str,
    product: str,
    engagement: str,
    faker: Faker,
):
    auth_url = f"{url}/api/v2/api-token-auth/"
    import_url = f"{url}/api/v2/import-scan/"

    scan_result = faker.word()
    scan_type = "Anchore Grype"
    service = faker.word()

    rsp_auth = responses.post(auth_url, json={"token": token})
    rsp_import = responses.post(
        import_url,
        match=[
            matchers.header_matcher({"Authorization": f"Token {token}"}),
        ],
    )

    dd_uploader.upload_scan_result(service=service, scan_type=scan_type, content=scan_result)

    assert rsp_auth.call_count == 1
    assert rsp_import.call_count == 1

    body = rsp_import.calls[0].request.body.decode("utf-8")

    for field in (scan_result, scan_type, service, environment, product, engagement):
        assert field in body
