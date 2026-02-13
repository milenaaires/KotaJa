# Papéis e Responsabilidades do Sistema

Este documento descreve os perfis operacionais do sistema KotaJá e suas respectivas responsabilidades dentro do fluxo de coleta e disponibilização de preços de veículos.

---

## Objetivo

Definir claramente as permissões, limites de atuação e interações entre os papéis do sistema, garantindo organização operacional e rastreabilidade das ações realizadas.

---

## Matriz de Responsabilidades

| Papel | Gestão de Usuários | Gestão de Catálogo | Cadastro de Loja | Aprovação de Loja | Planejamento Semanal | Registro de Preços | Consulta Pública |
|--------|------------------|--------------------|-----------------|-----------------|---------------------|------------------|----------------|
| Admin | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Gerente | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Coordenador | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Lojista | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Pesquisador | ❌ | ❌ | ✅* | ❌ | ❌ | ✅ | ❌ |
| Usuário Público | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

\* Pesquisador pode sugerir lojas, sujeitas à aprovação do coordenador.

---

## Administrador

Responsável pelo controle de acesso ao sistema.

### Responsabilidades
- Criar usuários
- Definir papéis dos usuários
- Ativar ou desativar contas

### Restrições
- Não realiza coleta de preços
- Não altera catálogo de veículos
- Não aprova lojas

---

## Gerente

Responsável pela manutenção do catálogo global de veículos.

### Responsabilidades
- Cadastrar marcas
- Cadastrar modelos
- Definir variantes e características dos veículos

### Restrições
- Não gerencia usuários
- Não aprova lojas
- Não define planejamento semanal
- Não registra preços

---

## Coordenador Regional

Responsável pela supervisão operacional da coleta de dados em sua região.

### Responsabilidades
- Avaliar documentação de lojas
- Aprovar ou rejeitar lojas cadastradas
- Definir planejamento semanal de pesquisa
- Distribuir tarefas para pesquisadores

### Restrições
- Não altera catálogo de veículos
- Não registra preços
- Não gerencia usuários

---

## Lojista

Responsável por cadastrar lojas no sistema.

### Responsabilidades
- Submeter cadastro de loja
- Enviar documentação para validação
- Acompanhar status da aprovação

### Restrições
- Não aprova lojas
- Não registra preços
- Não altera catálogo

---

## Pesquisador

Responsável pela coleta de preços nas lojas designadas.

### Responsabilidades
- Registrar preços observados
- Cumprir planejamento semanal definido pelo coordenador
- Sugerir novas lojas para cadastro

### Restrições
- Não aprova lojas
- Não altera catálogo
- Não gerencia usuários

---

## Usuário Público

Responsável pela consulta das informações disponibilizadas pelo sistema.

### Responsabilidades
- Consultar valores médios de veículos

### Restrições
- Não necessita autenticação
- Não altera dados do sistema

---

## Controle de Acesso

O sistema adotará modelo baseado em papéis (RBAC), onde cada usuário possui permissões associadas ao seu perfil operacional.

<pre class="mermaid">
flowchart LR

  subgraph Roles["Papeis"]
    A["Admin"]
    G["Gerente"]
    C["Coordenador"]
    L["Lojista"]
    P["Pesquisador"]
    U["Usuario Publico"]
  end

  subgraph Perms["Permissoes"]
    P1["Gerenciar usuarios"]
    P2["Gerenciar catalogo"]
    P3["Cadastrar loja"]
    P4["Aprovar loja"]
    P5["Planejamento semanal"]
    P6["Registrar preco"]
    P7["Consultar cotacao"]
  end

  A --> P1
  G --> P2
  L --> P3
  P --> P3
  C --> P4
  C --> P5
  P --> P6
  U --> P7
</pre>


---

## Interação Entre Papéis

O funcionamento do sistema depende da colaboração entre os papéis:

- Lojistas e pesquisadores fornecem dados iniciais
- Coordenadores validam e organizam a operação
- Gerentes mantêm a estrutura do catálogo
- Administradores controlam o acesso ao sistema
- Usuários públicos consomem os dados disponibilizados

---

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

