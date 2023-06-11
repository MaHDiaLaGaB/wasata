from app.exceptions import BadRequest
from app.api.dependencies import BinanceWa
from app.utils.helper_function import payment_getaway, aiocache_caching
import asyncio
import pytest


def test_get_account(spot_binance_api: BinanceWa) -> None:
    with pytest.raises(BadRequest):
        res = spot_binance_api.check_account()
        print(res)
        assert res is False


def test_get_balance(spot3_binance_api: BinanceWa) -> None:
    print(spot3_binance_api.client.api_key)
    res = spot3_binance_api.get_balance("USDT")

    assert res["USDT"] == 0


def test_get_ping(spot3_binance_api: BinanceWa) -> None:
    res = spot3_binance_api.check_connection()
    assert res is True


def test_check_system(spot3_binance_api: BinanceWa) -> None:
    res = spot3_binance_api.check_system()
    assert res is True


def test_check_account(spot3_binance_api: BinanceWa) -> None:
    res = spot3_binance_api.get_balance("USDT")
    assert res["USDT"] == 30


@pytest.mark.asyncio
async def test_payment_getaway_caching(test_app):
    # Call the payment_getaway function with a sample usdt_price
    usdt_price = 100.0
    transaction_token = await payment_getaway(usdt_price)

    # Check if the transaction token is stored in the cache
    assert await aiocache_caching.get(transaction_token) is not None

    # Check if the transaction token expires after the specified time (e.g., 5 minutes)
    await asyncio.sleep(6)  # Sleep for 6 seconds (5 seconds + 1 second)
    assert await aiocache_caching.get(transaction_token) is None
