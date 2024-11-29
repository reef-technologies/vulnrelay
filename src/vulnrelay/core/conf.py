import pathlib
from typing import Annotated

from pydantic import Field
from pydantic.functional_validators import AfterValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

from vulnrelay.scanners.utils import validate_scanner

SRC_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
ROOT_DIR = SRC_DIR.parent


ScannerOption = Annotated[str, AfterValidator(validate_scanner), Field(validate_default=True)]


class Settings(BaseSettings):
    # DefectDojo settings
    ENV: str
    DD_URL: str
    DD_API_KEY: str
    DD_PRODUCT: str
    DD_ENGAGEMENT: str = "vulnrelay"

    SENTRY_DSN: str | None = None

    SCANNERS: list[ScannerOption] = ["grype"]
    SCAN_HOST: bool = False

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
    )


settings = Settings()
