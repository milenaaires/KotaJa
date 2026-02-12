import pytest
from dataclasses import FrozenInstanceError
from datetime import date
from decimal import Decimal

from src.domain.quote_models import QuoteFilters, QuoteResult


def test_quote_filters_defaults_are_none():
    qf = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="df",
    )

    assert qf.brand_id is None
    assert qf.model_id is None
    assert qf.vehicle_variant_id is None


def test_quote_filters_accepts_optional_fields():
    qf = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="df",
        brand_id="vw",
        model_id="fusca",
        vehicle_variant_id="variant-123",
    )

    assert qf.brand_id == "vw"
    assert qf.model_id == "fusca"
    assert qf.vehicle_variant_id == "variant-123"


def test_quote_filters_is_frozen_and_cannot_be_modified():
    qf = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="df",
    )

    with pytest.raises(FrozenInstanceError):
        qf.region_id = "sp"  # type: ignore[misc]


def test_quote_filters_equality_and_hash():
    a = QuoteFilters(month_ref=date(2026, 2, 1), region_id="df", brand_id="vw")
    b = QuoteFilters(month_ref=date(2026, 2, 1), region_id="df", brand_id="vw")
    c = QuoteFilters(month_ref=date(2026, 2, 1), region_id="df", brand_id="gm")

    assert a == b
    assert a != c
    assert hash(a) == hash(b)

