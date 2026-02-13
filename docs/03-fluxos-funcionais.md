# Fluxos Funcionais do Sistema

Este documento descreve os principais fluxos operacionais do sistema KotaJá, apresentando como os dados são criados, validados, processados e disponibilizados ao longo do tempo.

Os fluxos são apresentados de forma conceitual, sem detalhamento técnico de implementação.

---

## 1. Objetivo

Documentar o funcionamento do sistema sob a perspectiva do negócio, garantindo clareza sobre responsabilidades, dependências e sequenciamento das atividades.

---

## 2. Fluxo 1 — Cadastro e Aprovação de Lojas

### 2.1 Descrição
O cadastro de lojas pode ser iniciado por lojistas ou pesquisadores. Todas as lojas precisam ser avaliadas e aprovadas por um coordenador regional antes de entrarem em operação.

### 2.2 Passos
1. Lojista ou pesquisador submete o cadastro de uma loja
2. Documentos e informações da loja são enviados
3. A loja entra com status **PENDENTE**
4. O coordenador regional analisa a submissão
5. O coordenador aprova ou rejeita a loja
6. O status da loja é atualizado para **APROVADA** ou **REJEITADA**

<pre class="mermaid">
flowchart TD
  Start([Inicio]) --> Sub["Submeter loja + documentos"]
  Sub --> Pend["Status: PENDENTE"]
  Pend --> Aval["Coordenador avalia submissao"]

  Aval -->|Aprova| Criar["Cria/atualiza registro oficial da loja"]
  Criar --> Aprov["Status final: APROVADA"]

  Aval -->|Rejeita| Rej["Status final: REJEITADA (com motivo)"]

  Aprov --> End([Fim])
  Rej --> End
</pre>


### 2.3 Regras
- Apenas lojas aprovadas podem receber coletas de preços
- Toda decisão deve registrar responsável e data

---

## 3. Fluxo 2 — Planejamento Semanal de Pesquisa

### 3.1 Descrição
O coordenador regional define semanalmente quais lojas devem ser pesquisadas por cada pesquisador em sua região.

### 3.2 Passos
1. Coordenador seleciona o período da semana
2. Coordenador escolhe as lojas aprovadas da região
3. Coordenador atribui as lojas a pesquisadores
4. O planejamento semanal é registrado no sistema
5. Pesquisadores visualizam suas atribuições

### 3.3 Regras
- Uma loja só pode ser atribuída se estiver aprovada
- Planejamentos são organizados por região e período

---

## 4. Fluxo 3 — Coleta de Preços

### 4.1 Descrição
Pesquisadores registram os preços observados nas lojas atribuídas durante o planejamento semanal.

### 4.2 Passos
1. Pesquisador acessa sua lista de lojas da semana
2. Pesquisador seleciona o veículo pesquisado
3. Pesquisador informa o valor observado
4. O sistema registra a observação com data, loja e pesquisador

### 4.3 Regras
- Cada observação deve estar associada a uma loja e um veículo
- Observações devem registrar autor e data
- O sistema pode aplicar validações para evitar duplicidades simples

---

## 5. Fluxo 4 — Processamento Mensal (Batch)

### 5.1 Descrição
O sistema executa periodicamente um processamento batch para consolidar os dados coletados.

### 5.2 Passos
1. O sistema identifica observações do período mensal
2. Os valores são agregados por veículo
3. O sistema calcula a média mensal
4. Os resultados consolidados são armazenados

### 5.3 Regras
- O processamento deve ser idempotente
- Resultados devem ser versionados por período
- O batch não altera dados originais de coleta

---

## 6. Fluxo 5 — Consulta Pública de Cotação

### 6.1 Descrição
Usuários públicos podem consultar valores médios de veículos sem necessidade de autenticação.

### 6.2 Passos
1. Usuário seleciona filtros (ex.: marca, modelo, variante)
2. O sistema consulta os dados consolidados
3. O valor médio mensal é exibido ao usuário
4. A consulta realizada é registrada pelo sistema

### 6.3 Regras
- A consulta não exige login
- Todas as consultas devem ser registradas
- Caso não existam dados, o sistema deve informar claramente

<pre class="mermaid">
flowchart TD
  Start([Inicio]) --> Filtros["Usuario seleciona filtros (marca/modelo/variante/regiao)"]
  Filtros --> Busca["Sistema consulta medias mensais (variante + regiao)"]

  Busca -->|Encontrou| Exibe["Exibe valor medio mensal"]
  Busca -->|Nao encontrou| Sem["Exibe: Sem resultados para os filtros"]

  Exibe --> Log["Registra log da consulta (filtros + timestamp)"]
  Sem --> Log

  Log --> End([Fim])
</pre>

---

## 7. Relação entre os Fluxos

Os fluxos descritos estão interligados:

- O cadastro de lojas habilita o planejamento semanal
- O planejamento semanal viabiliza a coleta de preços
- A coleta alimenta o processamento mensal
- O processamento mensal sustenta a consulta pública

Essas relações garantem consistência e rastreabilidade das informações do sistema.
