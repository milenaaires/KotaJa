from uuid import uuid4
from unittest.mock import MagicMock

import src.repositories.catalog_repository as catalog_repo_module
from src.repositories.catalog_repository import CatalogRepository


def _mock_get_conn(monkeypatch, rows):
    """
    Monta mocks para suportar:
      with get_conn() as conn, conn.cursor() as cur:
    e retorna (conn_cm, conn, cur) para asserts.
    """
    cur = MagicMock()
    cur.fetchall.return_value = rows

    cursor_cm = MagicMock()
    cursor_cm.__enter__.return_value = cur
    cursor_cm.__exit__.return_value = False

    conn = MagicMock()
    conn.cursor.return_value = cursor_cm

    conn_cm = MagicMock()
    conn_cm.__enter__.return_value = conn
    conn_cm.__exit__.return_value = False

    # IMPORTANT: patch no módulo onde get_conn foi importado
    monkeypatch.setattr(catalog_repo_module, "get_conn", lambda: conn_cm)

    return conn_cm, conn, cur


def test_list_regions_executes_query_and_returns_rows(monkeypatch):
    rows = [{"id": "r1", "name": "DF"}, {"id": "r2", "name": "SP"}]
    _, conn, cur = _mock_get_conn(monkeypatch, rows)

    repo = CatalogRepository()
    out = repo.list_regions()

    assert out == rows
    conn.cursor.assert_called_once()

    sql = cur.execute.call_args[0][0]
    assert "FROM regions" in sql
    assert "ORDER BY name" in sql
    cur.execute.assert_called_once()
    cur.fetchall.assert_called_once()


def test_list_brands_executes_query_and_returns_rows(monkeypatch):
    rows = [{"id": "b1", "name": "VW"}, {"id": "b2", "name": "GM"}]
    _, conn, cur = _mock_get_conn(monkeypatch, rows)

    repo = CatalogRepository()
    out = repo.list_brands()

    assert out == rows
    conn.cursor.assert_called_once()

    sql = cur.execute.call_args[0][0]
    assert "FROM brands" in sql
    assert "ORDER BY name" in sql
    cur.execute.assert_called_once()
    cur.fetchall.assert_called_once()


def test_list_models_passes_brand_id_param(monkeypatch):
    rows = [{"id": "m1", "name": "Fusca"}, {"id": "m2", "name": "Gol"}]
    _, conn, cur = _mock_get_conn(monkeypatch, rows)

    brand_id = uuid4()
    repo = CatalogRepository()
    out = repo.list_models(brand_id)

    assert out == rows
    conn.cursor.assert_called_once()

    sql, params = cur.execute.call_args[0]
    assert "FROM vehicle_models" in sql
    assert "WHERE brand_id = %s" in sql
    assert params == (brand_id,)
    cur.fetchall.assert_called_once()


def test_list_variants_passes_model_id_param_and_returns_rows(monkeypatch):
    rows = [{"id": "v1", "label": "2023 • Gasolina • Comfort • Manual"}]
    _, conn, cur = _mock_get_conn(monkeypatch, rows)

    model_id = uuid4()
    repo = CatalogRepository()
    out = repo.list_variants(model_id)

    assert out == rows
    conn.cursor.assert_called_once()

    sql, params = cur.execute.call_args[0]
    assert "FROM vehicle_variants" in sql
    assert "WHERE model_id = %s" in sql
    assert "ORDER BY year DESC" in sql
    assert params == (model_id,)
    cur.fetchall.assert_called_once()
