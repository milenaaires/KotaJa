# Batch Mensal — Design (Cálculo de Médias)

Este documento descreve o processamento mensal que calcula médias por **região + variante** e persiste em `monthly_price_averages`.

---

## 1. Objetivo
Consolidar preços coletados (`price_observations`) em médias mensais para consulta pública rápida e consistente.

---

## 2. Entradas e Saídas

### Entrada
- `price_observations`
- `store_region_history` (para determinar a região vigente da loja no momento do cálculo)

### Saída
- `monthly_price_averages`
- `batch_runs` (registro de execução)

---

## 3. Chave de agregação
A média mensal é calculada por:

- `month_ref` (mês de referência)
- `region_id`
- `vehicle_variant_id`

---

## 4. Regras do algoritmo (MVP)

### 4.1 Seleção do mês
- `month_ref` representa o primeiro dia do mês (ex.: `2026-02-01`)

### 4.2 Região da loja
A região é determinada pelo registro vigente em `store_region_history`:

- `valid_to IS NULL` (região atual), ou
- período que cobre a data de observação, se o projeto evoluir para histórico completo

> MVP recomendado: usar região vigente (valid_to IS NULL).  
> Evolução: usar validade por data (`observed_at` entre `valid_from` e `valid_to`).

### 4.3 Cálculo
- `avg_price = AVG(price_value)`
- `sample_size = COUNT(*)`

---

## 5. Query de referência (SQL)

### 5.1 Inserção/Atualização das médias
```sql
-- month_ref deve ser passado como parâmetro (ex.: '2026-02-01')
WITH base AS (
  SELECT
    date_trunc('month', po.observed_at)::date AS month_ref,
    srh.region_id,
    po.vehicle_variant_id,
    AVG(po.price_value) AS avg_price,
    COUNT(*)::int AS sample_size
  FROM price_observations po
  JOIN store_region_history srh
    ON srh.store_id = po.store_id
   AND srh.valid_to IS NULL
  WHERE po.observed_at >= date_trunc('month', :month_ref::date)
    AND po.observed_at <  (date_trunc('month', :month_ref::date) + interval '1 month')
  GROUP BY 1,2,3
)
INSERT INTO monthly_price_averages (month_ref, region_id, vehicle_variant_id, avg_price, sample_size, created_at)
SELECT month_ref, region_id, vehicle_variant_id, avg_price, sample_size, now()
FROM base
ON CONFLICT (month_ref, region_id, vehicle_variant_id)
DO UPDATE SET
  avg_price = EXCLUDED.avg_price,
  sample_size = EXCLUDED.sample_size,
  created_at = now();
```

## 6. Registro de execução (batch_runs)
O batch registra:
- month_ref
- status (RUNNING/SUCCESS/FAILED)
- started_at, finished_at

Exemplo (pseudo-fluxo):
- cria batch_runs status RUNNING
- executa agregação
- se sucesso → status SUCCESS, finished_at
- se erro → status FAILED, finished_at

## 7. Critérios de aceite (Batch)
- Para um mês dado, a tabela monthly_price_averages possui 1 linha por (mês, região, variante)
- sample_size condiz com o número de observações consideradas
- Execução registrada em batch_runs