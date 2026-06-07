# LLM Unit Test Generation

Repositório do projeto **“Um Estudo Empírico Comparativo sobre a Geração de Testes Unitários por Modelos de Linguagem de Grande Escala”**, desenvolvido para a disciplina de **Fundamentos de Teste de Software**.

## 1. Sobre o projeto

Este projeto tem como objetivo comparar a qualidade dos testes unitários gerados por diferentes Modelos de Linguagem de Grande Escala, como **ChatGPT**, **Gemini** e **Claude**, a partir de uma mesma aplicação simples desenvolvida em Python.

A aplicação foi construída com escopo controlado e contém funções de lógica de negócio relacionadas a um domínio de processamento de pedidos. O objetivo principal não é avaliar a aplicação em si, mas utilizá-la como objeto de estudo para investigar como diferentes LLMs geram testes unitários quando recebem o mesmo código-alvo e instruções equivalentes.

## 2. Objetivo do experimento

Avaliar comparativamente os testes unitários gerados por diferentes LLMs, considerando critérios como:

- Quantidade de testes gerados;
- Testes executáveis sem correção;
- Testes aprovados;
- Cobertura de linhas;
- Qualidade dos asserts;
- Presença de casos de borda;
- Ocorrência de alucinações;
- Esforço de correção humana.

## 3. Modelos avaliados

O experimento considera três modelos/ferramentas de IA generativa:

- ChatGPT;
- Gemini;
- Claude.

Cada integrante do grupo fica responsável por gerar testes unitários utilizando um dos modelos, garantindo que todos utilizem o mesmo código-alvo e o mesmo prompt-base.

## 4. Aplicação utilizada no experimento

A aplicação foi desenvolvida em Python e contém funções de lógica de negócio relacionadas a pedidos, pagamentos e clientes.

As funcionalidades preliminares utilizadas no experimento são:

- Validação de pedido;
- Validação de pagamento;
- Cálculo de taxa de pagamento;
- Classificação de risco do cliente;
- Validação se um cliente pode realizar um novo pedido.

Essas funcionalidades foram escolhidas por possuírem regras condicionais, entradas inválidas, valores-limite, exceções e diferentes caminhos de execução, permitindo avaliar a capacidade dos LLMs de gerar testes unitários relevantes.

## 5. Estrutura do repositório

```text
llm-unit-test-generation/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── orders.py
│   ├── payments.py
│   └── customer_risk.py
├── prompts/
│   └── prompt_base.txt
├── tests_generated/
│   ├── chatgpt/
│   ├── gemini/
│   └── claude/
├── results/
│   ├── coverage_reports/
│   ├── execution_logs/
│   └── metrics.csv
└── docs/
    └── entrega_3_resultados_preliminares.md