# Casos de Uso (Use Cases)

Este documento reúne os principais casos de uso do sistema KotaJá — fluxos de alto nível que descrevem como os atores interagem com o sistema para cumprir objetivos concretos.

Formato: cada caso traz Ator, Pré-condição, Fluxo Principal, Fluxos Alternativos e Pós-condição.

---

## CU-01 — Gerenciar Usuários (Administrador)
- Ator: Administrador
- Pré-condição: Administrador autenticado
- Fluxo principal:
  1. Administrador acessa área de gestão de usuários
  2. Seleciona "Criar usuário"
  3. Preenche e-mail e papel (role)
  4. Salva; sistema registra e envia convite por e‑mail
- Fluxos alternativos: edição, desativação e reativação de usuário
- Pós-condição: usuário criado/atualizado com papel e status definidos

---

## CU-02 — Manter Catálogo de Veículos (Gerente)
- Ator: Gerente
- Pré-condição: Gerente autenticado
- Fluxo principal:
  1. Gerente acessa módulo de catálogo
  2. Adiciona marca, cria modelo vinculado e define variantes
  3. Salva alterações; catálogo é versionado
- Pós-condição: catálogo atualizado e disponível para pesquisas

---

## CU-03 — Submeter e Aprovar Cadastro de Loja (Lojista → Coordenador)
- Atores: Lojista, Coordenador Regional
- Pré-condição: Lojista preenche formulário de cadastro
- Fluxo principal:
  1. Lojista submete cadastro com documentação
  2. Coordenador visualiza submissão e valida documentos
  3. Coordenador aprova ou rejeita; em caso de rejeição registra motivo
- Pós-condição: loja aprovada e disponível para ser selecionada em observações

---

## CU-04 — Planejar Coletas Semanais (Coordenador → Pesquisador)
- Ator: Coordenador Regional
- Pré-condição: Coordenador autenticado e lista de lojas válidas
- Fluxo principal:
  1. Coordenador cria plano semanal e atribui lojas a pesquisadores
  2. Pesquisadores recebem tarefas e confirmação
- Pós-condição: plano publicado e tarefas atribuídas

---

## CU-05 — Registrar Observação de Preço (Pesquisador)
- Ator: Pesquisador
- Pré-condição: Pesquisador autenticado com tarefa atribuída
- Fluxo principal:
  1. Seleciona loja e variante do veículo
  2. Informa preço e data da observação
  3. Salva; sistema valida consistência mínima e registra origem
- Pós-condição: observação persistida e disponível para agregação

---

## CU-06 — Solicitar Cadastro de Loja (Lojista)
- Ator: Lojista
- Fluxo principal: preencher e submeter formulário de cadastro
- Pós-condição: submissão pendente de aprovação do Coordenador

---

## CU-07 — Consulta Pública de Preços (Usuário Público)
- Ator: Usuário Público (não autenticado)
- Fluxo principal:
  1. Usuário acessa a tela de consulta
  2. Filtra por região e veículo
  3. Visualiza preço médio e histórico
- Pós-condição: consulta logada para auditoria (sem necessidade de login)

---

## CU-08 — Cálculo Automático de Médias (Sistema)
- Ator: Sistema (processo agendado)
- Fluxo principal:
  1. Rotina periódica agrega observações por período/variante/região
  2. Calcula médias e atualiza versão consolidada dos indicadores
- Pós-condição: médias mensais e relatórios atualizados

---

## Notas
- Cada caso de uso deve orientar a formulação de critérios de aceitação e testes automatizados.
- Casos menores e exceções ficam descritos nos requisitos e nos critérios de aceitação das User Stories.
