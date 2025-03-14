from telethon import TelegramClient
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
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")  # ✅ Load session from GitHub Secret

# ✅ Ensure all required variables exist
if not API_ID or not API_HASH or not SESSION_STRING:
    raise ValueError("❌ Missing TELEGRAM_API_ID, TELEGRAM_API_HASH, or SESSION_STRING in environment variables!")

API_ID = int(API_ID)  # Convert after checking

# ✅ Start Telegram Client using SESSION_STRING
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    logger.info("✅ Successfully connected to Telegram!")
    # Your bot logic here...

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
