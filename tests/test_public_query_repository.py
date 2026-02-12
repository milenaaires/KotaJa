from unittest.mock import MagicMock

import src.repositories.public_query_repository as pq_module
from src.repositories.public_query_repository import PublicQueryRepository


def _mock_get_conn(monkeypatch, fetchall_return):
    """
    Monta mocks para suportar:
      with get_conn() as conn:
          with conn.cursor() as cur:
    Retorna (conn_cm, conn, cur).
    """
    cur = MagicMock()
    cur.fetchall.return_value = fetchall_return

    cursor_cm = MagicMock()
    cursor_cm.__enter__.return_value = cur
    cursor_cm.__exit__.return_value = False

    conn = MagicMock()
    conn.cursor.return_value = cursor_cm

    conn_cm = MagicMock()
    conn_cm.__enter__.return_value = conn
    conn_cm.__exit__.return_value = False

    # Patch no módulo onde get_conn foi importado
    monkeypatch.setattr(pq_module, "get_conn", lambda: conn_cm)

    return conn_cm, conn, cur


def test_list_recent_enriched_executes_query_and_returns_rows(monkeypatch):
    rows = [
        {"region_name": "DF", "brand_name": "VW"},
        {"region_name": "SP", "brand_name": "GM"},
    ]
    _, _, cur = _mock_get_conn(monkeypatch, fetchall_return=rows)

    repo = PublicQueryRepository()
    out = repo.list_recent_enriched(limit=5)

    assert out == rows

    sql, params = cur.execute.call_args[0]
    assert "FROM public_quote_queries q" in sql
    assert "LEFT JOIN regions" in sql
    assert "LEFT JOIN brands" in sql
    assert "LEFT JOIN vehicle_models" in sql
    assert "LEFT JOIN vehicle_variants" in sql
    assert "ORDER BY q.created_at DESC" in sql
    assert "LIMIT %s" in sql
    assert params == (5,)

    cur.fetchall.assert_called_once()


def test_list_recent_enriched_returns_empty_list_when_fetchall_none(monkeypatch):
    _, _, cur = _mock_get_conn(monkeypatch, fetchall_return=None)

    repo = PublicQueryRepository()
    out = repo.list_recent_enriched(limit=10)

    assert out == []
    cur.execute.assert_called_once()
    cur.fetchall.assert_called_once()
