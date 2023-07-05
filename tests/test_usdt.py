from app.api.dependencies import BinanceWa
from app.services.wallet import wallet_validator
from fastapi import HTTPException

from .cont import CORRECT_WALLET_ADDRESS, WRONG_WALLET_ADDRESS, INCORRECT_WALLET_ADDRESS

from app.services.payments import payment_getaway
import pytest

from unittest.mock import MagicMock, patch


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


@pytest.mark.asyncio
async def test_payment_getaway():
    # mock the functions like uuid and payments
    with patch("uuid.uuid4", return_value="test_token"):
        with patch(
            "app.services.payments.aiocache_caching.get",
            new_callable=AsyncMock,
            return_value=None,
        ) as mock_get, patch(
            "app.services.payments.aiocache_caching.set", new_callable=AsyncMock
        ) as mock_set:
            with patch(
                "app.services.payments.pay_getaway.checkout",
                new_callable=AsyncMock,
                return_value="checkout_resp",
            ) as mock_checkout, patch(
                "app.services.payments.pay_getaway.approved",
                new_callable=AsyncMock,
                return_value="approved_resp",
            ) as mock_approved:
                # call the function
                checkout_resp, approved_resp, invoice_id = await payment_getaway(
                    1.0, "invoice_id"
                )

                # assert the results
                assert checkout_resp == "checkout_resp"
                assert approved_resp == "approved_resp"
                assert invoice_id == "invoice_id"

                # assert the methods were called with the correct arguments
                mock_get.assert_called_once_with("test_token")
                mock_set.assert_called_once_with("test_token", True, ttl=5)
                mock_checkout.assert_called_once_with(
                    usdt_price=1.0, invoice_id="invoice_id"
                )
                mock_approved.assert_called_once_with(invoice_id="invoice_id")


@pytest.mark.asyncio
async def test_payment_getaway_duplicate_transaction():
    with patch("uuid.uuid4", return_value="test_token"):
        with patch(
            "app.services.payments.aiocache_caching.get",
            new_callable=AsyncMock,
            return_value=True,
        ):
            with pytest.raises(HTTPException) as exc_info:
                await payment_getaway(1.0, "invoice_id")

            assert exc_info.value.detail == "Duplicate transaction request"
            assert exc_info.value.status_code == 400


# testing the binance class
def test_get_account(spot3_binance_api: BinanceWa) -> None:
    res = spot3_binance_api.check_account()
    assert res is True


def test_get_ping(spot3_binance_api: BinanceWa) -> None:
    res = spot3_binance_api.check_connection()
    assert res is True


def test_check_system(spot3_binance_api: BinanceWa) -> None:
    res = spot3_binance_api.check_system()
    assert res is True


@pytest.mark.asyncio
async def test_wallet_valedator() -> None:
    res = await wallet_validator(CORRECT_WALLET_ADDRESS)
    print(res)
    assert res is True

    resp = await wallet_validator(WRONG_WALLET_ADDRESS)
    assert resp is False
    #
    response = await wallet_validator(INCORRECT_WALLET_ADDRESS)
    assert response is False
