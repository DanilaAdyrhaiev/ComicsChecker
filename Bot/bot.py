import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from Bot.handlers import router, set_bot_send_message
from hypercorn.config import Config
from hypercorn.asyncio import serve
from Bot.Controller import app
from Bot.Logger import Logger

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
logger = Logger.get_logger(__name__)


async def setup_bot_commands(bot: Bot) -> None:
    bot_commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="new", description="Добавить новый комикс"),
    ]
    await bot.set_my_commands(bot_commands)


async def start_hypercorn():
    """Запускает Hypercorn сервер асинхронно"""
    config = Config()
    config.bind = ["0.0.0.0:8002"]
    await serve(app, config)


async def main() -> None:
    logger.info("Бот запущен")
    await setup_bot_commands(bot)
    dp.include_router(router)
    set_bot_send_message(bot.send_message)

    # Запуск FastAPI сервера в отдельной задаче
    asyncio.create_task(start_hypercorn())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Ошибка при опросе бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
