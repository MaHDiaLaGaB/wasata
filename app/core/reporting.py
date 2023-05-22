import logging
from typing import Any

import sentry_sdk


def setup(config: Any) -> None:
    if config.SENTRY_DSN:
        sentry_sdk.init(
            config.SENTRY_DSN,
            traces_sample_rate=0.0,
            environment=config.ENV,
            integrations=[],
        )
        sentry_sdk.set_context("component", config.NAME)


def report_exception(exc: Exception) -> None:
    """
    Report the exception here, not used at the moment
    """
    try:
        # in case of error logging happens in the client
        sentry_sdk.capture_exception(exc)
    except Exception as exc_inner:
        logging.error("Could not report Exception to sentry")
        raise exc_inner
