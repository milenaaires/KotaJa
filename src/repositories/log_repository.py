from __future__ import annotations

import hashlib
from typing import Optional
from uuid import UUID

from src.db.connection import get_conn
from src.domain.quote_models import QuoteFilters


class LogRepository:
    """
    Registra auditoria de consultas públicas.
    LGPD-friendly: permite armazenar apenas hash do IP.
    """

    def insert_public_query_log(
        self,
        filters: QuoteFilters,
        user_agent: Optional[str] = None,
        ip: Optional[str] = None,
        brand_id: Optional[UUID] = None,
        model_id: Optional[UUID] = None,
    ) -> None:
        ip_hash = self._hash_ip(ip) if ip else None

        sql = """
            INSERT INTO public_quote_queries (
                month_ref,
                region_id,
                brand_id,
                model_id,
                vehicle_variant_id,
                user_agent,
                ip_hash
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            filters.month_ref,
            filters.region_id,
            brand_id,
            model_id,
            filters.vehicle_variant_id,
            user_agent,
            ip_hash,
        )

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()

    def _hash_ip(self, ip: str) -> str:
        return hashlib.sha256(ip.encode()).hexdigest()
