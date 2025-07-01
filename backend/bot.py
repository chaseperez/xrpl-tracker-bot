import os
print("Current working directory:", os.getcwd())
print("Listing files in current directory:", os.listdir('.'))
print("Listing files in parent directory:", os.listdir('..'))

# Then you can use engine.connect() or ORM sessions here

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, JobQueue
from config import BOT_TOKEN
from handlers import commands, tracker
from db.models import Base, Wallet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.clipboard import decode_clip_payload
from db.db import engine

def main():
    engine = create_engine(BOT_URI := BOT_TOKEN and BOT_TOKEN or "", echo=False)
    Session = sessionmaker(bind=create_engine(BOT_URI := BOT_TOKEN and "", echo=False))
    engine = create_engine(BOT_URI := "", echo=False)  # fix DB_URI usage
    from config import DB_URI
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
    session = Session()

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.bot_data["db"] = session

    dp.add_handler(CommandHandler("start", commands.start))
    dp.add_handler(CommandHandler("track", commands.track))
    dp.add_handler(CommandHandler("untrack", commands.untrack))
    dp.add_handler(CommandHandler("list", commands.list_wallets))
    dp.add_handler(CallbackQueryHandler(on_clip := lambda update, _: update.callback_query.answer(decode_clip_payload(update.callback_query.data))))

    jq: JobQueue = updater.job_queue
    jq.run_repeating(tracker.check_wallets, interval=60, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

