# Notas de Modelagem e Regras Operacionais

Este documento registra decisões de modelagem que impactam cálculos e integridade do KotaJá.

---

## 1. Região da loja (fonte da verdade)
A região de uma loja é determinada pelo histórico `store_region_history`.

- A região **vigente** é aquela cujo `valid_to` é `NULL`.
- Alterações de região criam um novo registro com novo `valid_from` e encerram o anterior com `valid_to`.

**Motivo:** permite histórico e análises consistentes ao longo do tempo.

---

## 2. Submissão e aprovação de lojas
- `store_submissions` armazena todas as solicitações de cadastro/alteração.
- `store_reviews` registra a decisão do coordenador (auditoria).
- `stores` representa apenas o cadastro **oficial** (aprovado).

**Regra:** uma loja só entra em operação (planejamento/coleta) se estiver `active = true`.

---

## 3. Coleta de preços (observações)
- `price_observations` registra valores observados por pesquisador, em loja física.
- O mesmo veículo pode ter várias observações no mesmo mês (amostragem).

**Regra:** `price_value > 0` e `observed_at` é obrigatório.

---

## 4. Batch mensal (cálculo de médias)
O batch mensal calcula médias em `monthly_price_averages` a partir de `price_observations`.

**Chave de agregação:**
- `month_ref` (mês de referência)
- `region_id`
- `vehicle_variant_id`

**Campos gerados:**
- `avg_price`
- `sample_size`

**Unicidade garantida:**
- `UNIQUE (month_ref, region_id, vehicle_variant_id)`

---

## 5. Consulta pública (sem login)
A consulta pública obtém os valores a partir de `monthly_price_averages` (e não do dado bruto).

- O sistema registra a consulta em `public_quote_queries`
- O log é gravado mesmo quando não existe resultado (consulta sem retorno).

---

## 6. Auditoria e rastreabilidade
- decisões ficam em `store_reviews`
- execuções de processamento ficam em `batch_runs`
- consultas ficam em `public_quote_queries`

Isso permite análises futuras sem exigir autenticação no módulo público.
