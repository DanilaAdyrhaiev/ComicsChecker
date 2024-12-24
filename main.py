import asyncio
import threading
from comicsChecker.checker import start_comics_check
from telegram.bot import start_bot

async def main():
    asyncio.create_task(start_comics_check())  
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
