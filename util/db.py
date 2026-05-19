import psycopg2
from urllib.parse import quote

from util.config import Config


def get_connection():
    dsn = (
        "postgresql://"
        f"{quote(Config.DB_USER, safe='')}:"
        f"{quote(Config.DB_PASSWORD, safe='')}@"
        f"{quote(Config.DB_HOST, safe='')}:"
        f"{quote(Config.DB_PORT, safe='')}/"
        f"{quote(Config.DB_NAME, safe='')}"
    )
    return psycopg2.connect(dsn)
