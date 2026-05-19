import os

import psycopg2

from util.config import Config

# Evita problemas de decodificación al recibir mensajes de libpq en Windows.
os.environ.setdefault("PGCLIENTENCODING", "LATIN1")


def _connect_with_encoding(encoding: str):
    params = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "dbname": Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
        "options": f"-c client_encoding={encoding}",
    }
    return psycopg2.connect(**params)


def get_connection():
    preferred = os.getenv("DB_CLIENT_ENCODING", "LATIN1")
    tried = []

    for encoding in dict.fromkeys([preferred, "LATIN1", "UTF8"]):
        tried.append(encoding)
        try:
            return _connect_with_encoding(encoding)
        except UnicodeDecodeError:
            continue

    raise RuntimeError(
        "No se pudo abrir la conexión a PostgreSQL por un error de codificación. "
        f"Se intentaron codificaciones {', '.join(tried)}. "
        "Ajusta DB_CLIENT_ENCODING (por ejemplo LATIN1 o UTF8) y revisa que "
        "DB_HOST, DB_NAME, DB_USER y DB_PASSWORD no tengan caracteres inválidos."
    )
