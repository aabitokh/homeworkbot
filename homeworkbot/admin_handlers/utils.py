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

async def start_upload_file_message(message: Message) -> Message:
    return await bot.send_message(
        message.chat.id,
        "<i>Загружаем ваш файл...</i>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


async def finish_upload_file_message(
        message: Message,
        result_message: Message,
        text: str = '<i>Файл загружен!</i>') -> None:

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=result_message.id,
        text=text,
        parse_mode="HTML",
    )

from model.main_db.student import Student

async def create_groups_button(message: Message, callback_prefix: str):
    groups = admin_crud.get_all_groups()
    if len(groups) < 1:
        await bot.send_message(message.chat.id, "В БД отсутствуют группы!")
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        *[InlineKeyboardButton(
            it.group_name,
            callback_data=f'{callback_prefix}_{it.id}'
        ) for it in groups]
    )
    await bot.send_message(
        message.chat.id,
        "Выберете группу в которой учится студент:",
        reply_markup=markup
    )


async def create_callback_students_button(
        call: CallbackQuery,
        students: list[Student],
        callback_prefix: str, id_flag: bool = False) -> None:
    if len(students) < 1:
        await bot.send_message(call.message.chat.id, "В группе нет студентов")
        return
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        *[InlineKeyboardButton(
            it.full_name,
            callback_data=f'{callback_prefix}_{it.telegram_id if not id_flag else it.id}'
        ) for it in students]
    )
    await bot.edit_message_text(
        "Выберите студента:",
        call.message.chat.id,
        call.message.id,
        reply_markup=markup,
    )
