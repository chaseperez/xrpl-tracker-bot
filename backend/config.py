import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URI = os.getenv("DATABASE_URL")
XRPL_HORIZON_URL = os.getenv("XRPL_HORIZON_URL", "https://s.altnet.rippletest.net:51234/")
DEX_SCREEENER_API = os.getenv("DEX_SCREENER_API", None)  # Optional
FIRSTLEDGER_API = os.getenv("FIRSTLEDGER_API", None)