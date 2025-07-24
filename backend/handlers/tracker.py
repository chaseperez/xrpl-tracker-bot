from telegram.ext import CallbackContext
from db.models import Wallet
from services.xrpl_service import get_account_tx
from services.dex_screener import get_token_info
from services.firstledger import lookup_account
from utils.fmt import fmt_transaction
from telegram.constants import ParseMode
import logging

logger = logging.getLogger(__name__)

# Helper: store last processed tx hashes in-memory (consider persisting in DB)
last_processed_hashes = {}

def split_message(text, limit=4000):
    """
    Utility to split long messages into chunks under Telegram's limit.
    Splits on double newline or single newline where possible.
    """
    if len(text) <= limit:
        return [text]

    chunks = []
    while len(text) > limit:
        split_pos = text.rfind('\n\n', 0, limit)
        if split_pos == -1:
            split_pos = text.rfind('\n', 0, limit)
        if split_pos == -1:
            split_pos = limit

        chunks.append(text[:split_pos].strip())
        text = text[split_pos:].strip()

    if text:
        chunks.append(text)

    return chunks

async def check_wallets(context: CallbackContext):
    SessionLocal = context.bot_data["SessionLocal"]
    bot = context.bot

    chat_id = getattr(getattr(context, "job", None), "data", {}).get("chat_id")
    if not chat_id:
        from config import CHAT_ID
        chat_id = CHAT_ID

    session = SessionLocal()
    try:
        wallets = session.query(Wallet).all()

        for wallet in wallets:
            try:
                wallet_id = wallet.id
                wallet_last_hashes = last_processed_hashes.setdefault(wallet_id, set())

                txs = get_account_tx(wallet.address)  # or await if async

                messages = []
                for tx_item in reversed(txs):
                    tx = tx_item.get("tx", {})
                    tx_hash = tx.get("hash")
                    if not tx_hash or tx_hash in wallet_last_hashes:
                        continue
                    wallet_last_hashes.add(tx_hash)

                    msg_parts = []
                    tx_type = tx.get("TransactionType")

                    if tx_type == "TrustSet":
                        limit = tx.get("LimitAmount", {})
                        msg_parts.append(f"🔐 TrustLine set: {limit.get('currency')} issued by {limit.get('issuer')}")

                    elif tx_type == "Payment":
                        amt = tx.get("Amount")
                        if isinstance(amt, dict):
                            currency = amt.get("currency")
                            issuer = amt.get("issuer")
                            value = amt.get("value")
                            msg_parts.append(f"💰 Token Payment: {value} {currency} from {tx.get('Account')} to {tx.get('Destination')}")
                            info = get_token_info(f"{currency}:{issuer}")  # or await
                            if info:
                                msg_parts.append(f"📈 Token price: {info}")
                        else:
                            msg_parts.append(f"💸 XRP Payment: {amt} drops from {tx.get('Account')} to {tx.get('Destination')}")

                    if msg_parts:
                        messages.append(f"*TX:* `{tx_hash}`\n" + "\n".join(msg_parts))

                if messages:
                    batch = "\n\n".join(messages)
                    for chunk in split_message(batch):
                        await bot.send_message(chat_id=int(wallet.chat_id), text=chunk, parse_mode=ParseMode.MARKDOWN)

                trust_lines = lookup_account(wallet.address)
                if trust_lines:
                    trust_msg = f"*Trust Lines for {wallet.address}:*\n"
                    for tl in trust_lines:
                        trust_msg += f"- {tl['currency']} issued by {tl['issuer']} (Balance: {tl['balance']})\n"
                    await bot.send_message(chat_id=int(wallet.chat_id), text=trust_msg, parse_mode=ParseMode.MARKDOWN)

            except Exception as e:
                logger.error(f"❌ Error checking wallet {wallet.address}: {e}")
    finally:
        session.close()
