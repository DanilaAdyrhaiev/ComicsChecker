from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram import Router, F
from .states.AddComicState import AddComic
from aiogram.fsm.context import FSMContext
from comicsChecker.user.User import User, global_service
from comicsChecker.comic.ComicDTO import ComicDTO

router = Router()
bot_send_message = None

def set_bot_send_message(send_message_method):
    global bot_send_message
    bot_send_message = send_message_method

def sendDataToService(message:Message, data):
    user = global_service.get_user_by_chat_id(message.chat.id)
    global_service.add_comic(user.chatId, ComicDTO(data['title'], data['url']).toComic())


@router.message(Command("start"))
async def sendMessage(message: Message):
    if message.chat.username == "IceikSky":
        await message.answer(f"Хуле ты клацаешь. Иди своей маме в писб поклацай")
    else:
        global_service.add_user(user=User(message.chat.username, message.chat.id))
        await message.answer(f"Hello {message.from_user.full_name}\nЧтобы добавить тайтл, введите /new")

@router.message(Command('new'))
async def callAddComicState(message: Message, state: FSMContext):
    await state.set_state(AddComic.title)
    await message.answer('Введи название тайтла из канала:\nt.me/lnmanga')

@router.message(AddComic.title)
async def regComicTitle(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddComic.url)
    await message.answer('Скинь ссылку последней главы\n(Если хотите посмотреть как работает бот, то предпоследней) из канала:\n t.me/lnmanga:')

@router.message(AddComic.url)
async def regComicURL(message: Message, state: FSMContext):
    await state.update_data(url = message.text)
    data = await state.get_data()
    sendDataToService(message, data)
    await message.answer("Тайтл добавлен")

async def notifyUser(chat_id: int, text: str):
    if bot_send_message is None:
        raise ValueError("Метод отправки сообщений не установлен")
    try:
        await bot_send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")