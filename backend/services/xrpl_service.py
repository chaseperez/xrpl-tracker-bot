import requests
import logging
from config import XRPL_HORIZON_URL

logger = logging.getLogger(__name__)

def get_account_tx(address, limit=10):
    payload = {
        "method": "account_tx",
        "params": [{
            "account": address,
            "ledger_index_min": -1,
            "ledger_index_max": -1,
            "limit": limit
        }]
    }
    try:
        r = requests.post(XRPL_HORIZON_URL, json=payload, timeout=5)
        r.raise_for_status()
        data = r.json()
        return data.get("result", {}).get("transactions", [])
    except requests.RequestException as e:
        logger.error(f"XRPL API request failed for address {address}: {e}")
        return []
