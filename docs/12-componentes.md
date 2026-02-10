# Componentes do Sistema (Technical Design)

Este documento descreve os principais componentes internos do KotaJá e suas responsabilidades.

---

## 1. Visão em Componentes (alto nível)

<pre class="mermaid">
flowchart LR
  UI["UI (Streamlit)"]
  SVC["Camada de Servicos"]
  REPO["Camada de Repositorios"]
  DB[("PostgreSQL")]

  UI -->|"chama casos de uso"| SVC
  SVC -->|"executa consultas"| REPO
  REPO -->|"SQL"| DB
</pre>

---

## 2. Componentes internos (detalhado)

<pre class="mermaid">
flowchart TB
  subgraph UI["Interface (Streamlit)"]
    P1["pages/public_quote.py (consulta publica)"]
    P2["pages/admin_users.py (backoffice - futuro)"]
    P3["pages/catalog.py (backoffice - futuro)"]
  end

  subgraph APP["Aplicacao (Core)"]
    S1["services/quote_service.py"]
    S2["services/log_service.py"]
    S3["services/catalog_service.py (futuro)"]
    S4["services/store_service.py (futuro)"]
    S5["services/batch_service.py (futuro)"]
  end

  subgraph DATA["Dados (Persistencia)"]
    R1["repos/quote_repo.py"]
    R2["repos/log_repo.py"]
    R3["repos/catalog_repo.py (futuro)"]
    R4["repos/store_repo.py (futuro)"]
    R5["repos/batch_repo.py (futuro)"]
    DB[("PostgreSQL")]
  end

  P1 --> S1
  P1 --> S2

  S1 --> R1
  S2 --> R2

  R1 --> DB
  R2 --> DB
</pre>

---

## 3. Responsabilidade por componente

### UI (Streamlit)
- renderiza telas
- captura filtros de consulta
- exibe resultado
- não contém regra de negócio

### Services
- valida entradas
- aplica regras de negócio
- orquestra chamadas a repositórios
- define respostas (DTOs) para a UI

### Repositories
- executa queries SQL
- isola persistência do resto do sistema
- retorna dados em formato simples (dict/rows)

### Banco
- mantém integridade via constraints
- armazena logs de consulta
- armazena agregações mensais
