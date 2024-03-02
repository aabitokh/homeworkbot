import os
from database.main_db.database import Session
from model.main_db.admin import Admin
from database.main_db.teacher_crud import is_teacher
from model.main_db.chat import Chat
from model.main_db.teacher import Teacher
from model.main_db.group import Group
from model.main_db.teacher_group import TeacherGroup

from model.main_db.assigned_discipline import AssignedDiscipline
from model.main_db.discipline import Discipline
from model.main_db.student import Student
from utils.disciplines_utils import disciplines_works_from_json
from utils.homeworks_utils import create_homeworks, homeworks_to_json
from model.pydantic.discipline_works import DisciplineWorksConfig
from utils.disciplines_utils import disciplines_works_from_json, disciplines_works_to_json, counting_tasks
from sqlalchemy.exc import IntegrityError
from database.main_db.crud_exceptions import DisciplineNotFoundException, GroupAlreadyExistException
from model.pydantic.students_group import StudentsGroup
from model.main_db.teacher_discipline import TeacherDiscipline


from database.main_db.crud_exceptions import DisciplineNotFoundException, GroupAlreadyExistException, \
    DisciplineAlreadyExistException, GroupNotFoundException

from model.pydantic.db_start_data import DbStartData



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

def get_teachers() -> list[Teacher]:
    with Session() as session:
        return session.query(Teacher).all()


def get_not_assign_teacher_groups(teacher_id: int) -> list[Group]:
    with Session() as session:
        assign_group = session.query(TeacherGroup).filter(
            TeacherGroup.teacher_id == teacher_id
        )
        assign_group = [it.group_id for it in assign_group]
        not_assign_group = session.query(Group).filter(
            Group.id.not_in(assign_group)
        ).all()
        return not_assign_group


def assign_teacher_to_group(teacher_id: int, group_id: int) -> None:
    with Session() as session:
        session.add(TeacherGroup(teacher_id=teacher_id, group_id=group_id))
        session.commit()

def get_all_groups() -> list[Group]:
    with Session() as session:
        return session.query(Group).all()


def add_student(full_name: str, group_id: int, discipline_id: int):

    session = Session()
    student = Student(full_name=full_name, group=group_id)
    session.add(student)
    session.flush()
    discipline: Discipline = session.query(Discipline).get(discipline_id)
    empty_homework = create_homeworks(
        disciplines_works_from_json(discipline.works)
    )
    #print(empty_homework)
    session.add(
        AssignedDiscipline(
            student_id=student.id,
            discipline_id=discipline_id,
            home_work=homeworks_to_json(empty_homework)
        )
    )
    session.commit()
    session.close()

def add_discipline(discipline: DisciplineWorksConfig) -> None:
    with Session() as session:
        session.add(
            Discipline(
                full_name=discipline.full_name,
                short_name=discipline.short_name,
                path_to_test=discipline.path_to_test,
                path_to_answer=discipline.path_to_answer,
                works=disciplines_works_to_json(discipline),
                language=discipline.language,
                max_tasks=counting_tasks(discipline),
                max_home_works=len(discipline.works)
            )
        )
        session.commit()


def add_students_group(student_groups: list[StudentsGroup]) -> None:
    """
    Функция добавления групп студентов

    :param student_groups: Список с параметрами групп

    :raises DisciplineNotFoundException: дисциплина не найдена
    :raises GroupAlreadyExistException: если группа с таким названием уже существует

    :return: None
    """
    session = Session()
    session.begin()
    try:
        for it in student_groups:
            group = Group(group_name=it.group_name)
            session.add(group)
            session.flush()
            students = [Student(full_name=student_raw, group=group.id) for student_raw in it.students]
            session.add_all(students)
            session.flush()
            for discipline in it.disciplines_short_name:
                current_discipline = session.query(Discipline).filter(
                    Discipline.short_name.ilike(f"%{discipline}%")
                ).first()
                if current_discipline is None:
                    raise DisciplineNotFoundException(f'{discipline} нет в БД')

                empty_homework = create_homeworks(
                    disciplines_works_from_json(current_discipline.works)
                )
                session.add_all([
                    AssignedDiscipline(
                        student_id=student.id,
                        discipline_id=current_discipline.id,
                        home_work=homeworks_to_json(empty_homework)
                    ) for student in students]
                )
        session.commit()
    except DisciplineNotFoundException as ex:
        session.rollback()
        raise ex
    except IntegrityError as ex:
        session.rollback()
        raise GroupAlreadyExistException(f'{ex.params[0]} уже существует')
    finally:
        session.close()

def assign_teacher_to_discipline(teacher_id: int, discipline_id: int) -> None:
    with Session() as session:
        session.add(TeacherDiscipline(teacher_id=teacher_id, discipline_id=discipline_id))
        session.commit()


def get_not_assign_teacher_discipline(teacher_id: int) -> list[Discipline]:
    with Session() as session:
        assign_discipline = session.query(TeacherDiscipline).filter(
            TeacherDiscipline.teacher_id == teacher_id
        )
        assign_discipline = [it.discipline_id for it in assign_discipline]
        not_assign_discipline = session.query(Discipline).filter(
            Discipline.id.not_in(assign_discipline)
        ).all()
        return not_assign_discipline
    
