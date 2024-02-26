from enum import Enum, auto

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, Message

from database.main_db import admin_crud
from homeworkbot import bot

from model.main_db.teacher import Teacher
from homeworkbot.admin_handlers.add_chat import _handle_add_chat

from homeworkbot.admin_handlers.add_teacher import _handle_add_teacher
from homeworkbot.admin_handlers.utils import create_teachers_button
from homeworkbot.admin_handlers.add_student import _handle_add_student
from homeworkbot.admin_handlers.add_discipline import _handle_add_discipline



class AdminException(Exception):
    ...


class AdminCommand(Enum):
    ADD_GROUP = auto()
    ADD_TEACHER = auto()
    ADD_STUDENT = auto()
    ADD_DISCIPLINE = auto()
    ADD_CHAT = auto()
    SET_TEACHER_TO_GROUP = auto()
    SET_TEACHER_TO_DISCIPLINE = auto()
    BAN_STUDENT = auto()
    UNBAN_STUDENT = auto()
    UPLOAD_CONFIGURATION = auto()
    UPLOAD_TESTS = auto()
    ADD_STUDENTS_GROUP = auto()
    NEXT = auto()
    BACK = auto()
    DELETE_STUDENT = auto()
    DELETE_TEACHER = auto()
    DELETE_GROUP = auto()
    DOWNLOAD_FULL_REPORT = auto()
    DOWNLOAD_SHORT_REPORT = auto()
    DOWNLOAD_FINISH_REPORT = auto()
    DOWNLOAD_ANSWER = auto()
    DOWNLOAD_ALL_ANSWER_WITH_TEST = auto()
    SWITCH_TO_TEACHER = auto()


__admin_commands = {
    AdminCommand.UPLOAD_TESTS: 'Загрузить тесты',
    AdminCommand.UPLOAD_CONFIGURATION: 'Загрузить стартовую конфигурацию',
    AdminCommand.BAN_STUDENT: 'Забанить',
    AdminCommand.UNBAN_STUDENT: 'Разбанить',
    AdminCommand.SET_TEACHER_TO_DISCIPLINE: 'Назначить преподу дисциплину',
    AdminCommand.SET_TEACHER_TO_GROUP: 'Назначить преподу группу',
    AdminCommand.ADD_STUDENTS_GROUP: 'Доб. гр. студентов',
    AdminCommand.ADD_STUDENT: 'Добавить студента',
    AdminCommand.ADD_TEACHER: 'Добавить препода',
    AdminCommand.ADD_DISCIPLINE: 'Добавить дисциплину',
    AdminCommand.ADD_CHAT: 'Добавить чат',
    AdminCommand.NEXT: '➡',
    AdminCommand.BACK: '⬅',
    AdminCommand.DELETE_STUDENT: 'Удал. студента',
    AdminCommand.DELETE_GROUP: 'Удал. группу',
    AdminCommand.DELETE_TEACHER: 'Удал. препода',
    AdminCommand.DOWNLOAD_ANSWER: 'Скачать ответы',
    AdminCommand.DOWNLOAD_ALL_ANSWER_WITH_TEST: 'Скачать все ответы',
    AdminCommand.DOWNLOAD_FULL_REPORT: 'Полный отчет',
    AdminCommand.DOWNLOAD_SHORT_REPORT: 'Короткий отчет',
    AdminCommand.DOWNLOAD_FINISH_REPORT: 'Итоговый отчет',
    AdminCommand.SWITCH_TO_TEACHER: '👨‍🏫'
}


def first_admin_keyboard(message: Message) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.ADD_TEACHER]),
        KeyboardButton(__admin_commands[AdminCommand.ADD_CHAT])
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.ADD_STUDENT]),
        KeyboardButton(__admin_commands[AdminCommand.ADD_DISCIPLINE]),
        KeyboardButton(__admin_commands[AdminCommand.ADD_STUDENTS_GROUP])
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.SET_TEACHER_TO_DISCIPLINE]),
        KeyboardButton(__admin_commands[AdminCommand.SET_TEACHER_TO_GROUP])
    )
    footer_buttons = []
    if admin_crud.is_teacher(message.from_user.id):
        footer_buttons.append(KeyboardButton(__admin_commands[AdminCommand.SWITCH_TO_TEACHER]))
    footer_buttons.append(KeyboardButton(__admin_commands[AdminCommand.NEXT]))
    markup.add(*footer_buttons)
    return markup


