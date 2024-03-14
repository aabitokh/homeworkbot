from pydantic import BaseModel


class TestLocalSettings(BaseModel):
    """
    Локальные политики конкретной задачи
    """
    lab_number: int
    prohibition: list[str] | None
    restriction: list[str] | None
    resolve_import: list[str] | None


class TestGlobalSettings(BaseModel):
    """
    Глобальные политики всей лабораторной (домашней) работы
    """
    prohibition: list[str] | None
    restriction: list[str] | None


class TestSettings(BaseModel):
    """
    Агрегация политик лабораторной (домашней) работы
    с зависимостями от внешних пакетов
    """
    dependencies: list[str] | None
    global_level: TestGlobalSettings
    local_level: list[TestLocalSettings]