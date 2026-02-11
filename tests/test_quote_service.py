from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

import pytest

from src.domain.quote_models import QuoteFilters
from src.services.quote_service import QuoteService


class FakeQuoteRepo:
    def __init__(self, row):
        self.row = row

    def fetch_monthly_average(self, filters):
        return self.row


def test_ct01_consulta_com_resultado_retorna_dict_normalizado():
    # Simula retorno do banco (como psycopg dict_row)
    row = {
        "avg_price": Decimal("25000.00"),
        "sample_size": 12,
        "region_id": UUID("11111111-1111-1111-1111-111111111111"),
        "vehicle_variant_id": UUID("44444444-4444-4444-4444-444444444444"),
        "month_ref": date(2026, 2, 1),
    }

    svc = QuoteService(FakeQuoteRepo(row))
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        vehicle_variant_id="44444444-4444-4444-4444-444444444444",
    )

    res = svc.get_quote(filters)

    assert res is not None
    assert isinstance(res, dict)

    # Normalizações esperadas
    assert res["avg_price"] == 25000.0
    assert res["sample_size"] == 12
    assert res["region_id"] == "11111111-1111-1111-1111-111111111111"
    assert res["vehicle_variant_id"] == "44444444-4444-4444-4444-444444444444"


def test_ct02_consulta_sem_resultado_retorna_none():
    svc = QuoteService(FakeQuoteRepo(None))
    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="11111111-1111-1111-1111-111111111111",
        vehicle_variant_id=None,
    )

    res = svc.get_quote(filters)
    assert res is None


def test_ct03_erro_no_repo_sobe_excecao():
    class BoomRepo:
        def fetch_monthly_average(self, filters):
            raise Exception("db down")

    svc = QuoteService(BoomRepo())
    filters = QuoteFilters(month_ref=date(2026, 2, 1), region_id="r1", vehicle_variant_id=None)

    # Na estrutura atual, o serviço NÃO trata exceção.
    with pytest.raises(Exception, match="db down"):
        svc.get_quote(filters)
