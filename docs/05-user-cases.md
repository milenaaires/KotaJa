# Casos de Uso (Use Cases)

Este documento descreve os principais casos de uso do sistema KotaJá.

---

# 1. UC-01 — Consulta Pública de Preço Médio

## 1.1 Atores
Usuário Público

## 1.2 Pré-condições
- Base de médias mensais deve estar disponível

## 1.3 Fluxo Principal
1. Usuário acessa tela de consulta
2. Seleciona região
3. Seleciona veículo
4. Sistema retorna média mensal

## 1.4 Fluxo Alternativo
- Caso não existam dados, sistema informa indisponibilidade.

## 1.5 Pós-condições
- Consulta registrada no log

---

# 2. UC-02 — Registrar Log de Consulta

## 2.1 Atores
Sistema

## 2.2 Fluxo
1. Sistema registra filtros utilizados
2. Sistema armazena timestamp da consulta
3. Sistema registra identificador de sessão

---

# 3. UC-03 — Gerenciar Catálogo

## 3.1 Atores
Gerente

## 3.2 Fluxo
1. Gerente cadastra marca
2. Gerente cadastra modelo
3. Gerente cadastra variante

---

# 4. UC-04 — Aprovar Cadastro de Loja

## 4.1 Atores
Coordenador

## 4.2 Fluxo
1. Coordenador visualiza submissão
2. Analisa documentos
3. Aprova ou rejeita loja

---

# 5. UC-05 — Criar Plano Semanal

## 5.1 Atores
Coordenador

## 5.2 Fluxo
1. Coordenador cria plano
2. Define pesquisadores
3. Associa lojas ao plano

---

# 6. UC-06 — Registrar Preço Observado

## 6.1 Atores
Pesquisador

## 6.2 Fluxo
1. Pesquisador seleciona loja
2. Seleciona veículo
3. Registra preço
4. Sistema salva observação

---

# 7. UC-07 — Executar Batch Mensal

## 7.1 Atores
Sistema

## 7.2 Fluxo
1. Sistema executa rotina mensal
2. Calcula médias
3. Armazena resultados consolidados

