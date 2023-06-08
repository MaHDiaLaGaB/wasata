import logging
from fastapi import APIRouter, status, Depends, HTTPException, Body, Query
from .routes import BUY
from app.db.schemas import UserCreate
from http import HTTPStatus

from app.core.config import config
from app.services.user_bl import UserBL
from app.api.dependencies import BinanceWa
from app.exceptions import BadRequest, AdminTokenRunOut

# from app.utils.helper_function import payment_getaway

logger = logging.getLogger(__name__)

route = APIRouter(tags=["users"])


@route.post(BUY, status_code=HTTPStatus.CREATED)
def create(
    *,
    user: UserCreate = Body(),
    user_bl: UserBL = Depends(),
    binance_end: BinanceWa = Depends(),
    wallet_address: str = Query(),
):

    # check binance connection
    if not binance_end.check_connection():
        raise HTTPException(
            detail="no connection can't connect with binance client",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # check the binance wallet and account is active and not blocked
    if not binance_end.check_account():
        raise BadRequest()

    # check if user usdt request is more than wasata balance
    balance = binance_end.get_balance(coin=config.COIN)
    if balance:
        print(balance[config.COIN])
        if float(balance[config.COIN]) <= user.tokens:
            raise AdminTokenRunOut()

    logging.info(f"Adding new user ")
    if user.tokens <= 0:
        raise ValueError("Price must be greater than 0")

    usdt_price = user.tokens * float(config.PRICE)

    # TODO here i will read the payment response
    # res = payment_getaway(usdt_price=usdt_price)
    if usdt_price:
        logger.info(
            f"sending info to binance to start sending to {wallet_address} ... "
        )

    # Because of testing will comment the binance withdraw
    # binance_end.withdraw(coin=config.COIN, amount=user.tokens, to_address=wallet_address, network=None)

    user.price = usdt_price
    created_user = user_bl.create_user(user)

    return created_user
