import sqlalchemy
from unittest.mock import MagicMock

import src.db.session as session_module


def test_get_database_url_uses_env_when_set(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    assert session_module.get_database_url() == "postgresql://user:pass@localhost:5432/db"


def test_get_database_url_falls_back_to_sqlite(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert session_module.get_database_url() == "sqlite:///./dev.db"


def test_create_db_engine_sqlite_uses_check_same_thread_false(monkeypatch):
    monkeypatch.setattr(session_module, "get_database_url", lambda: "sqlite:///./dev.db")

    create_engine_mock = MagicMock(return_value="ENGINE")
    monkeypatch.setattr(session_module, "create_engine", create_engine_mock)

    out = session_module.create_db_engine()

    assert out == "ENGINE"
    create_engine_mock.assert_called_once_with(
        "sqlite:///./dev.db",
        future=True,
        echo=False,
        connect_args={"check_same_thread": False},
    )


def test_create_db_engine_non_sqlite_uses_empty_connect_args(monkeypatch):
    monkeypatch.setattr(session_module, "get_database_url", lambda: "postgresql://x")

    create_engine_mock = MagicMock(return_value="ENGINE")
    monkeypatch.setattr(session_module, "create_engine", create_engine_mock)

    out = session_module.create_db_engine()

    assert out == "ENGINE"
    create_engine_mock.assert_called_once_with(
        "postgresql://x",
        future=True,
        echo=False,
        connect_args={},
    )


def test_sessionlocal_is_sessionmaker():
    # SessionLocal foi criado na importação do módulo
    assert isinstance(session_module.SessionLocal, sqlalchemy.orm.session.sessionmaker)
