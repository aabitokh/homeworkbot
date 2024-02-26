from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message

from database.main_db import common_crud


class BanMiddleware(BaseMiddleware):
    """
    Класс промежуточного ПО, внедряемого в бота для отсечения забаненных
    студентов от функциональности системы
    """
    def __init__(self, bot: AsyncTeleBot) -> None:
        self.update_types = ['message']
        self.bot = bot

    async def pre_process(self, message: Message, data):
        if common_crud.is_ban(message.from_user.id):
            await self.bot.send_message(
                message.chat.id,
                f'Функциональность бота недоступна, вы в бан-листе!!! '
                f'Для разблокировки обратитесь к своему преподавателю!'
            )
            return CancelUpdate()

    async def post_process(self, message, data, exception):
        pass