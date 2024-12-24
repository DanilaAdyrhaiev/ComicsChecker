from aiogram.fsm.state import StatesGroup, State

class AddComic(StatesGroup):
    title = State()
    url = State()