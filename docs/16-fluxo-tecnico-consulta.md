# Fluxo Técnico — Consulta Pública 

Este fluxo descreve a implementação da consulta pública, sem login, incluindo registro de log em banco.

---

## 1. Diagrama de Sequência (consulta)

<pre class="mermaid">
sequenceDiagram
  actor U as Usuário Público
  participant UI as Streamlit (UI)
  participant SVC as QuoteService
  participant RQ as QuoteRepository
  participant RL as LogRepository
  participant DB as PostgreSQL

  U->>UI: Seleciona filtros (mês, região, marca/modelo/variante)
  UI->>SVC: get_quote(filters)

  SVC->>SVC: valida filtros (campos obrigatórios)

  SVC->>RQ: fetch_monthly_average(filters)
  RQ->>DB: SELECT monthly_price_averages ...
  DB-->>RQ: resultado (avg_price, sample_size) ou vazio
  RQ-->>SVC: result | None

  SVC->>RL: insert_public_query_log(filters, result_found)
  RL->>DB: INSERT public_quote_queries ...
  DB-->>RL: ok

  SVC-->>UI: resposta (valor ou mensagem sem resultado)
  UI-->>U: Exibe resultado
</pre>

---

## 2. Regras do fluxo

### 2.1 Fonte do resultado
A consulta pública utiliza exclusivamente:
- `monthly_price_averages`

A consulta não lê dados brutos de `price_observations`.

### 2.2 Log obrigatório
Toda consulta registra:
- filtros usados
- timestamp
- user_agent (opcional)
- ip_hash (opcional)
- se houve resultado (derivado do retorno)

---

## 3. Tratamento de erro (MVP)

- Se filtros mínimos não forem preenchidos: UI bloqueia/avisa.
- Se banco estiver indisponível: mostrar mensagem amigável e não travar a UI.
- Se não houver resultado: mensagem “Sem resultados para os filtros”.

---

## 4. Contrato do serviço (assinatura)

`QuoteService.get_quote(filters)` retorna:

- `found: bool`
- `avg_price: decimal | None`
- `sample_size: int | None`
- `message: str`
