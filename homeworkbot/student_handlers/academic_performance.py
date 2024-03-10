import asyncio

from telebot.types import CallbackQuery

from database.main_db import student_crud
from homeworkbot import bot
from model.pydantic.student_report import StudentReport
from reports.interactive_report_builder import run_interactive_report_builder


@bot.callback_query_handler(func=lambda call: 'academicPerf_' in call.data)
async def callback_academic_performance(call: CallbackQuery):
    type_callback = call.data.split('_')[0]
    match type_callback:
        case 'academicPerf':
            discipline_id = int(call.data.split('_')[1])
            student = student_crud.get_student_by_tg_id(call.from_user.id)
            await __create_report(call, student.id, discipline_id)
        case _:
            await bot.edit_message_text(
                "Неизвестный формат для обработки данных",
                call.message.chat.id,
                call.message.id
            )


async def __create_report(
        call: CallbackQuery,
        student_id: int,
        discipline_id: int) -> None:
    await bot.edit_message_text(
        "Начинаем формировать отчет",
        call.message.chat.id,
        call.message.id)

    report = await asyncio.gather(
        asyncio.to_thread(run_interactive_report_builder, student_id, discipline_id)
    )
    student_report: StudentReport = report[0]
    text_report = f'<i>Студент</i>: <b>{student_report.full_name}</b>\n'
    text_report += f'<i>Кол-во баллов</i>: {student_report.points}\n'
    text_report += f'<i>Пропущенных дедлайнов</i>: {student_report.deadlines_fails}\n'
    text_report += f'<i>Полностью выполнено лаб</i>: {student_report.lab_completed}\n'
    text_report += f'<i>Выполнено заданий</i>: {student_report.task_completed}\n'
    text_report += f'<i>Task ratio</i>: {student_report.task_ratio}\n'
    await bot.edit_message_text(
        text_report,
        call.message.chat.id,
        call.message.id,
        parse_mode="HTML"
    )