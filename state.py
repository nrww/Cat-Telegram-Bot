from aiogram.fsm.state import StatesGroup, State

class CreateCat(StatesGroup):
    add_name = State()
    add_img = State()

class CheckCat(StatesGroup):
    check = State()