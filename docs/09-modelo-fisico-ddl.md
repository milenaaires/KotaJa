# Modelo Físico — DDL PostgreSQL

> Script base do banco KotaJá com constraints e índices essenciais.

```sql
-- =========================
-- EXTENSÕES
-- =========================
CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- gen_random_uuid()

-- =========================
-- ENUMS
-- =========================
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
    CREATE TYPE user_role AS ENUM ('admin','manager','coordinator','store_owner','researcher');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'submission_status') THEN
    CREATE TYPE submission_status AS ENUM ('PENDING','APPROVED','REJECTED');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'review_decision') THEN
    CREATE TYPE review_decision AS ENUM ('APPROVED','REJECTED');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'plan_status') THEN
    CREATE TYPE plan_status AS ENUM ('DRAFT','PUBLISHED','CLOSED');
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'batch_status') THEN
    CREATE TYPE batch_status AS ENUM ('RUNNING','SUCCESS','FAILED');
  END IF;
END $$;

-- =========================
-- USERS
-- =========================
CREATE TABLE IF NOT EXISTS users (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email           text NOT NULL UNIQUE,
  role            user_role NOT NULL,
  active          boolean NOT NULL DEFAULT true,
  created_at      timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- CATÁLOGO
-- =========================
CREATE TABLE IF NOT EXISTS brands (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name        text NOT NULL UNIQUE,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS vehicle_models (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id    uuid NOT NULL REFERENCES brands(id),
  name        text NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now(),
  UNIQUE (brand_id, name)
);

CREATE TABLE IF NOT EXISTS vehicle_variants (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  model_id      uuid NOT NULL REFERENCES vehicle_models(id),
  year          smallint NOT NULL,
  fuel_type     text NOT NULL,
  trim          text NOT NULL,
  transmission  text NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  UNIQUE (model_id, year, fuel_type, trim, transmission)
);

-- =========================
-- REGIÕES E LOJAS
-- =========================
CREATE TABLE IF NOT EXISTS regions (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name        text NOT NULL UNIQUE,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS stores (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  legal_name   text NOT NULL,
  trade_name   text,
  cnpj         text,
  city         text NOT NULL,
  state        text NOT NULL,
  active       boolean NOT NULL DEFAULT true,
  created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS store_submissions (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  submitted_by_user_id    uuid NOT NULL REFERENCES users(id),
  store_id                uuid REFERENCES stores(id),
  status                  submission_status NOT NULL,
  payload_json            jsonb NOT NULL,
  created_at              timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS store_documents (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  submission_id  uuid NOT NULL REFERENCES store_submissions(id),
  file_name      text NOT NULL,
  file_url       text NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS store_reviews (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  submission_id        uuid NOT NULL REFERENCES store_submissions(id),
  reviewer_user_id     uuid NOT NULL REFERENCES users(id),
  decision             review_decision NOT NULL,
  reason               text,
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS store_region_history (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  store_id    uuid NOT NULL REFERENCES stores(id),
  region_id   uuid NOT NULL REFERENCES regions(id),
  valid_from  date NOT NULL,
  valid_to    date,
  created_at  timestamptz NOT NULL DEFAULT now(),
  CHECK (valid_to IS NULL OR valid_to >= valid_from)
);

-- =========================
-- OPERAÇÃO SEMANAL E COLETA
-- =========================
CREATE TABLE IF NOT EXISTS weekly_plans (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  region_id   uuid NOT NULL REFERENCES regions(id),
  week_start  date NOT NULL,
  status      plan_status NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS weekly_assignments (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  weekly_plan_id          uuid NOT NULL REFERENCES weekly_plans(id),
  researcher_user_id      uuid NOT NULL REFERENCES users(id),
  created_at              timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS weekly_assignment_stores (
  id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  weekly_assignment_id   uuid NOT NULL REFERENCES weekly_assignments(id),
  store_id               uuid NOT NULL REFERENCES stores(id),
  created_at             timestamptz NOT NULL DEFAULT now(),
  UNIQUE (weekly_assignment_id, store_id)
);

CREATE TABLE IF NOT EXISTS price_observations (
  id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  researcher_user_id     uuid NOT NULL REFERENCES users(id),
  store_id               uuid NOT NULL REFERENCES stores(id),
  vehicle_variant_id     uuid NOT NULL REFERENCES vehicle_variants(id),
  price_value            numeric(12,2) NOT NULL CHECK (price_value > 0),
  observed_at            timestamptz NOT NULL,
  notes                  text,
  created_at             timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- BATCH E AGREGAÇÃO
-- =========================
CREATE TABLE IF NOT EXISTS batch_runs (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  month_ref   date NOT NULL,
  status      batch_status NOT NULL,
  started_at  timestamptz NOT NULL DEFAULT now(),
  finished_at timestamptz
);

CREATE TABLE IF NOT EXISTS monthly_price_averages (
  id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  month_ref              date NOT NULL,
  region_id              uuid NOT NULL REFERENCES regions(id),
  vehicle_variant_id     uuid NOT NULL REFERENCES vehicle_variants(id),
  avg_price              numeric(12,2) NOT NULL,
  sample_size            integer NOT NULL,
  created_at             timestamptz NOT NULL DEFAULT now(),
  UNIQUE (month_ref, region_id, vehicle_variant_id)
);

CREATE TABLE IF NOT EXISTS public_quote_queries (
  id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  month_ref              date,
  region_id              uuid REFERENCES regions(id),
  brand_id               uuid REFERENCES brands(id),
  model_id               uuid REFERENCES vehicle_models(id),
  vehicle_variant_id     uuid REFERENCES vehicle_variants(id),
  user_agent             text,
  ip_hash                text,
  created_at             timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- ÍNDICES ESSENCIAIS
-- =========================
CREATE INDEX IF NOT EXISTS idx_obs_batch
  ON price_observations (observed_at, store_id, vehicle_variant_id);

CREATE INDEX IF NOT EXISTS idx_obs_store_time
  ON price_observations (store_id, observed_at);

CREATE INDEX IF NOT EXISTS idx_avg_lookup
  ON monthly_price_averages (month_ref, region_id, vehicle_variant_id);

CREATE INDEX IF NOT EXISTS idx_region_current
  ON store_region_history (store_id, valid_to);

CREATE INDEX IF NOT EXISTS idx_submissions_status_time
  ON store_submissions (status, created_at);

CREATE INDEX IF NOT EXISTS idx_reviews_submission_time
  ON store_reviews (submission_id, created_at);
```