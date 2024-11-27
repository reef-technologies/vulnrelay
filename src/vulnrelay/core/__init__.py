from .conf import settings

if settings.SENTRY_DSN:
    import sentry_sdk

    environment = f"{settings.DD_PRODUCT} - {settings.DD_ENGAGEMENT}"
    sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=environment)
