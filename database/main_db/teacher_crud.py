from operator import and_
from database.main_db.database import Session
from model.main_db.teacher import Teacher
from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline
from model.main_db.student import Student
from model.main_db.admin import Admin

from model.main_db.teacher_discipline import TeacherDiscipline
from model.main_db.group import Group
from model.main_db.teacher_group import TeacherGroup


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

def get_assign_groups(teacher_tg_id: int) -> list[Group]:
    """
    Функция запроса списка групп, у которых ведет предметы преподаватель

    :param teacher_tg_id: телеграм идентификатор преподавателя

    :return: список групп
    """
    with Session() as session:
        teacher = session.query(Teacher).filter(
            Teacher.telegram_id == teacher_tg_id
        ).first()
        assign_group = session.query(TeacherGroup).filter(
            TeacherGroup.teacher_id == teacher.id
        ).all()
        assign_group = [it.group_id for it in assign_group]
        assign_group = session.query(Group).filter(
            Group.id.in_(assign_group)
        ).all()
        return assign_group



def get_teacher_disciplines(teacher_tg_id: int) -> list[Discipline]:
    """
    Функция запроса списка дисциплин, которые числятся за преподавателем

    :param teacher_tg_id: телеграм идентификатор преподавателя

    :return: список дисциплин
    """
    with Session() as session:
        disciplines = session.query(Discipline).join(
            TeacherDiscipline,
            TeacherDiscipline.discipline_id == Discipline.id
        ).join(
            Teacher,
            TeacherDiscipline.teacher_id == Teacher.id
        ).filter(
            Teacher.telegram_id == teacher_tg_id
        ).all()
        return disciplines

def get_auth_students(group_id: int) -> list[Student]:
    with Session() as session:
        students = session.query(Student).filter(
            and_(
                Student.group == group_id,
                Student.telegram_id.is_not(None),
            )
        ).all()
        return students
