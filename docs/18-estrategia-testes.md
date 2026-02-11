# Estratégia de Testes (MVP)

Este documento define a estratégia e os casos de teste para o entregável implementado: **Consulta Pública**.

---

## 1. Escopo de Teste

### Incluído (nesta entrega)
- Serviço de consulta (`QuoteService.get_quote`)
- Repositório de consulta (`QuoteRepository.fetch_monthly_average`)
- Repositório de log (`LogRepository.insert_public_query_log`)
- Página Streamlit (validação mínima via testes de service; UI test é opcional)

### Fora do escopo (futuro)
- backoffice (admin/gerente/coordenador)
- batch executando automaticamente (apenas design)

---

## 2. Tipos de Teste

### 2.1 Unitários (principal)
Testar regras do `QuoteService` isolando banco via mocks.

- validação de filtros
- retorno de mensagem
- chamada obrigatória de log

### 2.2 Integração leve (opcional/recomendado)
Testar `repositories` contra um Postgres local (docker) **ou** um banco temporário, validando SQL.

---

## 3. Casos de Teste (Consulta Pública)

### CT-01 — Consulta com resultado
**Dado** filtros válidos  
**Quando** existe registro em `monthly_price_averages`  
**Então**
- `found=True`
- `avg_price` e `sample_size` preenchidos
- log é inserido

---

### CT-02 — Consulta sem resultado
**Dado** filtros válidos  
**Quando** não existe média mensal  
**Então**
- `found=False`
- `message="Sem resultados para os filtros"`
- log é inserido

---

### CT-03 — Filtros inválidos (mês ausente)
**Dado** ausência de `month_ref`  
**Quando** usuário tenta consultar  
**Então**
- `found=False`
- `message` indica erro de filtro
- não executa query de média
- log pode ser registrado como inválido (decisão: **não registrar** no MVP)

---

### CT-04 — Filtros inválidos (região ausente)
Mesma lógica do CT-03.

---

### CT-05 — Banco indisponível (erro no repo)
**Dado** filtros válidos  
**Quando** `fetch_monthly_average` lança exceção  
**Então**
- `found=False`
- `message` amigável (“Sistema indisponível…”)
- log de consulta **não** deve gravar (evitar erro em cascata)

---

## 4. Critérios de Aceite (Consulta Pública)

- Usuário consegue filtrar e consultar sem login
- Sistema retorna média mensal quando existir
- Sistema retorna mensagem clara quando não existir
- Sistema registra log das consultas válidas
- Testes unitários cobrindo os casos CT-01 a CT-05

---

## 5. Ferramentas e Execução

- Framework: `pytest`
- Cobertura: `pytest-cov`

Comandos:
```bash
pytest -q
pytest --cov=src --cov-report=term-missing
