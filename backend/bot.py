from config import BOT_TOKEN, CHAT_ID, DB_URI
from handlers import commands, tracker
from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.clipboard import decode_clip_payload

from telegram import Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

from flask import Flask
import logging
import threading
import os

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Flask App (for Railway) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ XRPL Tracker Bot is Running on Railway"

# --- Async Telegram Command Handlers ---
async def start(update, context):
    await update.message.reply_text("🚀 Bot started and connected!")

# --- Send a Startup Message to Telegram ---
def send_startup_message():
    try:
        bot = Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text="🚀 Bot started and running!")
    except Exception as e:
        logging.error(f"❌ Failed to send startup message: {e}")

# --- Telegram Bot Setup ---
def run_bot():
    try:
        # Database setup
        engine = create_engine(DB_URI, echo=False)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        session = Session()

        # Initialize bot
        app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
        app_bot.bot_data["db"] = session

        # Add command handlers
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CommandHandler("track", commands.track))
        app_bot.add_handler(CommandHandler("untrack", commands.untrack))
        app_bot.add_handler(CommandHandler("list", commands.list_wallets))

        # Add inline button handler
        app_bot.add_handler(CallbackQueryHandler(
            lambda update, context: update.callback_query.answer(
                decode_clip_payload(update.callback_query.data)
            )
        ))

        # Add periodic wallet checker job
        app_bot.job_queue.run_repeating(
            tracker.check_wallets,
            interval=60,
            first=10,
            context={"chat_id": CHAT_ID}
        )

        logging.info("🤖 Telegram bot polling started...")
        send_startup_message()
        app_bot.run_polling()

    except Exception as e:
        logging.error(f"❌ Error starting Telegram bot: {e}")

# --- Main Entrypoint ---
if __name__ == "__main__":
    # Start bot in separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Run Flask server for Railway ping
    port = int(os.environ.get("PORT", 8000))  # Railway auto-sets $PORT
    logging.info(f"🌐 Flask server starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
