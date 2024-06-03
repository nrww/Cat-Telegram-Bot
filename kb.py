from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="Добавить кота", callback_data="add_cat"),
    InlineKeyboardButton(text="Опознать кота", callback_data="check_cat")],
    [InlineKeyboardButton(text="Добавить устройство", callback_data="buy_tokens"),
    InlineKeyboardButton(text="Изменить кота", callback_data="balance")],
    [InlineKeyboardButton(text="Статистика", callback_data="ref")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Выйти в меню", callback_data="menu")]])
