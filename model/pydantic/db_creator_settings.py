from dataclasses import dataclass


@dataclass
class DbCreatorSettings:
    #вызывается при стартовой инциализации системы
    remote_configuration: bool
    default_admin: int | None = None
    disciplines_path: str = ''
    excel_data_path: str = ''
