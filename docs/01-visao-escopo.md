<p align="center">
  <img src="/assets/logo/logopreta.png" width="300">
</p>

Sistema de captura, organização e consulta pública de preços de veículos coletados em lojas físicas, com gerenciamento operacional por regiões e planejamento semanal de pesquisas.

---

## 1. Visão Geral

O **KotaJá** é um sistema projetado para registrar valores reais praticados por lojas na venda de veículos e disponibilizar essas informações através de consultas públicas.

O sistema organiza o processo de coleta de dados por meio de papéis operacionais e fluxos definidos, garantindo qualidade, rastreabilidade e consistência das informações armazenadas.

---

## 2. Objetivo do Sistema

O objetivo principal do KotaJá é:

- Permitir a coleta estruturada de preços de veículos
- Organizar a coleta por regiões geográficas e períodos semanais
- Disponibilizar consulta pública de cotação sem necessidade de autenticação
- Armazenar dados das consultas para análises futuras
- Calcular médias mensais através de processamento batch

---

## 3. apéis do Sistema

O sistema possui diferentes papéis operacionais responsáveis pela manutenção e qualidade das informações.

**Administrador**: Responsável pela criação e gerenciamento dos usuários do sistema.

**Gerente**: Responsável pela gestão do catálogo global de veículos, incluindo:
- Marcas
- Modelos
- Variantes e características globais

**Coordenador Regional**: Responsável por supervisionar a operação de coleta em sua região. Atividades principais:
- Aprovar lojas cadastradas
- Definir semanalmente quais lojas serão pesquisadas
- Distribuir tarefas para pesquisadores

**Lojista**: Responsável por cadastrar lojas e enviar documentação para validação.

**Pesquisador**: Responsável por registrar preços coletados nas lojas designadas. Também pode sugerir novas lojas para aprovação.

**Usuário Público**: Pode consultar valores médios de veículos sem necessidade de login.

---

## 4. Funcionamento Geral do Sistema

O fluxo principal do sistema ocorre da seguinte forma:

1. O gerente cadastra o catálogo de veículos
2. Lojas são cadastradas e avaliadas pelo coordenador regional
3. O coordenador define semanalmente as lojas que serão pesquisadas
4. Pesquisadores registram os preços observados
5. O sistema processa os dados coletados e calcula médias mensais
6. Usuários públicos realizam consultas de cotação

<div class="mermaid">
flowchart LR
  Publico["Usuario Publico"] -->|"Consulta cotacao"| KotaJa["KotaJa"]

  Admin["Admin"] -->|"Gerencia usuarios"| KotaJa
  Gerente["Gerente"] -->|"Mantem catalogo"| KotaJa
  Coord["Coordenador Regional"] -->|"Aprova lojas e planeja semana"| KotaJa
  Lojista["Lojista"] -->|"Submete loja e documentos"| KotaJa
  Pesq["Pesquisador"] -->|"Registra coletas e sugere lojas"| KotaJa

  KotaJa -->|"Escreve dados"| DB[("Banco de Dados")]
  DB -->|"Le dados"| KotaJa

  KotaJa --> Batch["Batch mensal (medias)"]
  Batch -->|"Atualiza medias mensais"| DB
  KotaJa -->|"Registra log de consulta"| DB
</div>

---

## 5. Escopo do Projeto

### Incluído no Projeto

- Documentação funcional completa
- Protótipos de interface
- Modelagem de banco de dados
- Projeto técnico do sistema
- Implementação da consulta pública
- Registro de consultas realizadas
- Definição e implementação de testes automatizados

---

## 6. Premissas Técnicas

O projeto será desenvolvido utilizando:

- Banco de dados online Neon
- Interface pública desenvolvida com Streamlit
- Controle de versão com GitHub
- Documentação publicada via GitHub Pages
- Protótipos desenvolvidos em HTML

---
