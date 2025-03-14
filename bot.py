from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
import logging
import sys
import asyncio
import os
import json
import time

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ✅ Get API Credentials from Environment Variables (GitHub Secrets)
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# ✅ Ensure required variables exist
if not API_ID or not API_HASH or not SESSION_STRING:
    raise ValueError("❌ Missing TELEGRAM_API_ID, TELEGRAM_API_HASH, or SESSION_STRING!")

API_ID = int(API_ID)  # Convert AFTER checking it's not None

# ✅ Source Channels (Using Usernames)
SOURCE_CHANNELS = [
    "@techjobtracker_il", "@HiTech_Jobs_In_Israel", "@bafosssssss",
    "@Nisancommunity"
]

# ✅ Target Channel (Where messages will be forwarded)
TARGET_CHANNEL_ID = -1002415944739

# ✅ Keywords to Filter Messages
KEYWORDS = [
    "student", "intern", "internship", "junior", "entry-level", "graduate",
    "trainee", "no experience", "first job", "סטודנט", "משרת סטודנט",
    "ג'וניור", "ללא ניסיון", "משרת התחלה", "התמחות", "התמחות בתשלום",
    "משרה חלקית", "משרה ללא ניסיון", "משרת ג'וניור", "משרה התחלתית",
    "תוכנית התמחות"
]

# ✅ JSON file for tracking forwarded messages
MESSAGE_TRACKER_FILE = "message_tracker.json"

# ✅ Ensure JSON file exists
if not os.path.exists(MESSAGE_TRACKER_FILE):
    with open(MESSAGE_TRACKER_FILE, "w") as file:
        json.dump({"messages": {}}, file)

# ✅ Load and Save Message History
def load_message_history():
    with open(MESSAGE_TRACKER_FILE, "r") as file:
        return json.load(file)

def save_message_history(data):
    with open(MESSAGE_TRACKER_FILE, "w") as file:
        json.dump(data, file)

# ✅ Function to clear history every 7 days
def clear_old_messages():
    data = load_message_history()
    now = time.time()
    data["messages"] = {key: timestamp for key, timestamp in data["messages"].items() if now - timestamp < 604800}
    save_message_history(data)

async def fetch_recent_messages(client):
    """Fetch last 100 messages from all source channels."""
    logger.info("🔄 Fetching recent messages from source channels...")
    data = load_message_history()

    for channel in SOURCE_CHANNELS:
        try:
            entity = await client.get_entity(channel)
            history = await client(GetHistoryRequest(peer=entity, limit=100, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))

            for message in history.messages:
                if message.message:
                    message_text = message.message.lower()
                    msg_id = message.id
                    chat_id = entity.id
                    msg_key = f"{chat_id}-{msg_id}"  

                    if any(keyword in message_text for keyword in KEYWORDS):
                        if msg_key not in data["messages"]:
                            logger.info(f"📩 Found relevant past message in {channel}, forwarding...")
                            await client.forward_messages(TARGET_CHANNEL_ID, message)
                            data["messages"][msg_key] = time.time()
                            save_message_history(data)
        except Exception as e:
            logger.error(f"❌ Failed to fetch messages from {channel}: {str(e)}")

async def main():
    """Initialize the Telegram client and listen for messages."""
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

    logger.info("🚀 Connecting to Telegram...")
    await client.start()
    logger.info("✅ Successfully connected!")

    logger.info(f"🔎 Listening to channels: {SOURCE_CHANNELS}")

    # 🔄 Fetch old messages before running
    await fetch_recent_messages(client)

    logger.info("✅ Bot is now running and waiting for messages.")

    # ✅ Set Timeout (Auto-exit after 2 minutes)
    await asyncio.sleep(60)  # ✅ Runs for 1 minutes (60 sec) and then exits

    logger.info("🛑 Exiting bot after timeout.")
    await client.disconnect()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        clear_old_messages()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped manually.")
    except Exception as e:
        logger.error(f"🚨 Unexpected error: {str(e)}")
    finally:
        loop.close()
        logger.info("🔴 Bot has shut down.")
