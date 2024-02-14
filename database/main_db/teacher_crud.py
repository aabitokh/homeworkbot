from database.main_db.database import Session
from model.main_db.teacher import Teacher

def is_teacher(telegram_id: int) -> bool:
    with Session() as session:
        teacher = session.query(Teacher).filter(
            Teacher.telegram_id == telegram_id
        )
        return teacher is not None