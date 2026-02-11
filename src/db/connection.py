import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


def _load_env_once() -> None:
    """
    Garante que o .env seja carregado mesmo quando o Streamlit roda a partir de /app.
    """
    project_root = Path(__file__).resolve().parents[2]  # .../KotaJa
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)


def get_database_url() -> str:
    _load_env_once()

    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL não definida. Configure no .env ou nas Secrets do deploy."
        )
    return url


def get_conn():
    return psycopg.connect(get_database_url(), row_factory=dict_row)
