from __future__ import annotations

from dataclasses import asdict
from typing import Any, Optional

from src.db.connection import get_conn
from src.domain.quote_models import QuoteFilters


class QuoteRepository:
    """
    Acesso a dados para Consulta Pública (médias mensais).

    - Lê de monthly_price_averages
    - (Opcional) registra log em public_quote_queries
    """

    def fetch_monthly_average(self, filters: QuoteFilters) -> Optional[dict[str, Any]]:
        """
        Retorna UMA média mensal compatível com os filtros.
        Se vehicle_variant_id for None, retorna qualquer variant da região/mês (primeira encontrada).
        """
        sql = """
            SELECT
              id,
              month_ref,
              region_id,
              vehicle_variant_id,
              avg_price,
              sample_size,
              created_at
            FROM monthly_price_averages
            WHERE month_ref = %s::date
              AND region_id = %s::uuid
              AND (%s::uuid IS NULL OR vehicle_variant_id = %s::uuid)
            ORDER BY created_at DESC
            LIMIT 1;
        """

        # Obs: repetimos o param do vehicle_variant_id 2x por causa do OR
        params = (
            filters.month_ref,
            filters.region_id,
            filters.vehicle_variant_id,
            filters.vehicle_variant_id,
        )

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                row = cur.fetchone()
                return dict(row) if row else None

    def insert_public_query_log(
        self,
        filters: QuoteFilters,
        result_found: bool,
        user_agent: Optional[str] = None,
        ip_hash: Optional[str] = None,
    ) -> None:
        """
        Salva log simples de consulta (sem dados sensíveis em claro).
        """
        sql = """
            INSERT INTO public_quote_queries (
              month_ref,
              region_id,
              brand_id,
              model_id,
              vehicle_variant_id,
              user_agent,
              ip_hash,
              created_at
            )
            VALUES (
              %s::date,
              %s::uuid,
              %s::uuid,
              %s::uuid,
              %s::uuid,
              %s,
              %s,
              now()
            );
        """

        params = (
            filters.month_ref,
            filters.region_id,
            filters.brand_id,
            filters.model_id,
            filters.vehicle_variant_id,
            user_agent,
            ip_hash,
        )

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()
