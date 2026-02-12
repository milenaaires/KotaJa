from datetime import date
from decimal import Decimal
from uuid import uuid4
from unittest.mock import Mock

from src.services.quote_service import QuoteService
from src.domain.quote_models import QuoteFilters


def test_get_quote_returns_none_and_logs_when_no_row():
    # Arrange
    repo = Mock()
    log_repo = Mock()
    repo.fetch_monthly_average.return_value = None

    svc = QuoteService(repo=repo, log_repo=log_repo)

    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="df",
        brand_id="vw",
        model_id="fusca",
        vehicle_variant_id=None,
    )

    ua = "pytest-agent"
    ip = "127.0.0.1"
    brand_uuid = uuid4()
    model_uuid = uuid4()

    # Act
    result = svc.get_quote(
        filters=filters,
        user_agent=ua,
        ip=ip,
        brand_id=brand_uuid,
        model_id=model_uuid,
    )

    # Assert
    assert result is None
    repo.fetch_monthly_average.assert_called_once_with(filters)
    log_repo.insert_public_query_log.assert_called_once_with(
        filters,
        user_agent=ua,
        ip=ip,
        brand_id=brand_uuid,
        model_id=model_uuid,
    )


def test_get_quote_converts_decimal_and_uuid_and_logs_on_success():
    # Arrange
    repo = Mock()
    log_repo = Mock()

    region_uuid = uuid4()
    variant_uuid = uuid4()

    repo.fetch_monthly_average.return_value = {
        "avg_price": Decimal("12345.67"),
        "region_id": region_uuid,
        "vehicle_variant_id": variant_uuid,
        "sample_size": 10,
    }

    svc = QuoteService(repo=repo, log_repo=log_repo)

    filters = QuoteFilters(
        month_ref=date(2026, 2, 1),
        region_id="df",
        brand_id=None,
        model_id=None,
        vehicle_variant_id=None,
    )

    # Act
    result = svc.get_quote(filters=filters)

    # Assert
    assert result is not None
    assert result["avg_price"] == 12345.67          # Decimal -> float
    assert result["region_id"] == str(region_uuid)  # UUID -> str
    assert result["vehicle_variant_id"] == str(variant_uuid)  # UUID -> str
    assert result["sample_size"] == 10

    repo.fetch_monthly_average.assert_called_once_with(filters)
    log_repo.insert_public_query_log.assert_called_once_with(
        filters,
        user_agent=None,
        ip=None,
        brand_id=None,
        model_id=None,
    )
