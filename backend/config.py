import os
from dotenv import load_dotenv

# Load local .env only if running locally
load_dotenv()

# --- Required Config ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN missing")

CHAT_ID = os.getenv("CHAT_ID")
if not CHAT_ID:
    raise RuntimeError("❌ CHAT_ID missing")

DB_URI = os.getenv("DATABASE_URL")
if not DB_URI:
    raise RuntimeError("❌ DATABASE_URL missing")

# --- Optional APIs ---
XRPL_HORIZON_URL = os.getenv("XRPL_HORIZON_URL", "https://s.altnet.rippletest.net:51234/")
DEX_SCREENER_API = os.getenv("DEX_SCREENER_API")
FIRSTLEDGER_API = os.getenv("FIRSTLEDGER_API")
