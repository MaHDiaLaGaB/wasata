import logging
import time
from typing import Any, Callable
from functools import partial
import re

import requests

_snake_1 = partial(re.compile(r"(.)((?<![^A-Za-z])[A-Z][a-z]+)").sub, r"\1_\2")
_snake_2 = partial(re.compile(r"([a-z0-9])([A-Z])").sub, r"\1_\2")


# ---------------------------------------
# Convert to snake casing (for DB models)
# ---------------------------------------
def snake_case(string: str) -> str:
    return _snake_2(_snake_1(string)).casefold()


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
