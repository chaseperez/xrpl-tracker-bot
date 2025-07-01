import requests
from config import DEX_SCREEENER_API

def get_token_info(token_address):
    if not DEX_SCREEENER_API:
        return None
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    r = requests.get(url)
    return r.json()