from app.core.config import config
from app.exceptions import BSCANClientError
from bscscan import BscScan
import logging

logger = logging.getLogger(__name__)


async def wallet_validator(wallet_address: str) -> bool:
    try:
        async with BscScan(config.BSCAN_API_KEY) as client:
            resp = await client.get_bnb_balance(address=wallet_address)
            return isinstance(resp, str) and float(resp) >= 0.0
    except BSCANClientError as e:
        logger.error(f"Error occurred: {e}")
        return False
