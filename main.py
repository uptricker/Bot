from flask import Flask
import threading
import time
import json

app = Flask(__name__)

def load_cookie():
    with open("fbstate.json", "r") as f:
        return json.load(f)

def bot_loop():
    print("🤖 Bot is live. Listening for commands...")
    while True:
        time.sleep(5)
        print("✅ Running... waiting for new messages...")

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=bot_loop).start()
    app.run(host='0.0.0.0', port=10000)
