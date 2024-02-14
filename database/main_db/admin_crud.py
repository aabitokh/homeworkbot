from database.main_db.database import Session
from model.main_db.admin import Admin
from teacher_crud import is_teacher

def is_admin_no_teacher_mode(telegram_id: int) -> bool:
    with Session() as session:
        admin = session.query(Admin).get(telegram_id)
        if admin is None:
            return False
        return not admin.teacher_mode
    
def is_admin_teacher_mode(telegram_id: int) -> bool:
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





