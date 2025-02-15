import os
from telethon import TelegramClient, events
import httpx
import asyncio

from telethon.errors import FloodWaitError

from CheckerService.Logger import Logger
from typing import List, Dict, Any
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
api = os.getenv("TELETHON_API_ID")
hash = os.getenv("TELETHON_API_HASH")

if not api or not hash:
    raise ValueError("TELETHON_API_ID и TELETHON_API_HASH должны быть заданы в .env")

SESSION_FILE = "CheckerService/user_session"
channel_username = "https://t.me/lnmanga"
client = TelegramClient(SESSION_FILE, api, hash)
logger = Logger.get_logger(__name__)
lock = asyncio.Lock()

def get_http_client():
    return httpx.AsyncClient(timeout=5.0)

async def fetch_comics_list() -> List[Dict[str, Any]]:
    try:
        async with get_http_client() as http_client:
            logger.debug("Fetching comics list from API")
            response = await http_client.get("http://comicslibrary:8000/comics/all")
            response.raise_for_status()
            comics_list = response.json()
            logger.info(f"Fetched {len(comics_list)} comics from API")
            return comics_list
    except httpx.HTTPError as e:
        logger.error(f"HTTP error while fetching comics list: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error while fetching comics list: {str(e)}")
    return []

async def notify_users(comics, message_text):
    for user_id in comics["users"]:
        logger.debug(f"Processing user {user_id}")
        try:
            async with get_http_client() as http_client:
                user_response = await http_client.get(
                    "http://comicslibrary:8000/user/", json={"id": user_id}
                )
                user_response.raise_for_status()
                user_data = user_response.json()

                if "chat_id" not in user_data:
                    logger.error(f"Missing chat_id in user data for user {user_id}")
                    continue

                notify_response = await http_client.post(
                    "http://bot:8002/notify/",
                    json={"chat_id": user_data["chat_id"], "message": message_text},
                )
                notify_response.raise_for_status()
                logger.info(f"Successfully notified user {user_id}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while processing user {user_id}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while processing user {user_id}: {str(e)}")

@client.on(events.NewMessage(chats=channel_username))
async def check_new_messages(event) -> None:
    if not event.text:
        logger.debug("Skipping message without text")
        return

    message_text = event.text.strip()
    logger.info(f"Received new message: {message_text[:100]}...")

    comics_list = await fetch_comics_list()
    if not comics_list:
        logger.warning("Comics list is empty, skipping message check")
        return

    for comics in comics_list:
        if comics["title"].lower() in message_text.lower():
            logger.info(f"Found matching comics: {comics['title']}")
            await notify_users(comics, message_text)


async def check_comics(title: str) -> bool:
    logger.info(f"Checking for comics with title: {title}")
    count = 0
    max_messages = 5000
    last_id = None

    try:
        async for message in client.iter_messages(channel_username, limit=1):
            last_id = message.id
            logger.debug(f"Last message ID: {last_id}")

        while count < max_messages and last_id is not None:
            messages_batch = []
            async for message in client.iter_messages(channel_username, limit=500, max_id=last_id):
                messages_batch.append(message)

            if not messages_batch:
                logger.info(f"No more messages to process after {count} messages")
                break
            for message in messages_batch:
                count += 1
                text = message.text.split("\n")[0] if message.text else ""
                logger.debug(f"Checking message {count} (ID: {message.id}): {text if text else 'No text'}")

                if text and title.lower() in text.lower():
                    logger.info(f"Found comics '{title}' in channel history")
                    return True

                last_id = message.id

            logger.debug(f"Processed {count} messages so far")
            logger.debug("Sleeping for 2 seconds to avoid rate limiting")
            await asyncio.sleep(2)

        logger.info(f"Comics '{title}' not found in channel history after checking {count} messages")
        return False

    except FloodWaitError as e:
        logger.warning(f"FloodWaitError: sleeping for {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
        return await check_comics(title)

    except Exception as e:
        logger.error(f"Error while checking comics history: {str(e)}")
        raise