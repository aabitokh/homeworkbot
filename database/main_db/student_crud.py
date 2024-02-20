# student_crud.py
from database.main_db.database import Session

from model.main_db.student import Student


def has_student(full_name: str) -> bool:
    with Session() as session:
        student = session.query(Student).filter(
            Student.full_name.ilike(f'%{full_name}%')
        ).first()
        return student is not None


def is_student(telegram_id: int) -> bool:
    with Session() as session:
        student = session.query(Student).filter(
            Student.telegram_id == telegram_id
        ).first()
        return student is not None



def set_telegram_id(full_name: str, telegram_id: int) -> None:
    with Session() as session:
        session.query(Student).filter(
            Student.full_name.ilike(f'%{full_name}%')
        ).update(
            {Student.telegram_id: telegram_id}, synchronize_session='fetch'
        )
        session.commit()