def delete_group(group_id: int) -> None:
    with Session() as session:
        session.query(Group).filter(
            Group.id == group_id
        ).delete(synchronize_session='fetch')
        session.query(TeacherGroup).filter(
            TeacherGroup.group_id == group_id
        ).delete(synchronize_session='fetch')

        students = session.query(Student).filter(Student.group == group_id).all()

        if not students:
            session.commit()
            return
        students_id = [it.id for it in students]
        session.query(AssignedDiscipline).filter(
            AssignedDiscipline.student_id.in_(students_id)
        ).delete(synchronize_session='fetch')
        session.query(Student).filter(Student.group == group_id).delete(synchronize_session='fetch')
        session.commit()


def delete_student(student_id: int) -> None:
    with Session() as session:
        session.query(Student).filter(Student.id == student_id).delete(synchronize_session='fetch')
        session.query(AssignedDiscipline).filter(
            AssignedDiscipline.student_id == student_id
        ).delete(synchronize_session='fetch')
        session.commit()


def delete_teacher(teacher_id: int) -> None:
    with Session() as session:
        session.query(Teacher).filter(
            Teacher.id == teacher_id
        ).delete(synchronize_session='fetch')

        session.query(TeacherGroup).filter(
            TeacherGroup.teacher_id == teacher_id
        ).delete(synchronize_session='fetch')

        session.query(TeacherDiscipline).filter(
            TeacherDiscipline.teacher_id == teacher_id
        ).delete(synchronize_session='fetch')

        session.commit()

def get_all_disciplines() -> list[Discipline]:
    with Session() as session:
        return session.query(Discipline).all()


def get_discipline(discipline_id: int) -> Discipline:
    with Session() as session:
        return session.query(Discipline).get(discipline_id)

def remote_start_db_fill(data: DbStartData) -> None:
    """
    Функция для стартовой конфигурации системы через загрузку json-файла

    :param data: данные по предметам, студентам, группам и преподавателям, а также
    какие дисциплины кому назначены и какой преподаватель их ведет

    :raises DisciplineNotFoundException: дисциплина не найдена
    :raises DisciplineAlreadyExistException: дисциплина уже существует (дублируется)
    :raises GroupAlreadyExistException: если группа с таким названием уже существует
    :raises GroupNotFoundException: если группа с таким названием не найдена

    :return: None
    """
    session = Session()
    session.begin()
    admin_default_tg = int(os.getenv("DEFAULT_ADMIN"))
    dis_short_names = {}
    groups_name = {}

    try:
        for discipline in data.disciplines:
            if discipline.short_name in dis_short_names:
                raise DisciplineAlreadyExistException(f"{discipline.short_name} дублируется")
            dis = Discipline(
                    full_name=discipline.full_name,
                    short_name=discipline.short_name,
                    path_to_test=discipline.path_to_test,
                    path_to_answer=discipline.path_to_answer,
                    works=disciplines_works_to_json(discipline),
                    language=discipline.language,
                    max_tasks=counting_tasks(discipline),
                    max_home_works=len(discipline.works)
                )
            session.add(dis)
            session.flush()
            dis_short_names[discipline.short_name] = dis.id

        for it in data.groups:
            group = Group(group_name=it.group_name)
            session.add(group)
            session.flush()
            groups_name[it.group_name] = group.id

            students = [
                Student(
                    full_name=student_raw,
                    group=group.id)
                for student_raw in it.students
            ]
            session.add_all(students)
            session.flush()

            for discipline in it.disciplines_short_name:
                current_discipline = session.query(Discipline).filter(
                    Discipline.short_name.ilike(f"%{discipline}%")
                ).first()
                if current_discipline is None:
                    raise DisciplineNotFoundException(f'{discipline} нет в БД')

                empty_homework = create_homeworks(
                    disciplines_works_from_json(current_discipline.works)
                )
                session.add_all([
                    AssignedDiscipline(
                        student_id=student.id,
                        discipline_id=current_discipline.id,
                        home_work=homeworks_to_json(empty_homework)
                    ) for student in students]
                )

        for it in data.teachers:
            teacher = Teacher(
                full_name=it.full_name,
                telegram_id=it.telegram_id
            )
            session.add(teacher)
            session.flush()
            for tgr in it.assign_groups:
                if tgr not in groups_name:
                    raise GroupNotFoundException(f'Группа {tgr} не найдена')
                session.add(
                    TeacherGroup(
                        teacher_id=teacher.id,
                        group_id=groups_name[tgr]
                    )
                )

            for tdis in it.assign_disciplines:
                if tdis not in dis_short_names:
                    raise DisciplineNotFoundException(f'Дисчиплина {tdis} не найдена')
                session.add(
                    TeacherDiscipline(
                        teacher_id=teacher.id,
                        discipline_id=dis_short_names[tdis]
                    )
                )

            if it.is_admin and teacher.telegram_id != admin_default_tg:
                session.add(
                    Admin(
                        telegram_id=teacher.telegram_id
                    )
                )

        for chat in data.chats:
            session.add(
                Chat(chat_id=chat)
            )
        session.commit()
    except DisciplineNotFoundException as ex:
        session.rollback()
        raise ex
    except DisciplineAlreadyExistException as daex:
        session.rollback()
        raise daex
    except GroupNotFoundException as gnfex:
        session.rollback()
        raise gnfex
    except IntegrityError as ex:
        session.rollback()
        raise GroupAlreadyExistException(f'{ex.params[0]} уже существует')
    finally:
        session.close()