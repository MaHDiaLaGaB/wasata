from fastapi import status, HTTPException
from app.core.config import config
from typing import Tuple, Any
import logging
import httpx
import uuid
import aiocache

logger = logging.getLogger(__name__)

aiocache_caching = (
    aiocache.Cache(aiocache.SimpleMemoryCache)
    # if config.ENVIRONMENT == "dev"
    # else redis.Redis(host="api", port=6379)
)


# TODO needs to return a custom exceptions from moamalat microservice


async def payment_getaway(
    usdt_price: float, invoice_id: str
) -> HTTPException | Tuple[Any, Any, str]:
    # generate a unique token for the transaction
    transaction_token = str(uuid.uuid4())

    # check if the token exists in the cache
    if await aiocache_caching.get(transaction_token):
        return HTTPException(
            detail="Duplicate transaction request",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    async with httpx.AsyncClient() as client:
        # call the /checkout endpoint

        checkout_response = await client.post(
            config.MO3AMALAT_CHECKOUT,
            json={
                "amount": usdt_price,
                "reference": invoice_id,
            },
        )
        checkout_data = checkout_response.json()

        # call the /transactionApproved endpoint

        approved_response = await client.post(
            config.MOAMALAT_TRANSACTIONS_APPROVED,
            json={
                "reference": invoice_id,
            },
        )
        approved_data = approved_response.json()

    # store the token in the cache with an expiration time (5 seconds)
    await aiocache_caching.set(transaction_token, True, ttl=5)

    logger.info(f"{approved_data} >>> {checkout_data} >>> {invoice_id}")
    return approved_data, checkout_data, invoice_id
