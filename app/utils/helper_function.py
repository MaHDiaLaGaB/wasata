import logging
import time
from typing import Any, Callable, Dict
from fastapi import status, HTTPException

from functools import partial
import re
import os
import secrets
import uuid

import aiocache

from app.core.config import config


import requests

_snake_1 = partial(re.compile(r"(.)((?<![^A-Za-z])[A-Z][a-z]+)").sub, r"\1_\2")
_snake_2 = partial(re.compile(r"([a-z0-9])([A-Z])").sub, r"\1_\2")

aiocache_caching = (
    aiocache.Cache(aiocache.SimpleMemoryCache)
    if config.ENVIRONMENT == "dev"
    else aiocache.Cache(aiocache.RedisCache, endpoint="localhost", port=6379)
)


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


async def payment_getaway(usdt_price: float) -> HTTPException | float:
    # Generate a unique token for the transaction
    transaction_token = str(uuid.uuid4())

    # Check if the token exists in the cache
    if await aiocache_caching.get(transaction_token):
        return HTTPException(
            detail="Duplicate transaction request",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # TODO payment logic should me here

    # Store the token in the cache with an expiration time (e.g., 5 minutes)
    await aiocache_caching.set(transaction_token, True, ttl=5)
    return usdt_price


def check_idempotency_key(
    idempotency_key: str, idempotency_keys: Dict[str, bool]
) -> bool:
    """
    Check if the idempotency key exists in the storage.

    :param idempotency_keys: dict contain the key
    :param idempotency_key: The idempotency key to check.
    :return: True if the key exists, False otherwise.
    """
    return idempotency_key in idempotency_keys


def store_idempotency_key(
    idempotency_key: str, idempotency_keys: Dict[str, bool]
) -> None:
    """
    Store the idempotency key in the storage.

    :param idempotency_keys:
    :param idempotency_key: The idempotency key to store.
    """
    idempotency_keys[idempotency_key] = True


def create_idempotency_key() -> str:
    """
    Generate a new idempotency key.

    :return: A new unique idempotency key.
    """
    return str(uuid.uuid4())
