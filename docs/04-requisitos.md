# Requisitos do Sistema

Este documento apresenta os requisitos funcionais e não funcionais do sistema KotaJá, descrevendo de forma objetiva o comportamento esperado do sistema.

---

## Objetivo

Estabelecer critérios claros sobre o que o sistema deve oferecer, servindo como base para a modelagem de dados, projeto técnico, testes e validação final.

---

## Requisitos Funcionais

### RF01 — Gestão de usuários
O sistema deve permitir que um administrador cadastre, ative e desative usuários com papéis definidos.

### RF02 — Gestão do catálogo de veículos
O sistema deve permitir a manutenção de um catálogo global de veículos, incluindo marcas, modelos e variantes.

### RF03 — Cadastro de lojas
O sistema deve permitir o cadastro de lojas por lojistas e pesquisadores.


### RF04 — Aprovação de lojas
O sistema deve permitir que coordenadores regionais aprovem ou rejeitem lojas cadastradas.

### RF05 — Planejamento semanal
O sistema deve permitir que coordenadores regionais definam semanalmente quais lojas serão pesquisadas por cada pesquisador.

### RF06 — Registro de observações de preços
O sistema deve permitir que pesquisadores registrem preços observados de veículos em lojas atribuídas.

### RF07 — Processamento mensal de dados
O sistema deve executar um processamento periódico para calcular médias mensais a partir das observações registradas.

### RF08 — Consulta pública de cotação
O sistema deve permitir a consulta pública de valores médios de veículos sem necessidade de autenticação.

### RF09 — Registro de consultas públicas
O sistema deve armazenar informações sobre todas as consultas públicas realizadas, independentemente de haver resultado.

## Requisitos Não Funcionais

### RNF01 — Segurança
O sistema deve restringir ações de acordo com o papel do usuário, garantindo controle de acesso baseado em perfis.

### RNF02 — Rastreabilidade
O sistema deve registrar informações básicas de auditoria para ações relevantes, incluindo autor e data.

### RNF03 — Desempenho
As consultas públicas devem retornar resultados em tempo adequado para uso interativo.

### RNF04 — Confiabilidade
O processamento mensal deve ser idempotente, permitindo reexecução sem gerar inconsistências.

### RNF05 — Manutenibilidade
O sistema deve ser estruturado de forma modular, facilitando manutenção e evolução futura.

### RNF06 — Usabilidade
A interface pública de consulta deve ser simples, clara e acessível para usuários não autenticados.

### RNF07 — Persistência
Os dados devem ser armazenados em banco de dados relacional, garantindo integridade e consistência.

## Priorização (escopo do trabalho)

## Responsáveis por requisito 

| Requisito | Papel principal |
|---|---|
| RF01 | Admin |
| RF02 | Gerente |
| RF03 | Lojista / Pesquisador |
| RF04 | Coordenador |
| RF05 | Coordenador |
| RF06 | Pesquisador |
| RF07 | Sistema (Batch) |
| RF08 | Usuário Público |
| RF09 | Sistema |


- **MVP (documentação, modelagem e definição)**: RF01 a RF09.
- **Implementação prática neste projeto**: RF08 (Consulta pública) e RF09 (Registro de consultas).
- As demais funcionalidades são especificadas e modeladas, mas não serão implementadas nesta fase.
