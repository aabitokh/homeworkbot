from enum import Enum, auto

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, Message

from database.main_db import teacher_crud
import homeworkbot.admin_handlers.admin_menu as admin_keyboard
from database.main_db.admin_crud import is_admin
from homeworkbot import bot
from homeworkbot.teacher_handlers.utils import create_teacher_groups_button, create_teacher_discipline_button


class TeacherException(Exception):
    ...


class TeacherCommand(Enum):
    BAN_STUDENT = auto()
    UNBAN_STUDENT = auto()
    DOWNLOAD_FULL_REPORT = auto()
    DOWNLOAD_SHORT_REPORT = auto()
    DOWNLOAD_FINISH_REPORT = auto()
    DOWNLOAD_ANSWER = auto()
    INTERACTIVE_REPORT = auto()
    SWITCH_TO_ADMIN = auto()


__teacher_commands = {
    TeacherCommand.BAN_STUDENT: 'Забанить',
    TeacherCommand.UNBAN_STUDENT: 'Разбанить',
    TeacherCommand.DOWNLOAD_ANSWER: 'Скачать ответы',
    TeacherCommand.INTERACTIVE_REPORT: 'Интерактивный отчет',
    TeacherCommand.DOWNLOAD_FULL_REPORT: 'Полный отчет',
    TeacherCommand.DOWNLOAD_SHORT_REPORT: 'Короткий отчет',
    TeacherCommand.DOWNLOAD_FINISH_REPORT: 'Итоговый отчет',
    TeacherCommand.SWITCH_TO_ADMIN: '🥷',
}


def create_teacher_keyboard(message: Message | None = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=3)
    markup.add(
        KeyboardButton(__teacher_commands[TeacherCommand.DOWNLOAD_ANSWER]),
        KeyboardButton(__teacher_commands[TeacherCommand.DOWNLOAD_FINISH_REPORT]),
    )
    markup.add(
        KeyboardButton(__teacher_commands[TeacherCommand.DOWNLOAD_FULL_REPORT]),
        KeyboardButton(__teacher_commands[TeacherCommand.DOWNLOAD_SHORT_REPORT]),
    )
    markup.add(
        KeyboardButton(__teacher_commands[TeacherCommand.INTERACTIVE_REPORT]),
    )

    footer_buttons = [
        KeyboardButton(__teacher_commands[TeacherCommand.BAN_STUDENT]),
        KeyboardButton(__teacher_commands[TeacherCommand.UNBAN_STUDENT]),
    ]

    if is_admin(message.from_user.id):
        footer_buttons.append(
            KeyboardButton(__teacher_commands[TeacherCommand.SWITCH_TO_ADMIN])
        )
    markup.add(*footer_buttons)
    return markup


@bot.message_handler(
    is_teacher=True, func=lambda message: is_teacher_command(message.text)
)
async def handle_commands(message: Message):
    command = get_current_teacher_command(message.text)
    match command:
        case TeacherCommand.SWITCH_TO_ADMIN:
            await switch_teacher_to_admin_menu(message)
        case TeacherCommand.DOWNLOAD_FULL_REPORT:
            await create_teacher_groups_button(message, 'fullReport')
        case TeacherCommand.DOWNLOAD_FINISH_REPORT:
            await create_teacher_groups_button(message, 'finishReport')
        case TeacherCommand.DOWNLOAD_SHORT_REPORT:
            await create_teacher_groups_button(message, 'shortReport')
        case TeacherCommand.BAN_STUDENT:
            ...
        case TeacherCommand.UNBAN_STUDENT:
            ...
        case TeacherCommand.INTERACTIVE_REPORT:
            await create_teacher_groups_button(message, 'interactiveGrRep')
        case TeacherCommand.DOWNLOAD_ANSWER:
            await create_teacher_discipline_button(message, 'dowTAnswersDis')


async def switch_teacher_to_admin_menu(message: Message):
    teacher_crud.switch_teacher_mode_to_admin(message.from_user.id)
    await bot.send_message(
        message.chat.id,
        'Переключение в режим админа',
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=admin_keyboard.first_admin_keyboard(message),
    )


def is_teacher_command(command: str) -> bool:
    for key, value in __teacher_commands.items():
        if value == command:
            return True
    return False


def get_current_teacher_command(command: str) -> TeacherCommand:
    for key, value in __teacher_commands.items():
        if value == command:
            return key
    raise TeacherException('Неизвестная команда')
