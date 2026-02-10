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

---

## Interação Entre Papéis

O funcionamento do sistema depende da colaboração entre os papéis:

- Lojistas e pesquisadores fornecem dados iniciais
- Coordenadores validam e organizam a operação
- Gerentes mantêm a estrutura do catálogo
- Administradores controlam o acesso ao sistema
- Usuários públicos consomem os dados disponibilizados
