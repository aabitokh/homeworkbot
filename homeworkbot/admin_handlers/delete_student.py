from telebot.types import Message, CallbackQuery

from database.main_db import admin_crud, common_crud
from homeworkbot.admin_handlers.utils import create_groups_button, create_callback_students_button
from homeworkbot.configuration import bot


@bot.message_handler(is_admin=True, commands=['delstudent'])
async def handle_ban_student(message: Message):
    await create_groups_button(message, 'groupStudDel')


@bot.message_handler(is_admin=False, commands=['delstudent'])
async def handle_no_ban_student(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


@bot.callback_query_handler(func=lambda call: 'groupStudDel_' in call.data or 'studentDel_' in call.data)
async def callback_ban_student(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'groupStudDel':
            group_id = int(call.data.split('_')[1])
            students = common_crud.get_students_from_group(group_id)
            await create_callback_students_button(call, students, 'studentDel', True)
        case 'studentDel':
            telegram_id = int(call.data.split('_')[1])
            admin_crud.delete_student(telegram_id)
            await bot.edit_message_text(
                "Студент успешно удален!",
                call.message.chat.id,
                call.message.id)
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)