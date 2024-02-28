from telebot.types import Message, CallbackQuery

from homeworkbot.admin_handlers.utils import create_teachers_button
from homeworkbot.configuration import bot
from database.main_db import admin_crud


@bot.message_handler(is_admin=True, commands=['delteacher'])
async def handle_delete_teacher(message: Message):
    await create_teachers_button(message, 'delTeacher')


@bot.message_handler(is_admin=False, commands=['delteacher'])
async def handle_no_delete_teacher(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


@bot.callback_query_handler(func=lambda call: 'delTeacher_' in call.data)
async def callback_assign_teacher_to_group(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'delTeacher':
            teacher_id = int(call.data.split('_')[1])
            admin_crud.delete_teacher(teacher_id)
            await bot.edit_message_text(
                "Преподаватель успешно удален",
                call.message.chat.id,
                call.message.id
            )
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id
            )