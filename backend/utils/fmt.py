# backend/utils/formatters.py

def fmt_wallet_list(wallets):
    if not wallets:
        return "🔍 You're not tracking any wallets yet."
    return "\n".join(
        [f"• `{w.address}`{' — ' + w.name if w.name else ''}" for w in wallets]
    )

def fmt_transaction(tx):
    return (
   f"💸 *TX:* `{tx.get('hash')}`\n"
f"From `{tx.get('source')}` to `{tx.get('destination')}`\n"
f"Amount: {tx.get('amount')} {tx.get('currency')}`\n"
f"Timestamp: {tx.get('timestamp')}'"
    )