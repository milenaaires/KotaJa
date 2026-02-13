# **Protótipo de UI/UX e Workflow de Negócio (MVP)**

> Um ecossistema completo para coleta, auditoria e consulta de preços de veículos em tempo real.

O **KotaJá** foi desenvolvido para resolver a fragmentação de dados no mercado automotivo brasileiro. Ele conecta desde o pesquisador de campo que visita a loja física até o consumidor final, garantindo que a média de preço exibida seja baseada em observações reais e auditadas.

---

## Arquitetura do Protótipo

O protótipo foi construído utilizando uma arquitetura **SPA (Single Page Application)** com:
- **Core:** HTML5, CSS3 moderno (Flexbox/Grid) e Vanilla JavaScript.
- **Tema:** Dark Mode com acentos em Laranja (#ff8a00), focado em legibilidade e modernidade.
- **RBAC (Role-Based Access Control):** Simulação de múltiplos papéis de usuário no mesmo ambiente.

---

## Papéis e Funcionalidades

### 1. Consulta Pública (Acesso Livre)
A porta de entrada para o usuário comum. Permite consultar a média de preço de um veículo sem necessidade de login.
- **Filtros Inteligentes:** Seleção por Região, Marca, Modelo e Variante.
- **Auditoria Transparente:** Exibe logs das últimas consultas realizadas, garantindo que o sistema está operando com dados recentes.

### 2. Administrador (Admin)
Visão macro do sistema e controle de acesso.
- **Gestão de Usuários:** Cadastro, edição e controle de status de todos os membros (RBAC).
- **KPIs do Sistema:** Monitoramento de usuários ativos, lojas cadastradas e saúde do servidor de dados.
- **Monitoramento de Logs:** Visão técnica das operações do sistema.

### 3. Gerente (Manager)
Responsável pela padronização dos dados globais.
- **Catálogo de Veículos:** Gestão das Marcas e Modelos que os pesquisadores podem selecionar.
- **Variantes:** Cadastro técnico de versões (motorização, câmbio, ano), garantindo que os dados coletados sejam homogêneos.
- **Relatórios Gerenciais:** Acesso às médias consolidadas após o processamento.

### 4. Coordenador Regional (Coordinator)
O elo entre o escritório e o campo. Atua por região geográfica (ex: SP, RJ).
- **Workflow de Aprovação:** Analisa submissões de novas lojas feitas por lojistas ou pesquisadores.
- **Planejamento Semanal (Assignments):** Atribui quais pesquisadores devem visitar quais lojas em um determinado período.
- **Acompanhamento de Status:** Monitora em tempo real quais tarefas de coleta foram concluídas.

### 5. Pesquisador (Researcher)
Usuário de campo (mobile-first).
- **Roteiro de Visitas:** Visualiza a lista de lojas atribuídas pelo Coordenador para a semana.
- **Coleta de Preços:** Formulário para inserção de preços, quilometragem e opcionais diretamente da loja física.
- **Sincronização:** Envia os dados para a base global instantaneamente após a visita.

### 6. Lojista (Shopkeeper)
Parceiro estratégico do sistema.
- **Cadastro de Loja:** Submete dados da loja e documentação (CNPJ) para aprovação.
- **Status de Parceiro:** Acompanha se sua loja está ativa no radar de pesquisas do KotaJá.

---

## Processamento Inteligente (Batch Mensal)

O sistema conta com um motor de **Batch Processing** simulado:
1. **Coleta:** Acumula milhares de observações de pesquisadores durante o mês.
2. **Consolidação:** O Batch limpa dados espúrios e calcula a média ponderada por região e variante.
3. **Publicação:** As novas médias são liberadas para a Consulta Pública, mantendo o mercado atualizado.

---

## Execução Rápida

Para testar o protótipo agora mesmo:

<a href="https://milenaaires.github.io/KotaJa/downloads/Prototipo_KotaJa.html">Aperte aqui</a>

---

*Este projeto é um protótipo funcional para validação de requisitos e interface.*


