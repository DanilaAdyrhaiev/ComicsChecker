from .user.User import global_service as service
import time
import requests
import telegram.handlers as handlers
import copy
import asyncio

async def check():
    while True:
        for user in service.load_users():
            for comic in user.comics:
                url = comic.path.replace("###", f"{comic.lastChapter+1}")
                response = requests.get(url)
                status_code = response.status_code
                if status_code == 200:
                    text = f"{comic.title}\n{url}"
                    await handlers.notifyUser(user.chatId, text)  # Используем await
                    newComic = copy.deepcopy(comic)
                    newComic.lastChapter += 1
                    service.edit_comic(user.chatId, newComic)
        await asyncio.sleep(10)  # Используем asyncio.sleep вместо time.sleep

async def start_comics_check():
    await check()