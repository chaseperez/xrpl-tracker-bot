from telegram.ext import CallbackContext
from db.models import Wallet
from services.xrpl_service import get_account_tx
from services.dex_screener import get_token_info
from services.firstledger import lookup_account
from utils.fmt import fmt_transaction
from telegram.constants import ParseMode
import logging

logger = logging.getLogger(__name__)

def check_wallets(context: CallbackContext):
    session = context.bot_data["db"]
    bot = context.bot

    # 🔔 Optional: send test message on every run
    try:
        bot.send_message(
            chat_id=int(context.job.context["chat_id"]),
            text="✅ Wallet tracker check initiated.",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.warning(f"Could not send test message: {e}")

    for wallet in session.query(Wallet).all():
        try:
            txs = get_account_tx(wallet.address, limit=5)
            for tx_item in reversed(txs):
                tx = tx_item.get("tx", {})
                if not tx.get("hash"):
                    continue  # Skip invalid tx

                msg = fmt_transaction({
                    "hash": tx.get("hash"),
                    "source": tx.get("Account"),
                    "destination": tx.get("Destination"),
                    "amount": (
                        tx.get("Amount") if isinstance(tx.get("Amount"), str)
                        else tx.get("Amount", {}).get("value")
                    ),
                    "currency": (
                        "XRP" if isinstance(tx.get("Amount"), str)
                        else tx.get("Amount", {}).get("currency")
                    ),
                    "timestamp": tx_item.get("date")
                })

                bot.send_message(
                    chat_id=int(wallet.chat_id),
                    text=msg,
                    parse_mode=ParseMode.MARKDOWN
                )

                # 🔍 Optional: fetch token info if present
                ti = get_token_info(tx.get("Destination"))
                if ti:
                    bot.send_message(
                        chat_id=int(wallet.chat_id),
                        text=f"*Token info:* {ti}",
                        parse_mode=ParseMode.MARKDOWN
                    )
        except Exception as e:
            logger.error(f"Error checking wallet {wallet.address}: {e}")
