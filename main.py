
import time
import json

def load_cookie():
    with open("fbstate.json", "r") as f:
        return json.load(f)

def main():
    print("🤖 Bot is live. Listening for commands...")
    # Placeholder bot loop (simulate)
    while True:
        time.sleep(5)
        print("✅ Running... waiting for new messages...")

if __name__ == "__main__":
    main()
