from database.main_db.database import Session
from model.main_db.teacher import Teacher
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline
from model.main_db.student import Student
from model.main_db.admin import Admin

from model.main_db.teacher_discipline import TeacherDiscipline


def is_teacher(telegram_id: int) -> bool:
    with Session() as session:
        teacher = session.query(Teacher).filter(
            Teacher.telegram_id == telegram_id
        )
        return teacher is not None
    
def get_assign_group_discipline(teacher_tg_id: int, group_id: int) -> list[Discipline]:
    """
    Функция запроса списка дисциплин, которые числятся за преподавателем у конкретной группы

    :param teacher_tg_id: телеграм идентификатор преподавателя
    :param group_id: идентификатор группы

    :return: список дисциплин
    """
    with Session() as session:
        disciplines = session.query(Discipline).join(
            AssignedDiscipline,
            AssignedDiscipline.discipline_id == Discipline.id
        ).join(
            Student,
            Student.id == AssignedDiscipline.student_id
        ).filter(
                Student.group == group_id
        ).join(
            TeacherDiscipline,
            TeacherDiscipline.discipline_id == Discipline.id
        ).join(
            Teacher,
            Teacher.id == TeacherDiscipline.teacher_id
        ).filter(
            Teacher.telegram_id == teacher_tg_id
        ).all()

        return disciplines
    
def switch_teacher_mode_to_admin(teacher_tg_id: int) -> None:
    with Session() as session:
        session.query(Admin).filter(
            Admin.telegram_id == teacher_tg_id
        ).update(
            {'teacher_mode': False}
        )
        session.commit()