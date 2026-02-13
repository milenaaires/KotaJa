# Decisões de Design (Design Decisions)

Este documento descreve as principais decisões arquiteturais e padrões adotados no KotaJá, justificando escolhas técnicas e trade-offs.

---

## 1. Arquitetura em Camadas (Layered Architecture)

### Decisão
Separar o sistema nas camadas:

- Interface (Streamlit)
- Services (regras de negócio)
- Repositories (acesso a dados)
- Banco de Dados (PostgreSQL)

### Justificativa
- Reduz acoplamento entre UI e banco
- Facilita testes unitários
- Permite evolução futura do backend sem alterar UI

### Trade-off
- Mais arquivos e estrutura inicial maior
- Leve aumento de complexidade para MVP

---

## 2. Padrão Service + Repository

### Decisão
Utilizar Services para orquestrar regras de negócio e Repositories para acesso ao banco.

### Justificativa
- Mantém SQL isolado
- Facilita reutilização de lógica
- Permite mockar repositórios em testes

### Trade-off
- Mais código intermediário
- Requer disciplina de separação de responsabilidades

---

## 3. Uso de DTOs Simples (Data Transfer Objects)

### Decisão
Representar entrada e saída dos serviços com estruturas simples (dataclass ou dicionários tipados).

### Justificativa
- Padroniza comunicação entre camadas
- Facilita manutenção e leitura do código
- Evita dependência direta da estrutura do banco

### Trade-off
- Necessidade de conversão entre formatos

---

## 4. Persistência via PostgreSQL

### Decisão
Utilizar PostgreSQL como banco principal.

### Justificativa
- Suporte a JSONB
- Integridade forte via constraints
- Boa performance para agregações
- Compatível com provedores cloud

### Trade-off
- Requer configuração externa (não embutido como SQLite)

---

## 5. Agregação Mensal via Batch

### Decisão
Calcular médias mensalmente e armazenar em tabela dedicada (`monthly_price_averages`).

### Justificativa
- Consulta pública mais rápida
- Reduz carga sobre dados brutos
- Permite análises estatísticas futuras

### Trade-off
- Dados não são atualizados em tempo real
- Requer processo batch adicional

---

## 6. Streamlit como Interface

### Decisão
Utilizar Streamlit como framework de UI.

### Justificativa
- Desenvolvimento rápido
- Integração simples com Python
- Adequado para dashboards e formulários

### Trade-off
- Menos controle sobre front-end comparado a frameworks SPA
- Escalabilidade limitada para alto volume simultâneo

---

## 7. Consulta Pública sem Autenticação

### Decisão
Permitir consulta de preços sem login.

### Justificativa
- Reduz barreira de uso
- Aproxima comportamento de referência FIPE
- Mantém rastreabilidade via logs

### Trade-off
- Menor controle de abuso
- Necessidade futura de rate limiting

---

## 8. Registro de Logs de Consulta

### Decisão
Registrar todas as consultas públicas em `public_quote_queries`.

### Justificativa
- Permite analytics e melhoria do produto
- Permite auditoria de uso
- Não exige autenticação do usuário

---

## 9. Uso de Variáveis de Ambiente

### Decisão
Configurar conexões e parâmetros via environment variables.

### Justificativa
- Segurança
- Portabilidade entre ambientes
- Compatibilidade com Streamlit Cloud

---

## 10. Separação entre UI e Núcleo da Aplicação

### Decisão
Manter `app/` separado de `src/`.

### Justificativa
- Facilita manutenção
- Permite reutilização futura do backend
- Facilita testes automatizados

---

## 11. Queries Parametrizadas

### Decisão
Todas as consultas SQL utilizam parâmetros.

### Justificativa
- Previne SQL injection
- Mantém segurança do sistema
- Boa prática de desenvolvimento
