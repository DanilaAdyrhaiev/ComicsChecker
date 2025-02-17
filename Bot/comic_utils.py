# comic_utils.py
import httpx
import time
from urllib.parse import quote
from Bot.Logger import Logger
logger = Logger.get_logger(__name__)

timeout = 180  # например, определите ваш тайм-аут, если он глобальный

async def get_comic_title(message, state):
    await state.update_data(title=message.text)
    data = await state.get_data()
    title = data.get("title")
    logger.info(f"Received comic title from user {message.from_user.id}: {title}")
    return title

async def check_comic_in_checker(title: str):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json"}
        encoded_title = quote(title)
        logger.info(f"Sending request to comicschecker: {encoded_title}")
        start_time = time.monotonic()
        response = await client.get(
            "http://comicschecker:8001/comics/check",
            params={"title": title},
            headers=headers,
            timeout=timeout
        )
        end_time = time.monotonic()
        logger.info(f"Response time: {end_time - start_time:.2f} seconds")
        logger.info(f"Response from comicschecker: {response.status_code} {response.text}")
        response.raise_for_status()
        return response.json()

async def check_comic_in_library(title: str):
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Content-Type": "application/json"}
            response = await client.get(
                "http://comicslibrary:8000/comic/",
                params={"title": title},  # Используем params вместо json
                headers=headers
            )
            response.raise_for_status()  # Проверяем успешный статус ответа
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
        except httpx.HTTPError as e:
            logger.exception(f"HTTP request error: {type(e).__name__} - {str(e)}")
        return {}

async def create_comic_in_library(title: str):
    async with httpx.AsyncClient() as client:
        new_comic_data = {"title": title}
        comic_create_response = await client.post(
            "http://comicslibrary:8000/comic/",
            json=new_comic_data,
            headers={"Content-Type": "application/json"}
        )
        logger.info(f"Response from comicslibrary (create): {comic_create_response.status_code} {comic_create_response.text}")
        comic_create_response.raise_for_status()
        return comic_create_response.json()

async def link_comic_to_user(comic_id: int, user_id: int, chat_id: int):
    async with httpx.AsyncClient() as client:
        user_comic_data = {"comic_id": comic_id}
        res = await client.post(
            f"http://comicslibrary:8000/user/{chat_id}/comics/{comic_id}",
            headers={"Content-Type": "application/json"},
            json=user_comic_data,
            timeout=timeout
        )
        logger.info(f"Response from comicslibrary (link user): {res.status_code} {res.text}")
        res.raise_for_status()
        return res.json()