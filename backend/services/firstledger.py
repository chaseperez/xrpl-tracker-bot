import requests
import logging
from config import FIRSTLEDGER_API

logger = logging.getLogger(__name__)

def lookup_account(address):
    if not FIRSTLEDGER_API:
        logger.warning("FIRSTLEDGER_API is not set.")
        return None
    url = f"{FIRSTLEDGER_API}/account/{address}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching account info for {address}: {e}")
        return None
