# Paciente DAO con Flask + PostgreSQL

Estructura tipo patrón DAO:

- `app/dao/`: acceso a datos SQL.
- `app/services/`: reglas de negocio/validación.
- `app/models.py`: entidad Paciente.
- `app/app.py`: interfaz web Flask.

## Variables como secretos en GitHub

Crea estos secretos en tu repositorio (`Settings > Secrets and variables > Actions`):

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `FLASK_SECRET_KEY`

Luego, en tu workflow, expón los secretos como variables de entorno para ejecutar la app o pruebas.

> Nota: ya no se usa archivo `.env` ni valores por defecto en código. Si falta un secreto, la app falla al iniciar para evitar conexiones inseguras.

## Ejecutar local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.app
```


## ¿Para qué sirve `FLASK_SECRET_KEY`?

Flask la usa para **firmar criptográficamente** cookies de sesión y mensajes flash.
Si no es segura, un atacante podría manipular datos de sesión.

Recomendaciones:
- usar un valor largo, aleatorio y privado;
- guardarlo solo como secreto de GitHub;
- no subirlo al repositorio.
