import os


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno obligatoria '{name}'. "
            "Configúrala como secreto en GitHub Actions."
        )
    return value


class Config:
    DB_HOST = _required_env("DB_HOST")
    DB_PORT = _required_env("DB_PORT")
    DB_NAME = _required_env("DB_NAME")
    DB_USER = _required_env("DB_USER")
    DB_PASSWORD = _required_env("DB_PASSWORD")
    SECRET_KEY = _required_env("FLASK_SECRET_KEY")
