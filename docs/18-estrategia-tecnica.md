# Estratégia Técnica (Config, Segurança e Observabilidade)

Este documento define práticas mínimas para operação do KotaJá (MVP), com foco em segurança e manutenibilidade.

---

## 1. Configuração por ambiente

### Variáveis de ambiente
O projeto lê configurações via variáveis de ambiente:

- `DATABASE_URL` (obrigatória)  
  Ex.: `postgresql://user:pass@host:5432/kotaja`

- `APP_ENV` (opcional)  
  valores recomendados: `local`, `prod`

---

## 2. Segredos e repositório

- Senhas e URLs com credenciais **não devem** ser commitadas.
- O repositório deve conter um arquivo exemplo:

`/.env.example`

Com:
- `DATABASE_URL=postgresql://user:pass@host:5432/kotaja`

> O `.env` real fica no computador local e é ignorado pelo git.

---

## 3. Segurança (MVP)

### Consulta pública
- Não exige login
- Não permite escrita de dados críticos (apenas log de consulta)
- Queries sempre parametrizadas

### Backoffice
- Documentado como evolução futura
- Não será implementado nesta entrega

---

## 4. Observabilidade mínima (Logging)

### Objetivos
- Registrar erros de conexão
- Registrar falhas inesperadas
- Facilitar debug sem expor dados sensíveis

### Padrão recomendado (MVP)
- usar `logging` padrão do Python
- nível default: `INFO`
- não logar dados sensíveis

---

## 5. Tratamento de erros (MVP)

### Cenários mínimos
- Banco indisponível → UI mostra mensagem amigável
- Consulta sem dados → UI mostra “Sem resultados”
- Parâmetros inválidos → UI bloqueia ou avisa

---

## 6. Deploy (resumo)

### Streamlit Cloud
- deploy a partir da branch principal
- `requirements.txt` define dependências
- `DATABASE_URL` configurada via Secrets do Streamlit Cloud

### PostgreSQL online
- provedor sugerido: Neon / Supabase / Render (opções)
- conexão via `DATABASE_URL`
