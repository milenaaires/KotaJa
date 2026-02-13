# User Stories

Este documento descreve as **User Stories** do sistema KotaJá, organizadas por persona e alinhadas aos requisitos funcionais.

As histórias seguem o padrão:

> Como <persona>, quero <objetivo> para <benefício>.

---

## 🎭 Personas do Sistema

- Administrador
- Gerente
- Coordenador Regional
- Pesquisador
- Lojista
- Usuário Público

---

# 👤 Administrador

## US-ADM-01 — Cadastro de Usuários
Como **Administrador**,  
quero cadastrar usuários no sistema,  
para controlar o acesso conforme os perfis.

### Critérios de Aceitação
- Deve permitir cadastro por e-mail
- Deve permitir definir papel do usuário
- Deve permitir ativar/desativar usuários

---

# 🧭 Gerente

## US-GER-01 — Gerenciar Catálogo de Veículos
Como **Gerente**,  
quero cadastrar marcas, modelos e variantes,  
para padronizar os dados utilizados nas pesquisas.

### Critérios de Aceitação
- Cadastro de marca
- Cadastro de modelo vinculado à marca
- Cadastro de variantes (ano, combustível, transmissão, etc.)

---

# 🌎 Coordenador Regional

## US-COORD-01 — Aprovar Cadastro de Lojas
Como **Coordenador**,  
quero aprovar ou rejeitar lojas cadastradas,  
para garantir a confiabilidade das fontes de coleta.

### Critérios de Aceitação
- Visualizar dados enviados pelo lojista
- Aprovar ou rejeitar submissões
- Registrar motivo da rejeição

---

## US-COORD-02 — Criar Plano Semanal
Como **Coordenador**,  
quero definir quais lojas cada pesquisador deve visitar,  
para organizar a coleta de dados.

---

# 🔎 Pesquisador

## US-PESQ-01 — Registrar Observação de Preço
Como **Pesquisador**,  
quero registrar preços observados nas lojas,  
para alimentar o sistema com dados reais.

### Critérios de Aceitação
- Selecionar loja
- Selecionar variante do veículo
- Informar preço
- Registrar data da observação

---

## US-PESQ-02 — Cadastrar Loja
Como **Pesquisador**,  
quero sugerir novas lojas,  
para ampliar a cobertura de coleta.

---

# 🏪 Lojista

## US-LOJ-01 — Solicitar Cadastro da Loja
Como **Lojista**,  
quero cadastrar minha loja no sistema,  
para participar da base de pesquisa.

---

# 👥 Usuário Público

## US-PUB-01 — Consultar Preço Médio
Como **Usuário Público**,  
quero consultar preços médios por região e veículo,  
para comparar valores de mercado.

### Critérios de Aceitação
- Não exigir login
- Permitir filtrar por região
- Permitir filtrar por veículo
- Registrar log da consulta

---

# 🤖 Sistema

## US-SYS-01 — Calcular Médias Mensais
Como **Sistema**,  
quero calcular médias mensais automaticamente,  
para disponibilizar dados consolidados.
