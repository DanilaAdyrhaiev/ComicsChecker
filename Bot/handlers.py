from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from Bot.states.AddComicState import AddComic
from aiogram.fsm.context import FSMContext
import httpx
from Bot.Logger import Logger


logger = Logger.get_logger(__name__)

router = Router()
bot_send_message = None


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
                                         json={"chat_id": chat_id, "name": name})
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


@router.message(AddComic.title)
async def regComicTitle(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    title = data.get("title")
    logger.info(f"Comic title received: {title}")

    async with httpx.AsyncClient() as client:
        try:
            # Проверяем существование комикса
            headers = {"Content-Type": "application/json"}
            response = await client.get(
                "http://comicschecker:8001/comics/check",
                params={"title": title},
                headers=headers
            )
            response.raise_for_status()
            val = response.json()

            if not val.get("result"):
                logger.warning(f"Comic not found: {title}")
                await message.answer("Комикс не найден")
                return

            logger.info(f"Comic title exists: {title}, fetching from comicslibrary")

            comic_response = await client.request("GET", "http://comicslibrary:8000/comic/", json={"title": title})
            logger.info(f"Comic response received: {comic_response}")
            comic_response.raise_for_status()
            comic_data = comic_response.json()

            if not comic_data.get("result"):
                new_comic_data = {"title": title}
                comic_create_response = await client.post(
                    "http://comicslibrary:8000/comic/",
                    json=new_comic_data,
                    headers=headers
                )
                comic_create_response.raise_for_status()
                comic = comic_create_response.json()
                if "id" not in comic:
                    logger.error(f"Failed to create comic: {comic}")
                    await message.answer("Ошибка при создании комикса")
                    return
            else:
                comic = comic_data

            comic_id = comic["id"]

            # Привязываем комикс к пользователю
            user_comic_data = {"comic_id": comic_id}
            res = await client.post(
                f"http://comicslibrary:8000/user/{message.chat.id}/comics/{comic_id}",
                headers=headers,
                json=user_comic_data
            )
            res.raise_for_status()
            res_data = res.json()

            if not res_data.get("result"):
                logger.error(f"Failed to link comic {comic_id} to user {message.chat.id}: {res_data}")
                await message.answer("Ошибка при получении данных комикса")
                return

            logger.info(f"Comic '{title}' successfully added for user {message.from_user.full_name}")
            await message.answer("Комикс успешно добавлен")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            await message.answer("Ошибка на сервере. Попробуйте позже.")
        except httpx.HTTPError as e:
            logger.error(f"HTTP request error while processing comic: {e}")
            await message.answer("Произошла ошибка при обработке запроса.")


async def notifyUser(chat_id: int, text: str):
    if bot_send_message is None:
        logger.error("Send message method not set")
        raise ValueError("Метод отправки сообщений не установлен")

    try:
        logger.info(f"Sending notification to chat ID {chat_id}")
        await bot_send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Error sending message to chat ID {chat_id}: {e}")
