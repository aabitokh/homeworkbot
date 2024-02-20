from database.main_db.database import Session
from model.main_db.admin import Admin
from database.main_db.teacher_crud import is_teacher
from model.main_db.chat import Chat
from model.main_db.teacher import Teacher



def add_chat(chat_id: int) -> None:
    with Session() as session:
        session.add(Chat(chat_id=chat_id))
        session.commit()

def is_admin_no_teacher_mode(telegram_id: int) -> bool:
    with Session() as session:
        admin = session.query(Admin).get(telegram_id)
        if admin is None:
            return False
        return not admin.teacher_mode
    
def is_admin_with_teacher_mode(telegram_id: int) -> bool:
    with Session() as session:
        admin = session.query(Admin).get(telegram_id)
        if admin is None:
            return False
        return admin.teacher_mode

def is_admin(telegram_id: int) -> bool: 
    with Session() as session:
        admin = session.query(Admin).get(telegram_id)
        return admin is not None
    
def  is_admin_and_teacher(telegram_id: int) -> bool: 
    with Session() as session: 
        _is_admin = is_admin(telegram_id)
        _is_teacher = is_teacher(telegram_id)
        return _is_admin and _is_teacher


def add_teacher(full_name: str, tg_id: int) -> None:
    """
    Функция добавления преподавателя

    :param full_name: ФИО препода
    :param tg_id: идентификатор препода в телегераме

    :return: None
    """
    with Session() as session:
        session.add(Teacher(full_name=full_name, telegram_id=tg_id))
        session.commit()



