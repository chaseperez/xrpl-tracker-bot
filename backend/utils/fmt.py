def fmt_wallet_list(wallets):
    lines = [f"- `{w.address}` (added {w.added_at.strftime('%Y-%m-%d')})" for w in wallets]
    return "Your tracked wallets:\n" + "\n".join(lines) if wallets else "You have no wallets tracked."

def fmt_transaction(tx):
    return (
        f"💸 *TX:* `{tx['hash']}`\n"
        f"From `{tx['source']}` to `{tx['destination']}`\n"
        f"Amount: {tx['amount']} {tx['currency']}\n"
        f"Timestamp: {tx['timestamp']}"
    )

# backend/utils/formatters.py

def dummy():
    pass
