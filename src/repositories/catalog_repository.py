from __future__ import annotations

from typing import List, Dict, Any, Optional
from uuid import UUID

from src.db.connection import get_conn


class CatalogRepository:
    def list_regions(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT id, name
            FROM regions
            ORDER BY name;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql)
            return [dict(r) for r in cur.fetchall()]

    def list_brands(self) -> List[Dict[str, Any]]:
        sql = """
            SELECT id, name
            FROM brands
            ORDER BY name;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql)
            return [dict(r) for r in cur.fetchall()]

    def list_models(self, brand_id: UUID) -> List[Dict[str, Any]]:
        sql = """
            SELECT id, name
            FROM vehicle_models
            WHERE brand_id = %s
            ORDER BY name;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (brand_id,))
            return [dict(r) for r in cur.fetchall()]

    def list_variants(self, model_id: UUID) -> List[Dict[str, Any]]:
        sql = """
            SELECT id,
                   (year::text || ' • ' || fuel_type || ' • ' || trim || ' • ' || transmission) AS label
            FROM vehicle_variants
            WHERE model_id = %s
            ORDER BY year DESC, fuel_type, trim, transmission;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (model_id,))
            return [dict(r) for r in cur.fetchall()]
