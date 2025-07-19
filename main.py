from flask import Flask
import threading
import asyncio
import json
import os
from playwright.async_api import async_playwright

app = Flask(__name__)
GROUP_URL = "https://www.facebook.com/messages/t/23897623639929962/"

# Async bot loop using Playwright
async def run_bot():
    print("🤖 Bot is live. Listening for commands...\n")

    try:
        with open("fbstate.json", "r") as f:
            cookies = json.load(f)
    except Exception as e:
        print("❌ fbstate.json not found or invalid:", e)
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state="fbstate.json")
        page = await context.new_page()

        try:
            await page.goto(GROUP_URL)
            await page.wait_for_selector('div[role="row"] div[dir="auto"]', timeout=15000)
            print("✅ Messages loaded. Scanning...\n")

            messages = await page.query_selector_all('div[role="row"] div[dir="auto"]')
            for msg in messages[-5:]:
                text = await msg.inner_text()
                print("📩", text)

        except Exception as e:
            print("⚠️ Error loading messages:", e)
        finally:
            await browser.close()

# Background thread to run bot loop
def start_async_bot():
    asyncio.run(run_bot())

@app.route('/')
def index():
    return "✅ Facebook Group Bot is running."

if __name__ == '__main__':
    # Start bot in background thread
    threading.Thread(target=start_async_bot, daemon=True).start()

    # Render-friendly PORT support
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
