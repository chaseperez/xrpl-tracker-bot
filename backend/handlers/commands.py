from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Bot is connected.")

# Export a list of handlers to register
handlers = [
    CommandHandler("start", start),
    # Add more handlers here...
]



from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db.models import Wallet
from sqlalchemy.orm import Session
from utils import fmt_wallet_list, fmt_transaction






def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Welcome! Use /track <XRPL_ADDRESS> to start tracking.")

def track(update: Update, context: CallbackContext):
    session: Session = context.bot_data["db"]
    chat_id = str(update.effective_chat.id)
    if not context.args:
        return update.message.reply_text("Usage: /track <XRPL wallet address>")
    address = context.args[0]
    wallet = session.query(Wallet).filter_by(chat_id=chat_id, address=address).first()
    if wallet:
        return update.message.reply_text("You're already tracking that address!")
    session.add(Wallet(chat_id=chat_id, address=address))
    session.commit()
    update.message.reply_text(f"Now tracking `{address}`. {fmt_wallet_list(session.query(Wallet).filter_by(chat_id=chat_id).all())}", parse_mode="Markdown")

def untrack(update: Update, context: CallbackContext):
    session: Session = context.bot_data["db"]
    chat_id = str(update.effective_chat.id)
    if not context.args:
        return update.message.reply_text("Usage: /untrack <XRPL_ADDRESS>")
    address = context.args[0]
    wallet = session.query(Wallet).filter_by(chat_id=chat_id, address=address).first()
    if not wallet:
        return update.message.reply_text("That address wasn't tracked!")
    session.delete(wallet)
    session.commit()
    update.message.reply_text(f"Stopped tracking `{address}`. {fmt_wallet_list(session.query(Wallet).filter_by(chat_id=chat_id).all())}", parse_mode="Markdown")

def list_wallets(update: Update, context: CallbackContext):
    session: Session = context.bot_data["db"]
    chat_id = str(update.effective_chat.id)
    wallets = session.query(Wallet).filter_by(chat_id=chat_id).all()
    update.message.reply_text(fmt_wallet_list(wallets), parse_mode="Markdown")


async def start(update, context):
    print(f"Received /start from user {update.effective_user.id}")
    await update.message.reply_text("Hello! Bot started.")
