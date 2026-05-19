import os

import psycopg2
from psycopg2 import OperationalError

from util.config import Config

# Evita problemas de decodificación al recibir mensajes de libpq en Windows.
# Se puede sobreescribir con DB_CLIENT_ENCODING/PGCLIENTENCODING si es necesario.
os.environ.setdefault("PGCLIENTENCODING", "UTF8")


def _connect_with_encoding(encoding: str | None):
    params = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "dbname": Config.DB_NAME,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
    }
    if encoding:
        params["options"] = f"-c client_encoding={encoding}"
    return psycopg2.connect(**params)


def _is_possible_encoding_error(exc: Exception) -> bool:
    text = str(exc).lower()
    markers = ("unicode", "codec", "decode", "encoding", "codific")
    return any(marker in text for marker in markers)


def get_connection():
    preferred = os.getenv("DB_CLIENT_ENCODING", "UTF8")
    tried = []

    for encoding in dict.fromkeys([preferred, "UTF8", "LATIN1", None]):
        tried.append(encoding or "DEFAULT")
        try:
            return _connect_with_encoding(encoding)
        except UnicodeDecodeError:
            continue
        except OperationalError as exc:
            if _is_possible_encoding_error(exc):
                continue
            raise

    raise RuntimeError(
        "No se pudo abrir la conexión a PostgreSQL por un error de codificación. "
        f"Se intentaron codificaciones {', '.join(tried)}. "
        "Ajusta DB_CLIENT_ENCODING (por ejemplo UTF8 o LATIN1) y revisa que "
        "DB_HOST, DB_NAME, DB_USER y DB_PASSWORD no tengan caracteres inválidos."
    )
