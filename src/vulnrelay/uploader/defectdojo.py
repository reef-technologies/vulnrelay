import logging

import requests

from .base import Uploader

logger = logging.getLogger(__name__)


class DefectDojoUploader(Uploader):
    def __init__(
        self,
        *,
        url: str,
        api_key: str,
        environment: str,
        product: str,
        engagement: str,
        upload_timeout: int = 120,
    ):
        self._url = url
        self._api_key = api_key
        self._environment = environment
        self._product = product
        self._engagement = engagement
        self._session: requests.Session | None = None
        self._upload_timeout = upload_timeout

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._session.headers["Authorization"] = f"Token {self._api_key}"

        return self._session

    def _get_form_data(self) -> dict[str, str | bytes]:
        return {
            "active": "true",
            "auto_create_context": "true",
            "close_old_findings": "true",
            "product_name": self._product,
            "engagement_name": self._engagement,
            "environment": self._environment,
            "group_by": "component_name+component_version",
            "create_finding_groups_for_all_findings": "true",
            "minimum_severity": "Medium",
        }

    def upload_scan_result(self, *, service: str, scan_type: str, content: str) -> None:
        url = f"{self._url}/api/v2/import-scan/"

        logger.info("Uploading scan result for service %s to %s", service, url)

        form_data = self._get_form_data()
        form_data["service"] = service
        form_data["scan_type"] = scan_type

        response = self.session.post(
            url,
            data=form_data,
            files={"file": content.encode()},
            timeout=self._upload_timeout,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error("Failed to upload scan result: %s", e)
            logger.error("Response: %s", response.text)
            raise

        logger.info("Scan result uploaded successfully")
