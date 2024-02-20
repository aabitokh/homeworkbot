import telebot
from telebot import asyncio_filters
from telebot.types import Message

from database.main_db import admin_crud, teacher_crud, student_crud

class IsAdmin(asyncio_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    async def check(message: Message): 
        return admin_crud.is_admin_no_teacher_mode(message.from_user.id)
    

class IsAdmin(asyncio_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    async def check(message: Message): 
        return admin_crud.is_admin_no_teacher_mode(message.from_user.id)
    

class IsStudent(asyncio_filters.SimpleCustomFilter):
    key = 'is_student'

    @staticmethod
    async def check(message: Message):
        return student_crud.is_student(message.from_user.id)

class IsTeacher(asyncio_filters.SimpleCustomFilter):
    key = 'is_teacher'

    @staticmethod
    async def check(message: Message):
        if admin_crud.is_admin_and_teacher(message.from_user.id):
            return admin_crud.is_admin_with_teacher_mode(message.from_user.id)
        return teacher_crud.is_teacher(message.from_user.id)