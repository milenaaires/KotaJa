from __future__ import annotations

from typing import Any, Dict, List

from src.db.connection import get_conn


class PublicQueryRepository:
    def list_recent_enriched(self, limit: int = 10) -> List[Dict[str, Any]]:
        sql = """
        SELECT
            q.created_at,
            r.name AS region_name,
            b.name AS brand_name,
            m.name AS model_name,
            CONCAT(v.year, ' • ', v.fuel_type, ' • ', v.trim, ' • ', v.transmission) AS variant_label,
            q.region_id,
            q.brand_id,
            q.model_id,
            q.vehicle_variant_id,
            q.user_agent,
            q.ip_hash
        FROM public_quote_queries q
        LEFT JOIN regions r ON r.id = q.region_id
        LEFT JOIN brands b ON b.id = q.brand_id
        LEFT JOIN vehicle_models m ON m.id = q.model_id
        LEFT JOIN vehicle_variants v ON v.id = q.vehicle_variant_id
        ORDER BY q.created_at DESC
        LIMIT %s
        """
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (limit,))
                rows = cur.fetchall() or []
        return [dict(r) for r in rows]
