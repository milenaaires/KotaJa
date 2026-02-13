# Dicionário de Dados

Este dicionário descreve as principais tabelas e campos do KotaJá (PostgreSQL).

---

## 1. Catálogo de Veículos

### brands
**Objetivo:** cadastro de marcas.
- `id (uuid, PK)`: identificador da marca
- `name (text, unique)`: nome da marca
- `created_at (timestamptz)`: data de criação

### vehicle_models
**Objetivo:** modelos vinculados a uma marca.
- `id (uuid, PK)`
- `brand_id (uuid, FK -> brands.id)`
- `name (text)`: nome do modelo
- `created_at (timestamptz)`

### vehicle_variants
**Objetivo:** variação/versão do veículo (ano, combustível, versão).
- `id (uuid, PK)`
- `model_id (uuid, FK -> vehicle_models.id)`
- `year (smallint)`
- `fuel_type (text)`
- `trim (text)`
- `transmission (text)`
- `created_at (timestamptz)`

---

## 2. Lojas, Aprovação e Região

### stores
**Objetivo:** cadastro oficial de lojas aprovadas.
- `id (uuid, PK)`
- `legal_name (text)`: razão social
- `trade_name (text)`: nome fantasia
- `cnpj (text)`: identificador fiscal
- `city (text)`, `state (text)`
- `active (boolean)`
- `created_at (timestamptz)`

### store_submissions
**Objetivo:** submissões de cadastro/alteração de loja (para aprovação).
- `id (uuid, PK)`
- `submitted_by_user_id (uuid, FK -> users.id)`
- `store_id (uuid, FK -> stores.id, nullable)`: loja existente (se edição)
- `status (text)`: PENDING/APPROVED/REJECTED
- `payload_json (text/json)`: snapshot dos dados submetidos
- `created_at (timestamptz)`

### store_documents
**Objetivo:** documentos anexados na submissão.
- `id (uuid, PK)`
- `submission_id (uuid, FK -> store_submissions.id)`
- `file_name (text)`
- `file_url (text)`
- `created_at (timestamptz)`

### store_reviews
**Objetivo:** auditoria de decisões do coordenador sobre submissões.
- `id (uuid, PK)`
- `submission_id (uuid, FK -> store_submissions.id)`
- `reviewer_user_id (uuid, FK -> users.id)`
- `decision (text)`: APPROVED/REJECTED
- `reason (text)`
- `created_at (timestamptz)`

### regions
**Objetivo:** regiões operacionais.
- `id (uuid, PK)`
- `name (text, unique)`
- `created_at (timestamptz)`

### store_region_history
**Objetivo:** históricotopics.
- `id (uuid, PK)`
- `store_id (uuid, FK -> stores.id)`
- `region_id (uuid, FK -> regions.id)`
- `valid_from (date)`
- `valid_to (date, nullable)`
- `created_at (timestamptz)`

---

## 3. Planejamento Semanal e Coleta

### weekly_plans
**Objetivo:** planejamento semanal por região (definido pelo coordenador).
- `id (uuid, PK)`
- `region_id (uuid, FK -> regions.id)`
- `week_start (date)`
- `status (text)`
- `created_at (timestamptz)`

### weekly_assignments
**Objetivo:** designação do pesquisador para uma semana.
- `id (uuid, PK)`
- `weekly_plan_id (uuid, FK -> weekly_plans.id)`
- `researcher_user_id (uuid, FK -> users.id)`
- `created_at (timestamptz)`

### weekly_assignment_stores
**Objetivo:** lista de lojas que o pesquisador deve visitar na semana.
- `id (uuid, PK)`
- `weekly_assignment_id (uuid, FK -> weekly_assignments.id)`
- `store_id (uuid, FK -> stores.id)`
- `created_at (timestamptz)`

### price_observations
**Objetivo:** registros de preços coletados em loja física.
- `id (uuid, PK)`
- `researcher_user_id (uuid, FK -> users.id)`
- `store_id (uuid, FK -> stores.id)`
- `vehicle_variant_id (uuid, FK -> vehicle_variants.id)`
- `price_value (numeric)`
- `observed_at (timestamptz)`
- `notes (text)`
- `created_at (timestamptz)`

---

## 4. Consulta pública, Batch e Médias

### batch_runs
**Objetivo:** execução do batch mensal (processamento/agregação).
- `id (uuid, PK)`
- `month_ref (date)`
- `status (text)`
- `started_at (timestamptz)`
- `finished_at (timestamptz)`

### monthly_price_averages
**Objetivo:** médias mensais por (mês, região, variante).
- `id (uuid, PK)`
- `month_ref (date)`
- `region_id (uuid, FK -> regions.id)`
- `vehicle_variant_id (uuid, FK -> vehicle_variants.id)`
- `avg_price (numeric)`
- `sample_size (integer)`
- `created_at (timestamptz)`

### public_quote_queries
**Objetivo:** log de consultas públicas (sem login), para analytics.
- `id (uuid, PK)`
- `month_ref (date, optional)`
- `region_id (uuid, optional)`
- `brand_id (uuid, optional)`
- `model_id (uuid, optional)`
- `vehicle_variant_id (uuid, optional)`
- `user_agent (text, optional)`
- `ip_hash (text, optional)`
- `created_at (timestamptz)`
