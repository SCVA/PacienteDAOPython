# Paciente DAO con Flask + PostgreSQL

Estructura tipo patrón DAO:

- `dao/`: acceso a datos SQL.
- `services/`: reglas de negocio/validación.
- `models.py`: entidad Paciente.
- `app.py`: interfaz web Flask.

## Variables como secretos en GitHub

Crea estos secretos en tu repositorio (`Settings > Secrets and variables > Actions`):

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `FLASK_SECRET_KEY`

## Ejecutar local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```


## `FLASK_SECRET_KEY`

Flask la usa para **firmar criptográficamente** cookies de sesión y mensajes flash.
Si no es segura, un atacante podría manipular datos de sesión.
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```
