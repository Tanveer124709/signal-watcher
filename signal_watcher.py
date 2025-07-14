# 🔌 Simple Flask server to keep Railway app alive
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_server).start()  # ⏱️ Start Flask server in background

# 🧠 Imports for Discord signal watching
import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 🔐 Load secrets from .env
load_dotenv()
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
DISCORD_URL = os.getenv("DISCORD_URL")

# 📤 Send new signal to your own Discord channel
def send_to_discord(content):
    payload = {"content": content}
    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print(f"[❌] Failed to send to webhook: {e}")

# 🧱 Set up invisible browser
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

# 👤 First-time login
print("[👤] Opening login window...")
driver.get("https://discord.com/login")
input("🔐 Log in to Discord in the browser, then press [Enter] here to continue...")

# 📡 Open target signal channel
driver.get(DISCORD_URL)
print("[📡] Monitoring signal channel...")
time.sleep(10)

# 🔁 Watch for new signals
last_message = ""
while True:
    try:
        messages = driver.find_elements(By.CLASS_NAME, "messageContent-2t3eCI")
        if messages:
            latest = messages[-1].text
            if latest != last_message and "buying $" in latest.lower():
                print(f"[✅] New Signal Detected:\n{latest}")
                send_to_discord(f"📥 New Signal:\n```{latest}```")
                last_message = latest
    except Exception as e:
        print(f"[⚠️] Error reading messages: {e}")

    time.sleep(5)
