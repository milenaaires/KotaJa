from datetime import date
import hashlib
from unittest.mock import MagicMock
from uuid import uuid4

import src.repositories.log_repository as log_module
from src.repositories.log_repository import LogRepository
from src.domain.quote_models import QuoteFilters


def _mock_get_conn(monkeypatch):
    """
    Monta mocks para suportar:
      with get_conn() as conn:
          with conn.cursor() as cur:
    Retorna (conn_cm, conn, cur).
    """
    cur = MagicMock()

    cursor_cm = MagicMock()
    cursor_cm.__enter__.return_value = cur
    cursor_cm.__exit__.return_value = False

    conn = MagicMock()
    conn.cursor.return_value = cursor_cm

    conn_cm = MagicMock()
    conn_cm.__enter__.return_value = conn
    conn_cm.__exit__.return_value = False

    # Patch no módulo onde get_conn foi importado
    monkeypatch.setattr(log_module, "get_conn", lambda: conn_cm)

    return conn_cm, conn, cur


def test_insert_public_query_log_hashes_ip_and_commits(monkeypatch):
    _, conn, cur = _mock_get_conn(monkeypatch)

    repo = LogRepository()
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        vehicle_variant_id="22222222-2222-2222-2222-222222222222",
    )

    ip = "127.0.0.1"
    expected_hash = hashlib.sha256(ip.encode()).hexdigest()

    brand_id = uuid4()
    model_id = uuid4()

    repo.insert_public_query_log(
        filters=filters,
        user_agent="pytest",
        ip=ip,
        brand_id=brand_id,
        model_id=model_id,
    )

    sql, params = cur.execute.call_args[0]
    assert "INSERT INTO public_quote_queries" in sql

    assert params == (
        filters.month_ref,
        filters.region_id,
        brand_id,
        model_id,
        filters.vehicle_variant_id,
        "pytest",
        expected_hash,
    )

    conn.commit.assert_called_once()


def test_insert_public_query_log_without_ip_sets_ip_hash_none(monkeypatch):
    _, conn, cur = _mock_get_conn(monkeypatch)

    repo = LogRepository()
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        vehicle_variant_id=None,
    )

    repo.insert_public_query_log(
        filters=filters,
        user_agent=None,
        ip=None,
        brand_id=None,
        model_id=None,
    )

    _, params = cur.execute.call_args[0]
    assert params[-1] is None  # ip_hash

    conn.commit.assert_called_once()


def test_hash_ip_matches_sha256():
    repo = LogRepository()
    ip = "10.0.0.5"
    assert repo._hash_ip(ip) == hashlib.sha256(ip.encode()).hexdigest()
