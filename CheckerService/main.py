import asyncio
from CheckerService.Checker import client, fetch_comics_list
from CheckerService.Controller import app
from hypercorn.config import Config
from hypercorn.asyncio import serve

async def start_services() -> None:
    await client.start()
    print("Telegram client запущен...")
    asyncio.create_task(fetch_comics_list())

    config = Config()
    config.bind = ["0.0.0.0:8001"]
    await serve(app, config)


if __name__ == "__main__":
    asyncio.run(start_services())