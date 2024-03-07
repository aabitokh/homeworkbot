from telebot.types import Message

from homeworkbot.admin_handlers.utils import create_groups_button
from homeworkbot.configuration import bot


@bot.message_handler(is_admin=True, commands=['shortrep'])
async def handle_download_full_report(message: Message):
    await create_groups_button(message, 'shortReport')


@bot.message_handler(is_admin=False, commands=['shortrep'])
async def handle_no_download_full_report(message: Message):
    await bot.send_message(message.chat.id, "Нет прав доступа!!!")