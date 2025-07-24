from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from db.models import Wallet
from utils import fmt_wallet_list
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 Welcome! Use /track <XRPL_ADDRESS> [NAME] to start tracking.")

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    SessionLocal = context.bot_data["SessionLocal"]
    session = SessionLocal()
    try:
        chat_id = str(update.effective_chat.id)
        if not context.args:
            await update.message.reply_text("Usage: /track <ADDRESS> [NAME]")
            return

        address = context.args[0]
        name = " ".join(context.args[1:]) if len(context.args) > 1 else None

        wallet = session.query(Wallet).filter_by(chat_id=chat_id, address=address).first()
        if wallet:
            await update.message.reply_text("You're already tracking this address.")
            return

        session.add(Wallet(chat_id=chat_id, address=address, name=name))
        session.commit()

        await update.message.reply_text(
            f"✅ Now tracking `{address}`{' as *' + name + '*' if name else ''}.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in /track: {e}")
        await update.message.reply_text("❌ An error occurred while tracking the wallet.")
    finally:
        session.close()

async def untrack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    SessionLocal = context.bot_data["SessionLocal"]
    session = SessionLocal()
    try:
        chat_id = str(update.effective_chat.id)
        if not context.args:
            await update.message.reply_text("Usage: /untrack <ADDRESS>")
            return

        address = context.args[0]
        wallet = session.query(Wallet).filter_by(chat_id=chat_id, address=address).first()
        if not wallet:
            await update.message.reply_text("That address is not being tracked.")
            return

        session.delete(wallet)
        session.commit()
        await update.message.reply_text(f"🗑️ Untracked `{address}`", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in /untrack: {e}")
        await update.message.reply_text("❌ An error occurred while untracking the wallet.")
    finally:
        session.close()

async def list_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    SessionLocal = context.bot_data["SessionLocal"]
    session = SessionLocal()
    try:
        chat_id = str(update.effective_chat.id)
        wallets = session.query(Wallet).filter_by(chat_id=chat_id).all()

        buttons = [
            [InlineKeyboardButton(f"❌ {w.name or w.address}", callback_data=f"untrack|{w.address}")]
            for w in wallets
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(
            fmt_wallet_list(wallets),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in /list: {e}")
        await update.message.reply_text("❌ An error occurred while listing wallets.")
    finally:
        session.close()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    SessionLocal = context.bot_data["SessionLocal"]
    session = SessionLocal()
    query = update.callback_query
    await query.answer()

    try:
        chat_id = str(query.message.chat_id)
        data = query.data

        if data.startswith("untrack|"):
            address = data.split("|")[1]
            wallet = session.query(Wallet).filter_by(chat_id=chat_id, address=address).first()
            if wallet:
                session.delete(wallet)
                session.commit()
                await query.edit_message_text(f"✅ Untracked `{address}`", parse_mode="Markdown")
            else:
                await query.edit_message_text("❌ Wallet not found.")
    except Exception as e:
        logger.error(f"Error handling callback: {e}")
        await query.edit_message_text("❌ An error occurred.")
    finally:
        session.close()

# Global error handler for the bot application
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    # Optionally notify the user
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text("❌ An unexpected error occurred. Please try again later.")

# Export command + callback handlers
handlers = [
    CommandHandler("start", start),
    CommandHandler("track", track),
    CommandHandler("untrack", untrack),
    CommandHandler("list", list_wallets),
    CallbackQueryHandler(handle_callback),
]
