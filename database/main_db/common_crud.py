# common_crud.py
from enum import Enum

from database.main_db.database import Session

from model.main_db.admin import Admin
from model.main_db.student import Student
from model.main_db.teacher import Teacher
from model.main_db.chat import Chat

class UserEnum(Enum):
    Admin = 0
    Teacher = 1
    Student = 2
    Unknown = 3


def user_verification(telegram_id: int) -> UserEnum:
    with Session() as session:
        user = session.query(Admin).get(telegram_id)
        if user is not None:
            return UserEnum.Admin
        user = session.query(Teacher).filter(
            Teacher.telegram_id == telegram_id
        ).first()
        if user is not None:
            return UserEnum.Teacher
        user = session.query(Student).filter(
            Student.telegram_id == telegram_id
        ).first()
        if user is not None:
            return UserEnum.Student
    return UserEnum.Unknown

def get_chats() -> list[int]:
    with Session() as session:
        chats = session.query(Chat).all()
        return [it.chat_id for it in chats]