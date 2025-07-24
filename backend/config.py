import os
from dotenv import load_dotenv

# --- Load environment variables ---
# Only load from .env in local dev (Railway provides env vars automatically)
if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv()

# --- Required Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DB_URI = os.getenv("DATABASE_URL") or os.getenv("DB_URI")

# --- Validation ---
if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN is missing. Check your .env or Railway variables.")

if not CHAT_ID or not CHAT_ID.isdigit():
    raise RuntimeError("❌ CHAT_ID is missing or invalid. It must be a numeric Telegram user or group ID.")
CHAT_ID = int(CHAT_ID)

if not DB_URI:
    raise RuntimeError("❌ DATABASE_URL or DB_URI is missing. Set your database connection string.")

# --- Optional Configuration ---
XRPL_HORIZON_URL = os.getenv("XRPL_HORIZON_URL", "https://s.altnet.rippletest.net:51234/")
DEX_SCREENER_API = os.getenv("DEX_SCREENER_API")
FIRSTLEDGER_API = os.getenv("FIRSTLEDGER_API")
