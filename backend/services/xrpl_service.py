
import requests
from config import XRPL_HORIZON_URL

def get_account_tx(address, limit=10):
    payload = {
        "method": "account_tx",
        "params": [{"account": address, "ledger_index_min": -1, "ledger_index_max": -1, "limit": limit}]
    }
    r = requests.post(XRPL_HORIZON_URL, json=payload)
    r.raise_for_status()
    return r.json()["result"]["transactions"]