from __future__ import annotations

from typing import Optional, Dict, Any
from uuid import UUID
from decimal import Decimal

from src.domain.quote_models import QuoteFilters
from src.repositories.quote_repository import QuoteRepository
from src.repositories.log_repository import LogRepository


class QuoteService:
    def __init__(
        self,
        repo: Optional[QuoteRepository] = None,
        log_repo: Optional[LogRepository] = None,
    ):
        self.repo = repo or QuoteRepository()
        self.log_repo = log_repo or LogRepository()

    def get_quote(
        self,
        filters: QuoteFilters,
        user_agent: Optional[str] = None,
        ip: Optional[str] = None,
        brand_id: Optional[UUID] = None,
        model_id: Optional[UUID] = None,
    ) -> Optional[Dict[str, Any]]:
        row = self.repo.fetch_monthly_average(filters)
        if not row:
            # log também “sem resultado” (fica a seu critério; pode comentar se não quiser)
            self.log_repo.insert_public_query_log(
                filters, user_agent=user_agent, ip=ip, brand_id=brand_id, model_id=model_id
            )
            return None

        # log sucesso
        self.log_repo.insert_public_query_log(
            filters, user_agent=user_agent, ip=ip, brand_id=brand_id, model_id=model_id
        )

        out = dict(row)
        if isinstance(out.get("avg_price"), Decimal):
            out["avg_price"] = float(out["avg_price"])
        if isinstance(out.get("region_id"), UUID):
            out["region_id"] = str(out["region_id"])
        if isinstance(out.get("vehicle_variant_id"), UUID):
            out["vehicle_variant_id"] = str(out["vehicle_variant_id"])
        return out
