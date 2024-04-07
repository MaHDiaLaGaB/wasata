"""
 Contains dependency functions, such as authentication, authorization, or database session management.
"""
import traceback

import logging
from typing import Dict, Any
from binance.spot import Spot as Client
from core.config import config
from binance.error import ClientError
from cus_exceptions import ServiceUnavailable, BadRequest

logger = logging.getLogger(__name__)


class BinanceWa:
    def __init__(self) -> None:
        self.client = Client(
            api_key=config.BINANCE_API_KEY,
            api_secret=config.BINANCE_SECRETE_KEY,
            base_url=config.BINANCE_BASE_URL,
        )

    def check_connection(self) -> bool:
        try:
            if self.client.ping() == {}:
                return True
        except ClientError as e:
            logger.error(f"server not connected {e}")
            raise BadRequest(description="no connection")
        return False

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
        return False

    def check_account(self) -> bool:
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
        return False

    def get_balance(self, coin: str) -> Dict[str, float] | Dict[str, str]:
        try:
            if self.check_system():
                res = self.client.account()
                x = res["balances"]
                for asset in x:
                    if asset["asset"] == coin:
                        logger.info(f"my {asset['asset']}: {float(asset['free'])}")
                        return dict({f"{asset['asset']}": float(f"{asset['free']}")})
            else:
                logger.error("system error ...")
                raise BadRequest()

        except ClientError as error:
            logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            raise BadRequest(description="balance error")
        return dict({f"{coin}": "No asset"})

    def withdraw(
        self, coin: str, amount: float, to_address: str, network: str | None
    ) -> Any:
        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")

            res = self.client.withdraw(
                coin=coin, amount=amount, address=to_address, network=network
            )
            return res
        except ClientError as e:
            logger.error(f"Error withdrawing {coin}: {e}")
            traceback.print_exc()
            raise BadRequest(description="something went wrong while withdrawing ...")
