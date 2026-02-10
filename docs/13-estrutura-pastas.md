# Estrutura de Pastas (Repositório)

A estrutura do repositório separa **Interface (Streamlit)** do **Core da aplicação**.

---

## 1. Visão geral

```text
KotaJa/
├─ app/                      # Interface Streamlit (UI)
│  ├─ app.py                 # Entry point do Streamlit
│  └─ pages/                 # Páginas (multi-page)
│     └─ 1_Consulta.py       # Consulta pública (entregável de código)
│
├─ src/                      # Núcleo da aplicação (regra de negócio)
│  ├─ db/                    # Conexão/config com PostgreSQL
│  ├─ repositories/          # Acesso a dados (SQL)
│  ├─ services/              # Casos de uso / regras
│  └─ domain/                # Tipos/DTOs/validações (opcional)
│
├─ tests/                    # Testes automatizados (pytest)
│
├─ docs/                     # Documentação MkDocs
├─ mkdocs.yml
├─ requirements.txt
└─ README.md
```

## 2. Responsabilidades
### app/
- contém somente UI
- chama services para executar casos de uso
- não contém SQL direto

### src/services/
- valida filtros e regras de negócio
- orquestra chamadas aos repositories

### src/repositories/
- executa SQL e retorna dados
- não contém lógica de UI

### src/db/
- conexão PostgreSQL (ex.: get_conn())
- leitura de variáveis de ambiente (URL do banco)

### tests/
- testes unitários de service e repository
- testes offline usando mocks quando possível