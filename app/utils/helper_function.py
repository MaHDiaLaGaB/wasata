import logging
import time
from typing import Any, Callable, Dict, Tuple
from fastapi import status, HTTPException
from functools import partial
import re
import httpx
import uuid
import aiocache
from app.core.config import config
import requests

logger = logging.getLogger(__name__)

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


# TODO needs to move this function from here
async def payment_getaway(usdt_price: float, invoice_id: str) -> HTTPException | Tuple[Any, Any, str]:
    # Generate a unique token for the transaction
    transaction_token = str(uuid.uuid4())

    # Check if the token exists in the cache
    if await aiocache_caching.get(transaction_token):
        return HTTPException(
            detail="Duplicate transaction request",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    async with httpx.AsyncClient() as client:
        # Call the /checkout endpoint
        checkout_response = await client.post('http://moamalat:3000/checkout', json={
            'amount': usdt_price,
            'reference': invoice_id,
        })
        checkout_data = checkout_response.json()

        # Call the /transactionApproved endpoint
        approved_response = await client.post('http://moamalat:3000/transactionApproved', json={
            'reference': invoice_id,
        })
        approved_data = approved_response.json()

    # Store the token in the cache with an expiration time (e.g., 5 seconds)
    await aiocache_caching.set(transaction_token, True, ttl=5)
    logger.info(f"{approved_data} >>> {checkout_data} >>> {invoice_id}")
    return approved_data, checkout_data, invoice_id


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
