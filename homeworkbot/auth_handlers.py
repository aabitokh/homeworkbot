from telebot.apihelper import ApiTelegramException
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.types import Message

from homeworkbot.configuration import bot


@bot.message_handler(commands=['start'])
async def handle_start(message: Message):
    await bot.send_message(
                message.chat.id,
                'Hi!',
                parse_mode='HTML'
            )