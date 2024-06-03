
from aiogram import types, F, Router, flags, Bot
from aiogram.types import Message, ReplyKeyboardRemove, BufferedInputFile
from aiogram.fsm.context import FSMContext

from state import CreateCat, CheckCat
import kb
import io
import requests
from data import *
import os

REID_IP = os.environ['REID_IP']
REID_PORT = os.environ['REID_PORT']


router = Router()



@router.callback_query(F.data == "check_cat")
async def cmd_check_cat(clbck: types.CallbackQuery, state: FSMContext):
    await state.set_state(CheckCat.check)
    await clbck.message.answer('Загрузите фотографию', reply_markup=ReplyKeyboardRemove())

@router.message(CheckCat.check, F.content_type.in_({'photo', 'document'}))
@flags.chat_action("typing")
async def check_cat(msg: Message, state: FSMContext, bot: Bot, album: list[Message] = None):
    
    img = io.BytesIO()
    await bot.download(
        msg.photo[-1],
        destination=img
    )
    img.seek(0)
    user_id = msg.from_user.id
    try:
        with Session() as session:
            owner_id = session.query(Owner.id).filter(Owner.chat_id == user_id).first()[0]

        url = f'http://{REID_IP}:{REID_PORT}/check_cat/?owner={str(owner_id)}&debug=1'
        file = {'file': img}
        resp = requests.post(url=url, files=file) 

    except Exception as e:
        print(e)
        msg.answer('Internal error')
        return     
    
    await msg.answer_photo(
            BufferedInputFile(
                resp.content,
                filename="img.png"
            )
        )

    
    json = resp.headers
    cats_name = []
    with Session() as session:
        for c in json['nearest_cats'].strip('[]').split(', '):
            cats_name.append(session.query(Cat.name).filter(Cat.id == c).first()[0])
        cat_name = session.query(Cat.name).filter(Cat.id == json["cat_id"]).first()[0]

    text = ''    
    
    if json['pass'] == '1':
        text+='<b>Кот опознан</b>'
    else:
        text+='<b>Кот не опознан</b>'
    text+= f'\n<b>Prec@{len(cats_name)}:</b> {json["conf"]}'
    text+= f'\n<b>Кот:</b> {cat_name}'
    cats_list = "\n\t".join([" " + str(i+1) + ". " + x for i, x in enumerate(cats_name)])
    text+= f'\n<b>Ближайшие коты:</b>\n{cats_list}'
    text+= f'\n<b>Время:</b> {json["time"]} ms'
    text+= f'\n{json["nearest_cats"]}'
    
    await msg.answer(text, reply_markup=kb.menu)
    await state.clear()
    
@router.callback_query(F.data == "add_cat")
async def cmd_add_cat(clbck: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateCat.add_name)
    await clbck.message.answer('Введите имя питомца', reply_markup=ReplyKeyboardRemove())

@router.message(CreateCat.add_name)
async def add_name(msg: Message, state: FSMContext):
    name = msg.text
    if len(name) > 30:
        await msg.answer('Имя слишком длинное, введите имя короче')
    else:
        await state.update_data(name=name)
        await msg.answer('Отправьте 3-5 фото кота с разных ракурсов')
        await state.set_state(CreateCat.add_img)
    
@router.message(CreateCat.add_img, F.content_type.in_({'photo', 'document'}))
@flags.chat_action("typing")
async def add_name(msg: Message, state: FSMContext, bot: Bot, album: list[Message] = None):
    imgs = []
    for file in album:
        buff = io.BytesIO()
        await bot.download(
            file.photo[-1],
            destination=buff
        )
        buff.seek(0)
        imgs.append(buff)
    user_id = msg.from_user.id
    user_data = await state.get_data()
    try:
        url = f'http://{REID_IP}:{REID_PORT}/add_cat/?cat_name={user_data["name"]}&owner={str(user_id)}'
        files = [('files', file.getvalue()) for file in imgs]
        resp = requests.post(url=url, files=files) 
        resp = resp.json()          
    except Exception as e:
        print(e)
        msg.answer('Internal error')
        return
    
    if resp['n_add_img'] == len(imgs):
        text = 'Кот добавлен'       
    else:
        text = f'Успешно обработаны только {resp["n_all_img"]} фото'
        for i, err in enumerate(resp['error']):
            if err == 'NF':
                text += f'\nНа {i+1} фото не найден кот'
            elif err == 'OC':
                text += f'\nНа {i+1} фото несколько котов, обрежьте изображение так, что бы на фото был только Ваш питомец'
    if resp['n_all_img'] <3:
        text += f'\nДля стабильной работы необходимо не менее 3 фото.\nЗагрузите дополнительные фото'
        await msg.answer(text, reply_markup=kb.exit_kb)
    else:
        await msg.answer(text, reply_markup=kb.menu)
        await state.clear()

    
