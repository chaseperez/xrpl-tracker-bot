
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    JobQueue
)
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DB_URI
from handlers import commands, tracker
from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.clipboard import decode_clip_payload
import logging

logging.basicConfig(level=logging.INFO)

# Send one-time startup message
def send_startup_message():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="🚀 Bot started and running!")

def main():
    engine = create_engine(DB_URI, echo=False)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.bot_data["db"] = session

    app.add_handler(CommandHandler("start", commands.start))
    app.add_handler(CommandHandler("track", commands.track))
    app.add_handler(CommandHandler("untrack", commands.untrack))
    app.add_handler(CommandHandler("list", commands.list_wallets))
    app.add_handler(CallbackQueryHandler(lambda update, context: update.callback_query.answer(
        decode_clip_payload(update.callback_query.data)
    )))

    job_queue = app.job_queue
    job_queue.run_repeating(tracker.check_wallets, interval=60, first=10)

    logging.info("🚀 Starting bot polling...")
    send_startup_message()
    app.run_polling()