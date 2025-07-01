import os
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN missing")

chat_id_raw = os.environ.get("TELEGRAM_CHAT_ID")
if not chat_id_raw:
    raise RuntimeError("❌ TELEGRAM_CHAT_ID missing")

try:
    TELEGRAM_CHAT_ID = int(chat_id_raw)
except ValueError:
    raise RuntimeError("❌ TELEGRAM_CHAT_ID must be an integer")

DB_URI = os.environ.get("DATABASE_URL")
if not DB_URI:
    raise RuntimeError("❌ DATABASE_URL missing")

import os
DB_URI = os.getenv("DATABASE_URL")  # Must be set in your Railway env or .env file

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URI = os.getenv("DATABASE_URL")
XRPL_HORIZON_URL = os.getenv("XRPL_HORIZON_URL", "https://s.altnet.rippletest.net:51234/")
DEX_SCREEENER_API = os.getenv("DEX_SCREENER_API", None)  # Optional
FIRSTLEDGER_API = os.getenv("FIRSTLEDGER_API", None)
