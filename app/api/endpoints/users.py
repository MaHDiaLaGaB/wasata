import logging
import uuid

from fastapi import APIRouter, status, Depends, HTTPException, Body, Query
from .routes import BUY
from app.db.schemas import UserCreate, UserGet, StatusEntity
from app.db.sessions import AdminRepository
from http import HTTPStatus

from app.core.config import config
from app.services.user_bl import UserBL
from app.services.payments import payment_getaway
from app.api.dependencies import BinanceWa
from app.exceptions import BadRequest, AdminTokenRunOut, Conflict, ObjectNotFound

logger = logging.getLogger(__name__)

route = APIRouter(tags=["users"])


@route.post(BUY, status_code=HTTPStatus.CREATED)
async def create(
    *,
    user: UserCreate = Body(),
    user_bl: UserBL = Depends(),
    binance_end: BinanceWa = Depends(),
    admin_repository: AdminRepository = Depends(),
    admin_username: str = Query(),
    wallet_address: str = Query(),
) -> UserGet:
    if user.user_status == StatusEntity.ACTIVE:
        raise Conflict(description="it's duple request")
    # check binance connection
    if not binance_end.check_connection():
        raise HTTPException(
            detail="no connection can't connect with binance client",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user.user_status = StatusEntity.ACTIVE

    # check the binance wallet and account is active and not blocked
    if not binance_end.check_account():
        raise BadRequest(description="the account is not active")

    # check if user usdt request is more than wasata balance
    balance = binance_end.get_balance(coin=config.COIN)
    if balance:
        if float(balance[config.COIN]) <= user.tokens:
            raise AdminTokenRunOut(
                description="Wasata's money is low please recharge your wallet"
            )

    logging.info(f"Adding new user ")
    if user.tokens <= 0:
        raise ValueError("Price must be greater than 0")
    if admin_username:
        try:
            usdt_price = admin_repository.get_admin_usdt_price_by_username(
                admin_username
            )
            user.price = usdt_price
        except ObjectNotFound:
            raise BadRequest(description="No admin found with the provided username")
    else:
        raise BadRequest(description="Admin username must be provided")

    logger.info(
        f"the user with phone number {user.phone_number} buy with price {user.price}"
    )
    to_pay_in_LYD = user.tokens * float(usdt_price)
    user.invoice_id = uuid.uuid4()
    logger.info("release an invoice id using uuid4 ... ")
    # TODO here i will read the payment response
    res, checkout, invoice_id = await payment_getaway(
        usdt_price=to_pay_in_LYD, invoice_id=str(user.invoice_id)
    )
    if res:
        logger.info(
            f"sending info to binance to start sending to {wallet_address} under invoice >> {invoice_id} ... "
        )

    # TODO Because of testing, will comment the binance withdraw
    # binance_end.withdraw(coin=config.COIN, amount=user.tokens, to_address=wallet_address, network=None)

    user.price = usdt_price  # type: ignore
    user.user_status = StatusEntity.INACTIVE
    logger.info("now we will create user")
    created_user = user_bl.create_user(user)
    logger.info("user created")
    return created_user
