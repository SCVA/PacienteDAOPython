import os

import psycopg2
from psycopg2 import OperationalError

from util.config import Config

# Avoid Windows/libpq decode issues in server messages when possible.
# Can be overridden with DB_CLIENT_ENCODING / PGCLIENTENCODING.
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


def _decode_unicode_error(exc: UnicodeDecodeError) -> str | None:
    raw = exc.object
    if not isinstance(raw, (bytes, bytearray)):
        return None

    for encoding in ("utf-8", "latin1", "cp1252"):
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue

    return raw.decode("latin1", errors="replace").strip()


def _normalize_server_message(message: str) -> str:
    # Replace quote variants that frequently break on Windows terminals.
    replacements = {
        "«": '"',
        "»": '"',
        "Ť": '"',
        "ť": '"',
        "“": '"',
        "”": '"',
    }
    for source, target in replacements.items():
        message = message.replace(source, target)
    return message


def _connection_hint_from_message(message: str) -> str | None:
    lowered = message.lower()
    if "no existe la base de datos" in lowered or "database" in lowered and "does not exist" in lowered:
        return (
            f"La base configurada en DB_NAME ('{Config.DB_NAME}') no existe. "
            "Crea esa base o cambia DB_NAME."
        )
    return None


def get_connection():
    preferred = os.getenv("DB_CLIENT_ENCODING", "UTF8")
    tried = []
    decode_messages: list[str] = []

    for encoding in dict.fromkeys([preferred, "UTF8", "LATIN1", None]):
        tried.append(encoding or "DEFAULT")
        try:
            return _connect_with_encoding(encoding)
        except UnicodeDecodeError as exc:
            decoded = _decode_unicode_error(exc)
            if decoded:
                decode_messages.append(decoded)
            continue
        except OperationalError as exc:
            if _is_possible_encoding_error(exc):
                continue
            raise

    if decode_messages:
        first_message = _normalize_server_message(list(dict.fromkeys(decode_messages))[0])
        hint = _connection_hint_from_message(first_message)
        hint_text = f" {hint}" if hint else ""
        raise RuntimeError(
            "No se pudo abrir la conexion a PostgreSQL porque psycopg2 no pudo "
            "decodificar el mensaje de error del servidor. "
            f"Mensaje reportado por PostgreSQL: {first_message}{hint_text}"
        )

    raise RuntimeError(
        "No se pudo abrir la conexion a PostgreSQL por un error de codificacion. "
        f"Se intentaron codificaciones {', '.join(tried)}. "
        "Ajusta DB_CLIENT_ENCODING (por ejemplo UTF8 o LATIN1) y revisa que "
        "DB_HOST, DB_NAME, DB_USER y DB_PASSWORD no tengan caracteres invalidos."
    )
