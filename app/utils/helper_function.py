import logging
import time
from typing import Any, Callable, Dict
import uuid
import requests

logger = logging.getLogger(__name__)


def wait_until_status_code(
    url: str,
    code_to_await: int = 200,
    interval_seconds: float = 1,
    fail_after_seconds: float = 30,
) -> None:
    @wait_until_no_assertion_error(interval_seconds, fail_after_seconds)
    def check_result() -> None:
        try:
            logging.info(f"Checking if {url} will return {code_to_await}.")
            result = requests.get(url, timeout=30)
            assert result.status_code == code_to_await
        except Exception as exc:  # pylint: disable=broad-except
            logging.info(f"Got exception: {exc}")
            assert False


# ----------------------------------------------------------
# reruns the method until there are no assertion exceptions
# fails after fail_after_seconds
# ----------------------------------------------------------
def wait_until_no_assertion_error(
    interval_seconds: float = 0.2, fail_after_seconds: float = 3
) -> Any:
    def decorator(func: Callable[[], None]) -> Callable[[], None]:
        start = time.time()
        while True:
            try:
                func()
                return func
            except AssertionError:
                #  if we have tried long enough, re-raise the assertion
                if time.time() - start > fail_after_seconds:
                    raise
            time.sleep(interval_seconds)

    return decorator


# ----------------------------------------------------------------
# Create idempotency key to use to protect us from double requests
# ----------------------------------------------------------------
def check_idempotency_key(
    idempotency_key: str, idempotency_keys: Dict[str, bool]
) -> bool:
    return idempotency_key in idempotency_keys


def store_idempotency_key(
    idempotency_key: str, idempotency_keys: Dict[str, bool]
) -> None:
    idempotency_keys[idempotency_key] = True


def create_idempotency_key() -> str:
    return str(uuid.uuid4())
