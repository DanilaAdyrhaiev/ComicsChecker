from .config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from .handlers import router, set_bot_send_message


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def setup_bot_commands(bot: Bot) -> None:
    bot_commands = [
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="new", description="add new comic"),
    ]
    await bot.set_my_commands(bot_commands)

async def main() -> None:
    set_bot_send_message(bot.send_message)
    await setup_bot_commands(bot)
    dp.include_router(router)
    await dp.start_polling(bot)

async def start_bot():
    await main()