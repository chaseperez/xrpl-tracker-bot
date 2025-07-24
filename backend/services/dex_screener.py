import requests
import logging
from config import DEX_SCREENER_API

logger = logging.getLogger(__name__)

def get_token_info(token_address):
    if not DEX_SCREENER_API:
        logger.warning("DEX_SCREENER_API is not set.")
        return None

    url = f"{DEX_SCREENER_API}/latest/dex/tokens/{token_address}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # raise exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching token info for {token_address}: {e}")
        return None
