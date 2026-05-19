from flask import Flask, flash, redirect, render_template, request, url_for

from app.config import Config
from app.services.paciente_service import PacienteService


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    service = PacienteService()
    service.init_schema()

    @app.get("/")
    def index():
        pacientes = service.listar()
        return render_template("index.html", pacientes=pacientes)

    @app.post("/pacientes")
    def crear_paciente():
        try:
            service.crear_paciente(request.form)
            flash("Paciente creado correctamente.", "success")
        except Exception as exc:
            flash(f"No se pudo crear el paciente: {exc}", "error")
        return redirect(url_for("index"))

    @app.post("/pacientes/<cedula>/eliminar")
    def eliminar_paciente(cedula):
        filas = service.eliminar(cedula)
        if filas:
            flash("Paciente eliminado.", "success")
        else:
            flash("No existe un paciente con esa cédula.", "error")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
