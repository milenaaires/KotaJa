# Contratos — Serviços e Repositórios (TD)

Este documento define as interfaces principais para implementar a **consulta pública** do KotaJá.

---

## 1. Tipos (DTOs)

### 1.1 QuoteFilters
Representa os filtros escolhidos pelo usuário.

- `month_ref: date` (mês de referência)
- `region_id: uuid`
- `brand_id: uuid | None`
- `model_id: uuid | None`
- `vehicle_variant_id: uuid | None`

> Nota: no MVP, `vehicle_variant_id` é o filtro mais importante (consulta direta).  
> `brand_id/model_id` podem ser usados para preencher selects encadeados.

---

### 1.2 QuoteResult
Retorno da consulta pública.

- `found: bool`
- `avg_price: decimal | None`
- `sample_size: int | None`
- `message: str`

---

## 2. Serviço

## 2.1 QuoteService

### Responsabilidade
- Validar filtros
- Consultar média mensal via repositório
- Registrar log da consulta
- Montar resposta para a UI

### Interface (assinaturas)
- `get_quote(filters: QuoteFilters, user_agent: str | None = None, ip_hash: str | None = None) -> QuoteResult`

### Regras
- Se filtros mínimos inválidos → `found=False`, `message` informativa
- Se consulta não retornar dado → `found=False`, `message="Sem resultados..."`
- Sempre registrar log, independentemente do resultado

---

## 3. Repositórios

## 3.1 QuoteRepository

### Responsabilidade
Executar consulta em `monthly_price_averages`.

### Interface
- `fetch_monthly_average(filters: QuoteFilters) -> tuple[decimal, int] | None`

**Retorno:**
- `(avg_price, sample_size)` quando existir média
- `None` quando não existir

---

## 3.2 LogRepository

### Responsabilidade
Registrar consultas públicas em `public_quote_queries`.

### Interface
- `insert_public_query_log(filters: QuoteFilters, user_agent: str | None, ip_hash: str | None) -> None`

**Regras:**
- deve persistir pelo menos `month_ref`, `region_id`, `brand_id`, `model_id`, `vehicle_variant_id`
- `user_agent` e `ip_hash` são opcionais

---

## 4. Banco/Conexão

## 4.1 DB Connection (src/db)

### Responsabilidade
- Abrir conexão com PostgreSQL
- Ler `DATABASE_URL` (env)
- Fornecer `get_conn()` reutilizável

### Interface
- `get_conn() -> connection`

---

## 5. Observações de implementação (MVP)

- Queries devem ser parametrizadas (evitar SQL injection)
- UI nunca acessa banco diretamente
- Caso ocorra erro de banco: retornar mensagem amigável e logar erro (futuro)
