from datetime import date
from unittest.mock import MagicMock

import src.repositories.quote_repository as quote_repo_module
from src.repositories.quote_repository import QuoteRepository
from src.domain.quote_models import QuoteFilters


def _mock_get_conn(monkeypatch, fetchone_return=None):
    """
    Monta mocks para suportar:
      with get_conn() as conn:
          with conn.cursor() as cur:
    Retorna (conn_cm, conn, cur) para asserts.
    """
    cur = MagicMock()
    cur.fetchone.return_value = fetchone_return

    cursor_cm = MagicMock()
    cursor_cm.__enter__.return_value = cur
    cursor_cm.__exit__.return_value = False

    conn = MagicMock()
    conn.cursor.return_value = cursor_cm

    conn_cm = MagicMock()
    conn_cm.__enter__.return_value = conn
    conn_cm.__exit__.return_value = False

    # Patch no módulo onde get_conn foi importado
    monkeypatch.setattr(quote_repo_module, "get_conn", lambda: conn_cm)

    return conn_cm, conn, cur


def test_fetch_monthly_average_returns_dict_when_row_exists(monkeypatch):
    # Arrange
    row = {
        "id": "x",
        "month_ref": date(2026, 2, 1),
        "region_id": "r",
        "vehicle_variant_id": "v",
        "avg_price": 1000,
        "sample_size": 10,
        "created_at": "now",
    }
    _, _, cur = _mock_get_conn(monkeypatch, fetchone_return=row)

    repo = QuoteRepository()
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        vehicle_variant_id="22222222-2222-2222-2222-222222222222",
    )

    # Act
    out = repo.fetch_monthly_average(filters)

    # Assert
    assert out == row

    sql, params = cur.execute.call_args[0]
    assert "FROM monthly_price_averages" in sql
    assert "month_ref = %s::date" in sql
    assert "region_id = %s::uuid" in sql
    assert "vehicle_variant_id = %s::uuid" in sql
    assert params == (
        filters.month_ref,
        filters.region_id,
        filters.vehicle_variant_id,
        filters.vehicle_variant_id,  # repetido por causa do OR
    )
    cur.fetchone.assert_called_once()


def test_fetch_monthly_average_returns_none_when_no_row(monkeypatch):
    # Arrange
    _, _, cur = _mock_get_conn(monkeypatch, fetchone_return=None)

    repo = QuoteRepository()
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        vehicle_variant_id=None,
    )

    # Act
    out = repo.fetch_monthly_average(filters)

    # Assert
    assert out is None

    sql, params = cur.execute.call_args[0]
    assert "FROM monthly_price_averages" in sql
    assert params == (
        filters.month_ref,
        filters.region_id,
        None,
        None,
    )
    cur.fetchone.assert_called_once()


def test_insert_public_query_log_executes_and_commits(monkeypatch):
    # Arrange
    _, conn, cur = _mock_get_conn(monkeypatch, fetchone_return=None)

    repo = QuoteRepository()
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        brand_id="33333333-3333-3333-3333-333333333333",
        model_id="44444444-4444-4444-4444-444444444444",
        vehicle_variant_id=None,
    )

    # Act
    repo.insert_public_query_log(
        filters=filters,
        result_found=True,
        user_agent="pytest",
        ip_hash="hash123",
    )

    # Assert
    sql, params = cur.execute.call_args[0]
    assert "INSERT INTO public_quote_queries" in sql
    assert "month_ref" in sql
    assert "region_id" in sql
    assert "vehicle_variant_id" in sql
    assert "user_agent" in sql
    assert "ip_hash" in sql

    assert params == (
        filters.month_ref,
        filters.region_id,
        filters.brand_id,
        filters.model_id,
        filters.vehicle_variant_id,
        "pytest",
        "hash123",
    )

    conn.commit.assert_called_once()
