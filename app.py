from dotenv import load_dotenv
import os
from telethon import TelegramClient
import asyncio


load_dotenv()
api = os.getenv('TELETHON_API_ID')
hash = os.getenv('TELETHON_API_HASH')

channel_username = "https://t.me/lnmanga"
client = TelegramClient("user_session", api, hash)

async def get_messages(keyword):
    await client.start()
    count = 0
    async for message in client.iter_messages(channel_username, limit=1000):  # Проверяем 100 последних сообщений
        if message.text and keyword.lower() in message.text.lower():
            print(f"[{message.date}] {message.sender_id}: {message.text}\n")
            for attr, value in vars(message).items():
                print(f"{attr}: {value}")
            count += 1
    await client.disconnect()

asyncio.run(get_messages("Руководство по выживанию в Академии"))