def second_admin_keyboard(message: Message | None = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.DOWNLOAD_ANSWER]),
        KeyboardButton(__admin_commands[AdminCommand.DOWNLOAD_FINISH_REPORT]),
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.DOWNLOAD_FULL_REPORT]),
        KeyboardButton(__admin_commands[AdminCommand.DOWNLOAD_SHORT_REPORT]),
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.DOWNLOAD_ALL_ANSWER_WITH_TEST]),
        KeyboardButton(__admin_commands[AdminCommand.BAN_STUDENT]),
        KeyboardButton(__admin_commands[AdminCommand.UNBAN_STUDENT]),
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.BACK]),
        KeyboardButton(__admin_commands[AdminCommand.NEXT])
    )
    return markup


def third__admin_keyboard(message: Message | None = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.DELETE_GROUP]),
        KeyboardButton(__admin_commands[AdminCommand.DELETE_TEACHER]),
        KeyboardButton(__admin_commands[AdminCommand.DELETE_STUDENT]),
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.UPLOAD_TESTS]),
        KeyboardButton(__admin_commands[AdminCommand.UPLOAD_CONFIGURATION])
    )
    markup.add(
        KeyboardButton(__admin_commands[AdminCommand.BACK]),
    )
    return markup


def is_admin_command(command: str) -> bool:
    for key, value in __admin_commands.items():
        if value == command:
            return True
    return False


def get_current_admin_command(command: str) -> AdminCommand:
    for key, value in __admin_commands.items():
        if value == command:
            return key
    raise AdminException('Неизвестная команда')


__menu_index: dict[int, int] = {}
__menu_list = [
    first_admin_keyboard,
    second_admin_keyboard,
    third__admin_keyboard,
]


@bot.message_handler(is_admin=True, func=lambda message: is_admin_command(message.text))
async def handle_commands(message: Message):
    command = get_current_admin_command(message.text)
    match command:
        case AdminCommand.ADD_CHAT:
            @bot.message_handler(is_admin=True, func=lambda message: is_admin_command(message.text))
            async def handle_commands(message: Message):
                command = get_current_admin_command(message.text)
                match command:
                    case AdminCommand.ADD_CHAT:
                        await _handle_add_chat(message)
        case AdminCommand.ADD_STUDENT:
            await _handle_add_student(message)
        case AdminCommand.ADD_TEACHER:
            await _handle_add_teacher(message)
        case AdminCommand.ADD_STUDENTS_GROUP:
            ...
        case AdminCommand.ADD_DISCIPLINE:
            await _handle_add_discipline(message)
        case AdminCommand.BAN_STUDENT:
            ...
        case AdminCommand.UNBAN_STUDENT:
            ...
        case AdminCommand.NEXT:
            if message.from_user.id not in __menu_index:
                __menu_index[message.from_user.id] = 1
            else:
                __menu_index[message.from_user.id] += 1
            index = __menu_index[message.from_user.id]
            await bot.send_message(
                message.chat.id,
                "Смена меню",
                reply_markup=__menu_list[index](message),
            )
        case AdminCommand.BACK:
            if message.from_user.id not in __menu_index:
                __menu_index[message.from_user.id] = 0
            else:
                __menu_index[message.from_user.id] -= 1
            index = __menu_index[message.from_user.id]
            await bot.send_message(
                message.chat.id,
                "Смена меню",
                reply_markup=__menu_list[index](message),
            )
        case AdminCommand.SET_TEACHER_TO_GROUP:
            await create_teachers_button(message, 'assignTeacherGR')
        case AdminCommand.SET_TEACHER_TO_DISCIPLINE:
            ...
        case AdminCommand.DELETE_GROUP:
            ...
        case AdminCommand.DELETE_STUDENT:
            ...
        case AdminCommand.DELETE_TEACHER:
            ...
        case AdminCommand.UPLOAD_TESTS:
            ...
        case AdminCommand.UPLOAD_CONFIGURATION:
            ...
        case AdminCommand.SWITCH_TO_TEACHER:
            ...
        case AdminCommand.DOWNLOAD_FULL_REPORT:
            ...
        case AdminCommand.DOWNLOAD_ANSWER:
            ...
        case AdminCommand.DOWNLOAD_FINISH_REPORT:
            ...
        case AdminCommand.DOWNLOAD_SHORT_REPORT:
            ...
        case AdminCommand.DOWNLOAD_ALL_ANSWER_WITH_TEST:
            ...
            