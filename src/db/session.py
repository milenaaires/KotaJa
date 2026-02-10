import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_database_url() -> str:
    # Começa simples: se não tiver DATABASE_URL, usa SQLite local.
    return os.getenv("DATABASE_URL", "sqlite:///./dev.db")


def create_db_engine():
    url = get_database_url()
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, future=True, echo=False, connect_args=connect_args)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_db_engine())
