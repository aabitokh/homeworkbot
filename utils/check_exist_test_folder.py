import os
from pathlib import Path

from database.main_db import common_crud


def is_test_folder_exist(discipline_id: int, work_id: int) -> bool:
    discipline = common_crud.get_discipline(discipline_id)
    return os.path.exists(Path.cwd().joinpath(
        discipline.path_to_test
    ).joinpath(str(work_id)))