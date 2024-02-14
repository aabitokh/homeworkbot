import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_storage import StateStorageBase

load_dotenv()

#создаем бота
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'), state_storage= StateStorageBase())

#подключаем асинхронные фильтры
bot.add_custom_filter(asyncio_filters.StateFilter(bot))