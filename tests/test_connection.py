import pytest
from unittest.mock import MagicMock

import src.db.connection as conn_module


# -------------------------
# Fakes pra simular Path(...)
# -------------------------
class _FakeEnvPath:
    def __init__(self, path: str, exists: bool):
        self.path = path
        self._exists = exists

    def exists(self) -> bool:
        return self._exists

    def __repr__(self) -> str:
        return f"_FakeEnvPath({self.path!r}, exists={self._exists})"


class _FakeRootPath:
    def __init__(self, root: str, env_exists: bool):
        self.root = root
        self.env_exists = env_exists

    def __truediv__(self, other: str):
        # root / ".env"
        return _FakeEnvPath(f"{self.root}/{other}", self.env_exists)


class _FakeFilePath:
    def __init__(self, env_exists: bool):
        self._root = _FakeRootPath("FAKE_PROJECT_ROOT", env_exists)

    def resolve(self):
        return self

    @property
    def parents(self):
        # precisa ter index 2
        return [None, None, self._root]


def _patch_fake_path(monkeypatch, env_exists: bool):
    # conn_module.Path(__file__) -> _FakeFilePath(env_exists)
    monkeypatch.setattr(conn_module, "Path", lambda *_args, **_kwargs: _FakeFilePath(env_exists))


# -------------------------
# Tests
# -------------------------
def test_load_env_once_calls_load_dotenv_when_env_exists(monkeypatch):
    _patch_fake_path(monkeypatch, env_exists=True)
    load_dotenv_mock = MagicMock()
    monkeypatch.setattr(conn_module, "load_dotenv", load_dotenv_mock)

    conn_module._load_env_once()

    load_dotenv_mock.assert_called_once()
    kwargs = load_dotenv_mock.call_args.kwargs
    assert "dotenv_path" in kwargs
    assert kwargs["dotenv_path"].path.endswith("/.env")


def test_load_env_once_does_nothing_when_env_missing(monkeypatch):
    _patch_fake_path(monkeypatch, env_exists=False)
    load_dotenv_mock = MagicMock()
    monkeypatch.setattr(conn_module, "load_dotenv", load_dotenv_mock)

    conn_module._load_env_once()

    load_dotenv_mock.assert_not_called()


def test_get_database_url_returns_env_and_calls_load_env_once(monkeypatch):
    load_once_mock = MagicMock()
    monkeypatch.setattr(conn_module, "_load_env_once", load_once_mock)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

    url = conn_module.get_database_url()

    assert url == "postgresql://user:pass@localhost:5432/db"
    load_once_mock.assert_called_once()


def test_get_database_url_raises_when_missing(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(conn_module, "_load_env_once", lambda: None)

    with pytest.raises(RuntimeError) as exc:
        conn_module.get_database_url()

    assert "DATABASE_URL não definida" in str(exc.value)


def test_get_conn_calls_psycopg_connect_with_row_factory(monkeypatch):
    monkeypatch.setattr(conn_module, "get_database_url", lambda: "postgresql://x")

    connect_mock = MagicMock(return_value="CONN")
    monkeypatch.setattr(conn_module.psycopg, "connect", connect_mock)

    out = conn_module.get_conn()

    assert out == "CONN"
    connect_mock.assert_called_once_with(
        "postgresql://x",
        row_factory=conn_module.dict_row,
    )
