import time

from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from Bot.states.AddComicState import AddComic
from aiogram.fsm.context import FSMContext
import httpx
from Bot.Logger import Logger
from Bot.comic_utils import get_comic_title, check_comic_in_checker, check_comic_in_library, create_comic_in_library, link_comic_to_user


logger = Logger.get_logger(__name__)

router = Router()
bot_send_message = None
timeout = httpx.Timeout(180.0)


def set_bot_send_message(send_message_method):
    global bot_send_message
    bot_send_message = send_message_method
    logger.info("Bot send message method has been set")


@router.message(Command("start"))
async def sendMessage(message: Message):
    logger.info("Bot send message")
    chat_id = message.chat.id
    name = message.from_user.full_name
    logger.info(f"Start command received from user {name} (Chat ID: {chat_id})")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://comicslibrary:8000/user/",
                                         json={"chat_id": chat_id, "name": name}, timeout=timeout)
            response.raise_for_status()
            logger.info(f"User {name} successfully registered")
            logger.info("Attempting to send welcome message")
            try:
                await message.answer(
                    text=f"Hello {message.from_user.full_name}\nЧтобы добавить тайтл, введите /new"
                )
                logger.info("Welcome message sent successfully")
            except Exception as msg_error:
                logger.error(f"Error sending welcome message: {msg_error}")
                raise

    except httpx.HTTPError as e:
        logger.error(f"Error registering user: {e}")
        await message.answer("Произошла ошибка при обработке запроса")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.exception("Full exception traceback:")
        await message.answer("Произошла неизвестная ошибка.")



@router.message(Command('new'))
async def callAddComicState(message: Message, state: FSMContext):
    logger.info(f"New comic addition process started for user {message.from_user.full_name}")
    await state.set_state(AddComic.title)
    await message.answer('Введи название тайтла из канала:\nt.me/lnmanga')


from asyncio import sleep

from asyncio import sleep


@router.message(AddComic.title)
async def regComicTitle(message: Message, state: FSMContext):
    try:
        # Отправляем сообщение, что поиск начался
        waiting_message = await message.answer("Поиск комикса... Пожалуйста, подождите некоторое время.")

        title = await get_comic_title(message, state)

        val = await check_comic_in_checker(title)
        if not val.get("result"):
            logger.warning(f"Comic '{title}' not found in checker service")
            await waiting_message.edit_text("Комикс не найден.")
            await state.finish()  # Выход из состояния
            return

        logger.info(f"Comic '{title}' exists, checking in comicslibrary")
        start_time = time.monotonic()

        comic_data = await check_comic_in_library(title)
        if time.monotonic() - start_time > 20:
            await waiting_message.edit_text(
                "Поиск занимает больше времени, чем ожидалось. Пожалуйста, подождите ещё немного.")

        if not comic_data.get("result"):
            logger.info(f"Comic '{title}' not found in library, creating new record")
            comic = await create_comic_in_library(title)
        else:
            comic = comic_data

        comic_id = comic["id"]
        logger.info(f"Linking comic {comic_id} to user {message.from_user.id}")
        res_data = await link_comic_to_user(comic_id, message.from_user.id, message.chat.id)

        if not res_data.get("result"):
            logger.error(f"Failed to link comic {comic_id} to user {message.chat.id}: {res_data}")
            await waiting_message.edit_text(
                "Ошибка при получении данных комикса.\n"
                "Попробуйте скинуть ссылку на сообщение с комиксом или подождите, когда появится новая глава, и попробуйте снова."
            )
            await state.finish()  # Выход из состояния
            return

        logger.info(f"Comic '{title}' successfully added for user {message.from_user.full_name}")
        await waiting_message.edit_text("Комикс успешно добавлен")
        await state.finish()  # Завершаем процесс, выход из состояния

    except httpx.TimeoutException:
        logger.error("Timeout while checking comics")
        await waiting_message.edit_text("Время ожидания истекло. Попробуйте позже.")
        await state.finish()  # Выход из состояния
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
        await waiting_message.edit_text("Ошибка на сервере. Попробуйте позже.")
        await state.finish()  # Выход из состояния
    except httpx.HTTPError as e:
        logger.exception(f"HTTP request error while processing comic: {type(e).__name__} - {str(e)}")
        await waiting_message.edit_text("Произошла ошибка при обработке запроса.")
        await state.finish()  # Выход из состояния


async def notifyUser(chat_id: int, text: str):
    if bot_send_message is None:
        logger.error("Send message method not set")
        raise ValueError("Метод отправки сообщений не установлен")

    try:
        logger.info(f"Sending notification to chat ID {chat_id}")
        await bot_send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Error sending message to chat ID {chat_id}: {e}")
