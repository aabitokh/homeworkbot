from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from database.main_db import admin_crud
from homeworkbot import bot


async def create_teachers_button(message: Message, callback_prefix: str):
    teachers = admin_crud.get_teachers()
    if len(teachers) < 1:
        await bot.send_message(message.chat.id, "В БД отсутствуют преподаватели!")
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        *[InlineKeyboardButton(
            it.full_name,
            callback_data=f'{callback_prefix}_{it.id}'
        ) for it in teachers]
    )
    await bot.send_message(message.chat.id, "Выберите преподавателя:", reply_markup=markup)