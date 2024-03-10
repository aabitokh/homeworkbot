from enum import Enum, auto

from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from homeworkbot import bot


class StudentException(Exception):
    ...


class StudentCommand(Enum):
    UPLOAD_ANSWER = auto()
    NEAREST_DEADLINE = auto
    ACADEMIC_PERFORMANCE = auto()


__student_commands = {
    StudentCommand.UPLOAD_ANSWER: "Загрузить ответ",
    StudentCommand.NEAREST_DEADLINE: "Ближайший дедлайн",
    StudentCommand.ACADEMIC_PERFORMANCE: "Успеваимость",
}


def student_keyboard(message: Message | None = None) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(__student_commands[StudentCommand.UPLOAD_ANSWER]),
    )
    markup.add(
        KeyboardButton(__student_commands[StudentCommand.NEAREST_DEADLINE]),
        KeyboardButton(__student_commands[StudentCommand.ACADEMIC_PERFORMANCE]),
    )
    return markup


@bot.message_handler(
    is_student=True, func=lambda message: is_student_command(message.text)
)
async def handle_commands(message: Message):
    command = get_current_student_command(message.text)
    match command:
        case StudentCommand.UPLOAD_ANSWER:
            ...
        case StudentCommand.NEAREST_DEADLINE:
            ...
        case StudentCommand.ACADEMIC_PERFORMANCE:
            ...


def is_student_command(command: str) -> bool:
    for key, value in __student_commands.items():
        if value == command:
            return True
    return False


def get_current_student_command(command: str) -> StudentCommand:
    for key, value in __student_commands.items():
        if value == command:
            return key
    raise StudentException("Неизвестная команда")