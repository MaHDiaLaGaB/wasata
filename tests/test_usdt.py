from app.exceptions import BadRequest
from app.api.dependencies import BinanceWa
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
