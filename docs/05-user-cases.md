# Casos de Uso (Use Cases)

Este documento descreve os principais casos de uso do sistema KotaJá.

---

# UC-01 — Consulta Pública de Preço Médio

## Atores
Usuário Público

## Pré-condições
- Base de médias mensais deve estar disponível

## Fluxo Principal
1. Usuário acessa tela de consulta
2. Seleciona região
3. Seleciona veículo
4. Sistema retorna média mensal

## Fluxo Alternativo
- Caso não existam dados, sistema informa indisponibilidade.

## Pós-condições
- Consulta registrada no log

---

# UC-02 — Registrar Log de Consulta

## Atores
Sistema

## Fluxo
1. Sistema registra filtros utilizados
2. Sistema armazena timestamp da consulta
3. Sistema registra identificador de sessão

---

# UC-03 — Gerenciar Catálogo

## Atores
Gerente

## Fluxo
1. Gerente cadastra marca
2. Gerente cadastra modelo
3. Gerente cadastra variante

---

# UC-04 — Aprovar Cadastro de Loja

## Atores
Coordenador

## Fluxo
1. Coordenador visualiza submissão
2. Analisa documentos
3. Aprova ou rejeita loja

---

# UC-05 — Criar Plano Semanal

## Atores
Coordenador

## Fluxo
1. Coordenador cria plano
2. Define pesquisadores
3. Associa lojas ao plano

---

# UC-06 — Registrar Preço Observado

## Atores
Pesquisador

## Fluxo
1. Pesquisador seleciona loja
2. Seleciona veículo
3. Registra preço
4. Sistema salva observação

---

# UC-07 — Executar Batch Mensal

## Atores
Sistema

## Fluxo
1. Sistema executa rotina mensal
2. Calcula médias
3. Armazena resultados consolidados

