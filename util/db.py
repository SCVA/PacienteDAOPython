import os

import psycopg2

from util.config import Config

# Evita problemas de decodificación al recibir mensajes de libpq en Windows.
os.environ.setdefault("PGCLIENTENCODING", "LATIN1")


def get_connection():
    params = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "dbname": Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
    }

    try:
        conn = psycopg2.connect(**params)
        conn.set_client_encoding("UTF8")
        return conn
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            "No se pudo abrir la conexión a PostgreSQL por un error de codificación. "
            "Revisa que DB_HOST, DB_NAME, DB_USER y DB_PASSWORD no tengan caracteres "
            "copiados con codificación inválida y verifica que tu instalación de PostgreSQL "
            "en Windows use UTF-8 o LATIN1."
        ) from exc
