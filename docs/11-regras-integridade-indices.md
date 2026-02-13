# Regras de Integridade e Índices (PostgreSQL)

Este documento define **constraints** e **índices** recomendados para garantir integridade e performance do KotaJá.

---

## 1. Constraints (Integridade)

### 1.1 Unicidade

**brands**
- `UNIQUE (name)`

**vehicle_models**
- `UNIQUE (brand_id, name)`

**vehicle_variants**
- `UNIQUE (model_id, year, fuel_type, trim, transmission)`

**monthly_price_averages**
- `UNIQUE (month_ref, region_id, vehicle_variant_id)`

---

### 1.2 Validações (CHECK)

**price_observations**
- `CHECK (price_value > 0)`

**store_region_history**
- `CHECK (valid_to IS NULL OR valid_to >= valid_from)`

**public_quote_queries**
- `CHECK (month_ref IS NULL OR month_ref = date_trunc('month', month_ref))`

---

### 1.3 Enum / domínio controlado

**users.role**
- valores: `admin`, `manager`, `coordinator`, `store_owner`, `researcher`

**store_submissions.status**
- valores: `PENDING`, `APPROVED`, `REJECTED`

**store_reviews.decision**
- valores: `APPROVED`, `REJECTED`

---

## 2. Índices (Performance)

### 2.1 Consulta pública (principal)

**monthly_price_averages**
- índice para consultas por mês/região/variante:
  - `(month_ref, region_id, vehicle_variant_id)`

---

### 2.2 Coleta e batch

**price_observations**
- índice para batch mensal:
  - `(observed_at, store_id, vehicle_variant_id)`
- índice para análises por loja:
  - `(store_id, observed_at)`

---

### 2.3 Lojas e região

**store_region_history**
- índice para pegar região atual:
  - `(store_id, valid_to)`
- índice para relatórios por região:
  - `(region_id, valid_from)`

---

### 2.4 Auditoria e histórico

**store_submissions**
- `(status, created_at)`
- `(submitted_by_user_id, created_at)`

**store_reviews**
- `(submission_id, created_at)`
