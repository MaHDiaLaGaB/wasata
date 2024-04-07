import logging
import uuid

from fastapi import APIRouter, status, Depends, HTTPException, Body, Query
from .routes import BUY
from db.schemas import UserCreate, UserGet, StatusEntity
from db.sessions import AdminRepository
from http import HTTPStatus
from core.config import config
from services.user_bl import UserBL
from services.wallet import wallet_validator
from api.binance_client import BinanceWa
from api.tlync_client import TlyncClient
from cus_exceptions import BadRequest, AdminTokenRunOut, Conflict, ObjectNotFound

logger = logging.getLogger(__name__)

route = APIRouter(tags=["users"])


async def validate_user_request(user: UserCreate):
    logger.info("validating the user request ...")
    if user.user_status == StatusEntity.ACTIVE:
        raise Conflict(description="Duplicate request detected.")
    if user.tokens <= 0:
        raise ValueError("Token amount must be greater than 0")


async def check_binance_connection(binance_end: BinanceWa):
    logger.info("Binance connection checking ...")
    if not binance_end.check_connection():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to connect with Binance client.",
        )


async def validate_wallet_address(wallet_address: str):
    logger.info("Validating the wallet address ...")
    if not await wallet_validator(wallet_address=wallet_address):
        raise BadRequest(
            description="Invalid wallet address. Please check the steps and provide a valid BNB wallet address."
        )


async def calculate_usdt_price(admin_repository: AdminRepository, admin_username: str, tokens: float) -> float:
    logger.info("Calculating the USDT price ...")
    try:
        usdt_price = admin_repository.get_admin_usdt_price_by_username(admin_username)
    except ObjectNotFound:
        raise BadRequest(description="No admin found with the provided username")
    if not usdt_price:
        raise BadRequest(description="Admin username must be provided")
    return float(usdt_price) * tokens


async def process_user_payment(
    user: UserCreate, binance_end: BinanceWa, tlync_end: TlyncClient,
    admin_repository: AdminRepository, admin_username: str, wallet_address: str
):
    # Ensure binance account is active
    if not binance_end.check_account():
        raise BadRequest(description="The Binance account is not active.")

    # Calculate and set the user's price based on admin's USDT price
    user.price = await calculate_usdt_price(admin_repository, admin_username, user.tokens)

    total_price = user.tokens * float(user.price)
    user.invoice_id = uuid.uuid4()
    logger.info(f"the wallet address id: {wallet_address}")
    tlync_response = tlync_end.initiate_payment(
        store_id=config.TLINC_STORE_ID,
        backend_url="http://localhost:8080",
        frontend_url="http://localhost:3000",
        phone=user.phone_number,
        custom_ref=str(user.invoice_id),
        amount=total_price
    )
    logger.info(f"Response from Tlync: {tlync_response}")


# Dependency provider function
def get_payment_api():
    tlync_end = TlyncClient(is_test_environment=True)
    tlync_end.set_token(config.TLYNC_TOKEN)
    return tlync_end


@route.post(BUY, status_code=HTTPStatus.CREATED)
async def create_user_purchase(
        *,
        user: UserCreate = Body(),
        user_bl: UserBL = Depends(),
        binance_end: BinanceWa = Depends(),
        tlync_end: TlyncClient = Depends(get_payment_api),
        admin_repository: AdminRepository = Depends(),
        admin_username: str = Query(),
        wallet_address: str = Query(),
) -> UserGet:
    try:
        await validate_user_request(user)
        await check_binance_connection(binance_end)
        await validate_wallet_address(wallet_address)
        user.user_status = StatusEntity.ACTIVE
        await process_user_payment(user, binance_end, tlync_end, admin_repository, admin_username, wallet_address)
    except (Conflict, BadRequest, AdminTokenRunOut, ValueError) as e:
        logger.error(f"Error processing user purchase: {e.description}")
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Unexpected error occurred")

    logger.info("User purchase processed successfully")
    user.price = await calculate_usdt_price(admin_repository, admin_username, user.tokens)
    user.user_status = StatusEntity.INACTIVE
    created_user = user_bl.create_user(user)
    return created_user



# @route.post("/buy", status_code=HTTPStatus.CREATED)
# async def create(
#         *,
#         user: UserCreate = Body(),
#         user_bl: UserBL = Depends(),
#         binance_end: BinanceWa = Depends(),
#         tlync_end: TlyncClient = Depends(get_payment_api),
#         admin_repository: AdminRepository = Depends(),
#         admin_username: str = Query(),
#         wallet_address: str = Query(),
# ) -> UserGet:
#     if user.user_state == StatusEntity.ACTIVE:
#         raise Conflict(description="it's duple request")
#     # check binance connection
#     if not binance_end.check_connection():
#         raise HTTPException(
#             detail="no connection can't connect with binance client",
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )
#
#     if not wallet_validator(wallet_address=wallet_address):
#         raise BadRequest(
#             description="invalid wallet addres please check the steps and provide BNB wallet address"
#         )
#
#     user.user_state = StatusEntity.ACTIVE
#
#     # check the binance wallet and account is active and not blocked
#     if not binance_end.check_account():
#         raise BadRequest(description="the account is not active")
#
#     # check if user usdt request is more than wasata balance
#     balance = binance_end.get_balance(coin=config.COIN)
#     if balance:
#         if float(balance[config.COIN]) <= user.tokens:
#             raise AdminTokenRunOut(
#                 description="Wasata's money is low please recharge your wallet"
#             )
#
#     logging.info(f"Adding new user ")
#     if user.tokens <= 0:
#         raise ValueError("Price must be greater than 0")
#     if admin_username:
#         try:
#             usdt_price = admin_repository.get_admin_usdt_price_by_username(
#                 admin_username
#             )
#             user.price = usdt_price
#         except ObjectNotFound:
#             raise BadRequest(description="No admin found with the provided username")
#     else:
#         raise BadRequest(description="Admin username must be provided")
#
#     logger.info(
#         f"the user with phone number {user.phone_number} buy with price {user.price}"
#     )
#     total_price = user.tokens * float(usdt_price)
#     logger.info(f"libyan price is >>> {total_price}")
#     user.invoice_id = uuid.uuid4()
#     logger.info("release an invoice id using uuid4 ... ")
#     # TODO here i will read the payment response
#     # here should have a function to start the user payment in the frontend/
#     # and if the payment done successfully i will continue executing this function and sell my product
#     tlync_response = tlync_end.initiate_payment(store_id=config.TLINC_STORE_ID,
#                                                 backend_url="http://localhost:8080",
#                                                 frontend_url="http://localhost:3000",
#                                                 phone=user.phone_number,
#                                                 custom_ref=user.invoice_id,
#                                                 amount=total_price)
#     # TODO Because of testing, will comment the binance withdraw
#     logger.info(f"the response of the tylinc {tlync_response}")
#     # binance_end.withdraw(coin=config.COIN, amount=user.tokens, to_address=wallet_address, network="BSC")
#
#     user.price = usdt_price  # type: ignore
#     user.user_state = StatusEntity.INACTIVE
#     logger.info("now we will create user")
#     created_user = user_bl.create_user(user)
#     created_user.total_price = total_price
#     logger.info("user created")
#     return created_user
