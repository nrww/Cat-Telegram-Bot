
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from data import *
import kb


router = Router()
greet = "Привет, {name}, выберите действие:"
menu = "Главное меню"

@router.message(Command("start"))
async def start_handler(msg: Message):
    
    with Session() as session:
        owner = session.query(Owner.id).filter(Owner.chat_id == msg.from_user.id).first()
        if owner is None:
            owner = Owner(chat_id = msg.from_user.id)
            session.add(owner)
            session.commit()
        
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "menu")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message , state: FSMContext):
    await state.clear()
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(StateFilter(None),F.text == "Меню")
@router.message(StateFilter(None),F.text == "Выйти в меню")
async def cmd_cancel_no_state(msg: Message, state: FSMContext):

    await state.set_data({})
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)
