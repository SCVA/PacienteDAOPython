from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paciente:
    cedula: int
    fechanac: datetime
    primern: str
    segundon: str | None
    primera: str
    segundoa: str | None
