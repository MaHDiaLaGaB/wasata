from fastapi import status, HTTPException
from app.core.config import config
from typing import Tuple, Any
from datetime import datetime
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


class PaymentGetaway:
    def __init__(self, hostname: str):
        self.hostname = hostname

    # check moamalat api if it's up
    async def health_check(self):
        async with httpx.AsyncClient() as client:
            logger.info("checking moamalat container")
            req = client.build_request("GET", url=f"http://{self.hostname}:3030/health")
            health = await client.send(req, stream=True)

            if health.json() == "OK":
                logger.info("moamalat is up ... ")
                return True
            else:
                return False

    # checkout
    async def checkout(self, usdt_price, invoice_id):
        await self.health_check()
        async with httpx.AsyncClient() as client:
            checkout_request = client.build_request(
                "post",
                url=config.MO3AMALAT_CHECKOUT.format(host=self.hostname),
                json={
                    "amount": usdt_price,
                    "reference": invoice_id,
                    "date": datetime.now()
                },
            )
            checkout_data = await client.send(checkout_request, stream=True)
            if checkout_data:
                return checkout_data

    # approval
    async def approved(self, invoice_id):
        await self.health_check()
        async with httpx.AsyncClient() as client:
            approved_request = client.build_request(
                "post",
                url=config.MOAMALAT_TRANSACTIONS_APPROVED.format(host=self.hostname),
                json={
                    "reference": invoice_id,
                },
            )
            approved_data = await client.send(approved_request, stream=True)
            if approved_data:
                return approved_data


pay_getaway = PaymentGetaway(hostname="moamalat")


async def payment_getaway(usdt_price: float, invoice_id: str) -> Tuple[Any, Any, str]:
    # generate a unique token for the transaction
    transaction_token = str(uuid.uuid4())

    # check if the token exists in the cache
    if await aiocache_caching.get(transaction_token):
        raise HTTPException(
            detail="Duplicate transaction request",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    checkout_resp = await pay_getaway.checkout(usdt_price=usdt_price, invoice_id=invoice_id)
    approved_resp = await pay_getaway.approved(invoice_id=invoice_id)

    # store the token in the cache with an expiration time (5 seconds)
    await aiocache_caching.set(transaction_token, True, ttl=5)

    logger.info(f"{checkout_resp} >>> {approved_resp} >>> {invoice_id}")
    return checkout_resp, approved_resp, invoice_id
