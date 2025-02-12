from dotenv import load_dotenv
import os
from telethon import TelegramClient, events
import httpx
import asyncio
from Checker.Logger import Logger
from typing import List, Dict, Any

# Загрузка переменных окружения
load_dotenv()
api = os.getenv("TELETHON_API_ID")
hash = os.getenv("TELETHON_API_HASH")

if not api or not hash:
    raise ValueError("TELETHON_API_ID и TELETHON_API_HASH должны быть заданы в .env")

SESSION_FILE = "Checker/user_session"
channel_username = "https://t.me/testingchanell0000001"
client = TelegramClient(SESSION_FILE, api, hash)
logger = Logger.get_logger(__name__)

comics_list: List[Dict[str, Any]] = []
lock = asyncio.Lock()


async def fetch_comics_list() -> None:
    logger.info("Starting comics list fetching service")
    global comics_list

    while True:
        try:
            async with httpx.AsyncClient() as client:
                logger.debug("Sending request to comics API")
                response = await client.get(
                    "http://comicslibrary:8000/comics/all",
                    timeout=5.0
                )
                response.raise_for_status()
                comics = response.json()
                logger.info(f"Response from comics API: {comics}")

                # Валидация полученных данных
                valid_comics = [comic for comic in comics]
                invalid_count = len(comics) - len(valid_comics)
                if invalid_count > 0:
                    logger.warning(f"Filtered out {invalid_count} invalid comics entries")

                logger.info(f"Successfully fetched {len(valid_comics)} valid comics from API")
                logger.debug(f"Comics data: {valid_comics[:5]}...")  # Логируем первые 5 комиксов

                async with lock:
                    comics_list = valid_comics
                    logger.debug(f"Updated global comics list {valid_comics[:5]}")

        except httpx.TimeoutException:
            logger.error("Timeout while fetching comics list")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while fetching comics list: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching comics list: {str(e)}")

        logger.debug("Waiting 60 seconds before next fetch")
        await asyncio.sleep(60)


@client.on(events.NewMessage(chats=channel_username))
async def check_new_messages(event) -> None:
    if not event.text:
        logger.debug("Skipping message without text")
        return

    message_text = event.text.strip()
    logger.info(f"Received new message: {message_text[:100]}...")  # Логируем первые 100 символов

    # Ожидание разблокировки comics_list перед чтением
    async with lock:
        current_comics = comics_list.copy()

    if not current_comics:
        logger.warning("Comics list is empty, skipping message check")
        return

    for comics in current_comics:
        check_text = comics["title"].lower()
        message = message_text.lower()

        if check_text in message:
            logger.info(f"Found matching comics: {comics['title']}")

            for user_id in comics["users"]:
                logger.debug(f"Processing user {user_id}")

                try:
                    async with httpx.AsyncClient() as client:
                        # Получаем данные пользователя
                        async with lock:  # Ожидание при работе с пользователем
                            user_response = await client.get(
                                "http://comicslibrary:8000/user/",
                                json={"id": user_id},
                                timeout=5.0
                            )
                        user_response.raise_for_status()
                        user_data = user_response.json()
                        logger.debug(f"User data: {user_data}")

                        if "chat_id" not in user_data:
                            logger.error(f"Missing chat_id in user data for user {user_id}")
                            continue

                        logger.info(f"Retrieved user data for {user_id}: {user_data}")

                        # Отправляем уведомление
                        async with lock:  # Ожидание перед отправкой
                            notify_response = await client.post(
                                "http://bot:8002/notify/",
                                json={
                                    "chat_id": user_data["chat_id"],
                                    "message": message_text
                                },
                                timeout=5.0
                            )
                        notify_response.raise_for_status()
                        logger.info(f"Successfully notified user {notify_response.text}")

                except httpx.TimeoutException:
                    logger.error(f"Timeout while processing user {user_id}")
                except httpx.HTTPError as e:
                    logger.error(f"HTTP error while processing user {user_id}: {str(e)}")
                except Exception as e:
                    logger.error(f"Unexpected error while processing user {user_id}: {str(e)}")


async def check_comics(title: str) -> bool:
    logger.info(f"Checking for comics with title: {title}")
    try:
        async for message in client.iter_messages(channel_username, limit=100):
            if message.text and title.lower() in message.text.lower():
                logger.info(f"Found comics '{title}' in channel history")
                return True

        logger.info(f"Comics '{title}' not found in channel history")
        return False

    except Exception as e:
        logger.error(f"Error while checking comics history: {str(e)}")
        return False