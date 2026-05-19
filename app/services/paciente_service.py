from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from app.dao.paciente_dao import PacienteDAO
from app.models import Paciente


class PacienteService:
    def __init__(self):
        self.dao = PacienteDAO()

    def init_schema(self):
        self.dao.crear_tabla()

    def convertir_fecha(self, fecha_texto):
        zona = ZoneInfo("America/Bogota")
        fecha_texto = fecha_texto.strip()
        if len(fecha_texto) == 10:
            fecha = date.fromisoformat(fecha_texto)
            return datetime.combine(fecha, time.min, tzinfo=zona)
        fecha = datetime.fromisoformat(fecha_texto)
        return fecha if fecha.tzinfo else fecha.replace(tzinfo=zona)

    def validar_cedula(self, cedula):
        ced = str(cedula).strip()
        if not ced.isdigit() or len(ced) > 11:
            raise ValueError("Cédula inválida: solo números y máximo 11 dígitos.")
        return int(ced)

    def crear_paciente(self, form):
        paciente = Paciente(
            cedula=self.validar_cedula(form["cedula"]),
            fechanac=self.convertir_fecha(form["fechanac"]),
            primern=form["primern"].strip(),
            segundon=form.get("segundon", "").strip() or None,
            primera=form["primera"].strip(),
            segundoa=form.get("segundoa", "").strip() or None,
        )
        self.dao.crear(paciente)

    def listar(self):
        return self.dao.listar()

    def eliminar(self, cedula):
        return self.dao.eliminar(self.validar_cedula(cedula))
