from telebot.types import Message, CallbackQuery

from database.main_db import common_crud
from homeworkbot.admin_handlers.utils import create_groups_button, create_callback_students_button
from homeworkbot.configuration import bot


@bot.message_handler(is_admin=True, commands=['ban'])
async def handle_ban_student(message: Message):
    await create_groups_button(message, 'groupBan')


@bot.message_handler(is_admin=False, commands=['ban'])
async def handle_no_ban_student(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")


@bot.callback_query_handler(func=lambda call: 'studentBan_' in call.data or 'groupBan_' in call.data)
async def callback_ban_student(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'groupBan':
            group_id = int(call.data.split('_')[1])
            students = common_crud.get_students_from_group_for_ban(group_id)
            await create_callback_students_button(call, students, 'studentBan')
        case 'studentBan':
            telegram_id = int(call.data.split('_')[1])
            common_crud.ban_student(telegram_id)
            await bot.edit_message_text(
                "Студент добавлен в бан-лист",
                call.message.chat.id,
                call.message.id)
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id)
