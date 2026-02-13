from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.db.connection import get_conn


@dataclass(frozen=True)
class BatchResult:
    month_ref: date
    inserted: int
    updated: int
    status: str


def _month_start(d: date) -> date:
    """Normaliza qualquer data para o primeiro dia do mês."""
    return date(d.year, d.month, 1)


def run_monthly_batch(
    month_ref: date,
    *,
    dry_run: bool = False,
    create_run_record: bool = True,
) -> BatchResult:
    """
    Calcula e persiste médias mensais em monthly_price_averages a partir de price_observations.

    Regras:
    - month_ref é o "mês de referência" (primeiro dia do mês)
    - considera observations com observed_at dentro do mês
    - agrupa por (region_id, vehicle_variant_id)
    - avg_price = AVG(price_value), sample_size = COUNT(*)
    - upsert em monthly_price_averages por (month_ref, region_id, vehicle_variant_id)
    """

    month_ref = _month_start(month_ref)

    # intervalo [month_ref, next_month)
    if month_ref.month == 12:
        next_month = date(month_ref.year + 1, 1, 1)
    else:
        next_month = date(month_ref.year, month_ref.month + 1, 1)

    inserted = 0
    updated = 0

    with get_conn() as conn:
        with conn.cursor() as cur:
            run_id: Optional[str] = None

            if create_run_record:
                cur.execute(
                    """
                    INSERT INTO batch_runs (month_ref, status, started_at)
                    VALUES (%s::date, 'RUNNING', now())
                    RETURNING id::text AS id;
                    """,
                (month_ref,),
             )
            row = cur.fetchone()
            run_id = dict(row)["id"]




            # 1) computa médias por região + variante no mês
            # region_id vem da loja no dia via store_region_history:
            # pega o registro válido onde observed_at::date está entre valid_from e valid_to (ou valid_to NULL)
            cur.execute(
                """
                WITH obs AS (
                  SELECT
                    o.vehicle_variant_id,
                    o.price_value,
                    o.observed_at::date AS obs_date,
                    o.store_id
                  FROM price_observations o
                  WHERE o.observed_at >= %s::date
                    AND o.observed_at <  %s::date
                ),
                obs_with_region AS (
                  SELECT
                    srg.region_id,
                    obs.vehicle_variant_id,
                    obs.price_value
                  FROM obs
                  JOIN store_region_history srg
                    ON srg.store_id = obs.store_id
                   AND srg.valid_from <= obs.obs_date
                   AND (srg.valid_to IS NULL OR srg.valid_to >= obs.obs_date)
                ),
                agg AS (
                  SELECT
                    %s::date AS month_ref,
                    region_id,
                    vehicle_variant_id,
                    ROUND(AVG(price_value)::numeric, 2) AS avg_price,
                    COUNT(*)::int AS sample_size
                  FROM obs_with_region
                  GROUP BY region_id, vehicle_variant_id
                )
                SELECT
                  month_ref, region_id, vehicle_variant_id, avg_price, sample_size
                FROM agg;
                """,
                (month_ref, next_month, month_ref),
            )

            rows = cur.fetchall() or []

            if dry_run:
                # não grava nada
                if create_run_record:
                    cur.execute(
                        """
                        UPDATE batch_runs
                        SET status='SUCCESS', finished_at=now()
                        WHERE id::text = %s;
                        """,
                        (run_id,),
                    )
                conn.commit()
                return BatchResult(month_ref=month_ref, inserted=0, updated=0, status="SUCCESS (dry-run)")

            # 2) upsert em monthly_price_averages
            for (mref, region_id, variant_id, avg_price, sample_size) in rows:
                cur.execute(
                    """
                    INSERT INTO monthly_price_averages (
                      month_ref, region_id, vehicle_variant_id, avg_price, sample_size, created_at
                    )
                    VALUES (%s::date, %s::uuid, %s::uuid, %s::numeric, %s::int, now())
                    ON CONFLICT (month_ref, region_id, vehicle_variant_id)
                    DO UPDATE SET
                      avg_price = EXCLUDED.avg_price,
                      sample_size = EXCLUDED.sample_size,
                      created_at = now()
                    RETURNING (xmax = 0) AS inserted;
                    """,
                    (mref, region_id, variant_id, avg_price, sample_size),
                )
                was_inserted = bool(cur.fetchone()[0])
                if was_inserted:
                    inserted += 1
                else:
                    updated += 1

            if create_run_record:
                cur.execute(
                    """
                    UPDATE batch_runs
                    SET status='SUCCESS', finished_at=now()
                    WHERE id::text = %s;
                    """,
                    (run_id,),
                )

            conn.commit()

    return BatchResult(month_ref=month_ref, inserted=inserted, updated=updated, status="SUCCESS")


if __name__ == "__main__":

    res = run_monthly_batch(date(2026, 2, 1))
    print(res)
