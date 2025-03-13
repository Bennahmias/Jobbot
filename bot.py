from telethon import TelegramClient, events
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

API_ID = 25327295
API_HASH = "cbfa427495645e7bb7b8fe2a8da9fd9b"

# Source channels (using usernames)
SOURCE_CHANNELS = [
    "@techjobtracker_il",
    "@HiTech_Jobs_In_Israel",
    "@bafosssssss",
]

# Target channel
TARGET_CHANNEL_ID = -1002415944739

# ✅ Keywords to filter messages
KEYWORDS = ["student", "intern", "internship", "junior"]

async def main():
    """Initialize the bot and listen for messages."""
    client = TelegramClient("user_session", API_ID, API_HASH)

    logger.info("🚀 Connecting to Telegram...")
    await client.start()
    logger.info("✅ Successfully connected!")

    logger.info(f"🔎 Listening to channels: {SOURCE_CHANNELS}")

    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def forward_filtered_messages(event):
        try:
            chat = await event.get_chat()
            chat_name = chat.title if hasattr(chat, "title") else "Unknown"
            chat_id = event.chat_id
            message_text = event.text.lower() if event.text else ""

            logger.info(f"📩 New message from: {chat_name} (ID: {chat_id})")

            # 🔍 Check if the message contains a keyword
            if any(keyword in message_text for keyword in KEYWORDS):
                logger.info(f"✅ Message contains keyword, forwarding: {message_text[:50]}...")
                await client.forward_messages(TARGET_CHANNEL_ID, event.message)
                logger.info("✅ Message successfully forwarded!")
            else:
                logger.info("🚫 Message does not contain keywords, ignoring.")

        except Exception as e:
            logger.error(f"❌ Error forwarding message: {str(e)}")

    logger.info("✅ Bot is now running and waiting for messages.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped manually.")
    except Exception as e:
        logger.error(f"🚨 Unexpected error: {str(e)}")
    finally:
        loop.close()
        logger.info("🔴 Bot has shut down.")
