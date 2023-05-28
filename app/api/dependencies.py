"""
 Contains dependency functions, such as authentication, authorization, or database session management.
"""
import traceback

import logging
from typing import Dict
from binance.spot import Spot as Client
from binance.error import ClientError
from app.exceptions import ServiceUnavailable, BadRequest

logger = logging.getLogger(__name__)


class BinanceWa:
    def __init__(self, binance_api_key: str, binance_api_secret: str, base_url: str) -> None:
        self.client = Client(binance_api_key, binance_api_secret, base_url=base_url)

    def check_connection(self) -> bool:
        try:
            if self.client.ping() == {}:
                return True
        except ClientError as e:
            logger.error(f"server not connected {e}")
            raise BadRequest(description="no connection")

    def check_system(self) -> bool:
        try:
            res = self.client.system_status()
            if res["status"] == 1:
                logger.error("system is down or under maintenance")
                raise BadRequest(description="system is down or under maintenance")
            logger.info("the system is up and ready")
            return True
        except KeyError:
            logger.error("Failed to retrieve system status")

    def check_account(self) -> bool | None:
        try:
            if self.check_system():
                res = self.client.account()
                assert res["accountType"] == "SPOT"
                if res["canWithdraw"] is False:
                    raise ServiceUnavailable(
                        description="Your account can not withdraw at the moment"
                    )
                return True
        except ClientError as e:
            logger.error(f"Error fetching balance: {e}")
            traceback.print_exc()
            raise BadRequest("something went wrong checking the account")
        return None

    # TODO add check_connection after test it
    def get_balance(self, coin: str) -> Dict[str, float] | None:
        try:
            res = self.client.account()
            x = res["balances"]
            for asset in x:
                if asset["asset"] == coin:
                    return dict({f"{asset['asset']}": float(f"{asset['free']}")})

        except ClientError as error:
            logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            raise BadRequest(description="balance error")
        return None

    def withdraw(self, coin: str, amount: float, to_address: str, network: str | None):
        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")

            response = self.client.withdraw(
                coin=coin, amount=amount, address=to_address, network=network
            )
            return response
        except ClientError as e:
            logger.error(f"Error withdrawing {coin}: {e}")
            traceback.print_exc()
            raise BadRequest(description="something went wrong while withdrawing ...")
