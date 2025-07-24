# XRPL Wallet Tracker Bot — Refactored and Fixed Version

import pymysql
pymysql.install_as_MySQLdb()

import asyncio
import logging
import os
import threading
from dotenv import load_dotenv
from flask import Flask

# Load .env only locally
if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv()

# Required config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DB_URI = os.getenv("DATABASE_URL") or os.getenv("DB_URI")

# Validate config
if not BOT_TOKEN or not CHAT_ID or not DB_URI:
    raise RuntimeError("❌ BOT_TOKEN, CHAT_ID, or DB_URI is missing from environment variables.")

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Flask Health Check ---
app = Flask(__name__)

@app.route("/")
def health():
    return "✅ Bot is alive", 200

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

# --- Main Bot Logic ---
async def send_startup_message():
    from telegram import Bot
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text="🚀 Bot started and running!")
        logger.info("✅ Startup message sent")
    except Exception as e:
        logger.error(f"❌ Failed to send startup message: {e}")

async def run_bot():
    from telegram.ext import (
        ApplicationBuilder, CallbackQueryHandler, CommandHandler,
        MessageHandler, filters, ContextTypes
    )
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from db.models import Base
    from handlers import commands, tracker
    from utils.clipboard import decode_clip_payload
    from telegram import Update

    logger.info("🔧 Connecting to database...")
    engine = create_engine(DB_URI, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    logger.info("🤖 Initializing Telegram bot...")
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.bot_data["SessionLocal"] = SessionLocal

    # Register command handlers
    for handler in commands.handlers:
        app_bot.add_handler(handler)
    logger.info(f"✅ Registered {len(commands.handlers)} command handlers")

    # Add debug logger
    async def debug_logger(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.debug(f"📥 Message received: {update.message.text}")
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, debug_logger))

    # Inline button handler
    app_bot.add_handler(CallbackQueryHandler(
        lambda update, context: update.callback_query.answer(
            decode_clip_payload(update.callback_query.data)
        )
    ))

    # Job to check wallets
    app_bot.job_queue.run_repeating(
        tracker.check_wallets,
        interval=60,
        first=10,
        name="check_wallets_job",
        data={"chat_id": CHAT_ID}
    )
    logger.info("🕒 Scheduled job: check_wallets every 60s")

    # Global error handler
    app_bot.add_error_handler(commands.error_handler)

    await send_startup_message()
    logger.info("🤖 Telegram bot polling started...")
    await app_bot.run_polling()

# --- Entry Point ---
async def main():
    logger.info("🚀 Starting XRPL Tracker Bot...")

    # Start Flask health server in background
    threading.Thread(target=run_flask, daemon=True).start()

    # Run bot
    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
