import asyncio, json, re
from playwright.async_api import async_playwright
from flask import Flask
import threading

GROUP_URL = "https://www.facebook.com/messages/t/24292795350336668/"

app = Flask(__name__)

def start_bot_loop():
    asyncio.run(run_bot())

@app.route('/')
def home():
    return "🤖 Messenger Command Bot is Live!"

async def run_bot():
    print("🤖 Bot is live. Listening for commands...\n")

    with open("fbstate.json", "r") as f:
        cookies = json.load(f)

    with open("commands.json", "r") as f:
        commands = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="fbstate.json")
        page = await context.new_page()

        await page.goto(GROUP_URL)
        await page.wait_for_selector("div[role=\"row\"] div[dir=\"auto\"]", timeout=15000)
        print("✅ Loaded chat.")

        last_seen = set()

        while True:
            messages = await page.query_selector_all("div[role=\"row\"] div[dir=\"auto\"]")
            for msg in messages[-10:]:
                text = await msg.inner_text()
                if text not in last_seen:
                    last_seen.add(text)
                    print("📨", text)

                    for cmd in commands:
                        if text.startswith(cmd["command"]):
                            response = cmd["reply"]
                            await page.type('div[aria-label="Message"]', response)
                            await page.keyboard.press("Enter")
                            print(f"⚙️ Responded to: {cmd['command']}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=start_bot_loop).start()
    app.run(host="0.0.0.0", port=10000)
    
