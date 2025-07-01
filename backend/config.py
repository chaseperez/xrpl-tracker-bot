import os
from dotenv import load_dotenv


TELEGRAM_BOT_TOKEN = os.environ.get("8038618967:AAGOKrOAtOdsmYqGiPCV47Z2y19iIVTlQIk")
TELEGRAM_CHAT_ID = int(os.environ.get("7861907274"))
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Missing BOT_TOKEN environment variable")

import os
DB_URI = os.getenv("DATABASE_URL")  # Must be set in your Railway env or .env file

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URI = os.getenv("DATABASE_URL")
XRPL_HORIZON_URL = os.getenv("XRPL_HORIZON_URL", "https://s.altnet.rippletest.net:51234/")
DEX_SCREEENER_API = os.getenv("DEX_SCREENER_API", None)  # Optional
FIRSTLEDGER_API = os.getenv("FIRSTLEDGER_API", None)
