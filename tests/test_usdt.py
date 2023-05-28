import requests
import logging
from app.exceptions import ServiceUnavailable
import pytest


def test_get_account(spot_binance_api):
    with pytest.raises(ServiceUnavailable):
        res = spot_binance_api.check_account()
        print(res)
        assert res["accountType"] == "SPOT"
        assert res["canWithdraw"] is False


def test_get_balance(spot3_binance_api):
    res = spot3_binance_api.get_balance("USDT")
    assert res['USDT'] == 0


def test_get_ping(spot3_binance_api):

    res = spot3_binance_api.check_connection()
    assert res is True
