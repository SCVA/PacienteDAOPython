import psycopg2
import os

from util.config import Config


def get_connection():
    params = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "dbname": Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
    }

    try:
        return psycopg2.connect(**params)
    except UnicodeDecodeError:
        # Fallback útil en algunos entornos Windows donde libpq emite mensajes
        # de error con codificación local no UTF-8 durante el handshake.
        os.environ.setdefault("PGCLIENTENCODING", "LATIN1")
        conn = psycopg2.connect(**params)
        conn.set_client_encoding("UTF8")
        return conn
