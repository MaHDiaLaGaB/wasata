import logging
from fastapi import APIRouter, status, Depends, HTTPException
from .routes import BUY
from app.db.schemas import UserCreate, UserGet, StatusEntity
from http import HTTPStatus
from app.db.database_engine import UserDB
from app.core.config import config
from app.services.user_bl import UserBL
from app.api.dependencies import BinanceWa
from app.exceptions import BadRequest, AdminTokenRunOut
from app.utils.helper_function import payment_getaway

logger = logging.getLogger(__name__)

route = APIRouter(tags=["users"])

user_db = UserDB()


@route.post(
    BUY,
    status_code=HTTPStatus.CREATED,
)
def create(
    *,
    user: UserCreate,
    user_bl: UserBL = Depends(),
    binance_end: BinanceWa = Depends(),
) -> UserGet:
    # set the user status to Buying
    # UserGet.status = StatusEntity.ACTIVE

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
        if float(balance["asset"]) <= user.tokens:
            raise AdminTokenRunOut()

    logging.info(f"Adding new user {user}")
    if user.tokens <= 0:
        raise ValueError("Price must be greater than 0")

    # TODO here i will read the payment response
    res = payment_getaway()
    if res:
        logger.info("sending info to binance to start sending ... ")

    # Because of testing will comment the binance withdraw
    # binance_end.withdraw(coin=config.COIN, amount=user.tokens, to_address=user.wallet_address, network=None)

    # UserGet.status = StatusEntity.INACTIVE

    return user_bl.create_user(user)
