
import requests
from config import FIRSTLEDGER_API

def lookup_account(address):
    if not FIRSTLEDGER_API:
        return None
    r = requests.get(f"{FIRSTLEDGER_API}/account/{address}")
    return r.json()