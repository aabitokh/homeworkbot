import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_storage import StateMemoryStorage
from homeworkbot.filters import AddStudentCallbackFilter
from homeworkbot.filters import IsAdmin, IsStudent, IsTeacher
from homeworkbot.middlewares import BanMiddleware

load_dotenv()

#создаем бота
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'), state_storage= StateMemoryStorage())

#подключаем асинхронные фильтры
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(IsStudent())
bot.add_custom_filter(IsTeacher())
bot.add_custom_filter(AddStudentCallbackFilter())

bot.setup_middleware(BanMiddleware(bot))