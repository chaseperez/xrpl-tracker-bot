from backend.bot import main

if __name__ == "__main__":
    main()


    

    from flask import Flask
from bot import send_startup_message
import threading
from handlers.tracker import start_tracker  # Wallet tracker logic

app = Flask(__name__)

@app.before_first_request
def start_background_tasks():
    threading.Thread(target=start_tracker, daemon=True).start()
    send_startup_message()

@app.route('/')
def index():
    return "Bot is running"

if __name__ == "__main__":
    app.run(debug=True)
