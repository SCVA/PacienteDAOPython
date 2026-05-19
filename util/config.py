import os
from pathlib import Path


def _load_local_overrides() -> None:
    """Carga variables locales desde util/config_local.py si existe."""
    local_file = Path(__file__).with_name("config_local.py")
    if local_file.exists():
        local_vars: dict[str, str] = {}
        exec(local_file.read_text(encoding="utf-8"), {}, local_vars)

        for key, value in local_vars.items():
            if key.isupper() and isinstance(value, str):
                os.environ.setdefault(key, value)


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno obligatoria '{name}'. "
            "Configúrala como secreto en GitHub Actions o en util/config_local.py para local."
        )
    return value


_load_local_overrides()


class Config:
    DB_HOST = _required_env("DB_HOST")
    DB_PORT = _required_env("DB_PORT")
    DB_NAME = _required_env("DB_NAME")
    DB_USER = _required_env("DB_USER")
    DB_PASSWORD = _required_env("DB_PASSWORD")
    SECRET_KEY = _required_env("FLASK_SECRET_KEY")
