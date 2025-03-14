from telethon import TelegramClient
from telethon.sessions import StringSession  # ✅ Added missing import
import os
import logging
import sys
import asyncio

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ✅ Get API Credentials from Environment Variables
API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))  # Convert to int, default to 0 if missing
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")  # ✅ Load session from GitHub Secret

# ✅ Ensure required environment variables exist
if API_ID == 0 or not API_HASH or not SESSION_STRING:
    raise ValueError("❌ Missing TELEGRAM_API_ID, TELEGRAM_API_HASH, or SESSION_STRING!")

# ✅ Start Telegram Client using SESSION_STRING
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    logger.info("✅ Successfully connected to Telegram!")
    
    # Keep the bot running
    logger.info("🤖 Bot is now running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
