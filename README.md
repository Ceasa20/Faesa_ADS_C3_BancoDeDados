# Sistema de Gerenciamento de Locadora de Veículos — Python & MongoDB

Aplicação de linha de comando (CLI) desenvolvida em Python para o gerenciamento operacional de uma locadora de veículos, utilizando o **MongoDB** como banco de dados orientado a documentos por meio do driver oficial **PyMongo**. 

O projeto aplica arquitetura modular baseada em Orientação a Objetos (MVC adaptado) e implementa regras de integridade referencial na camada de aplicação, garantindo consistência entre as coleções relacionadas (`clientes`, `carros` e `locacoes`).

---

## Funcionalidades Principais

* **Gestão de Entidades (CRUD Completo):** Cadastro, consulta, atualização e remoção de **Clientes**, **Carros** e **Locações**, com validação de chaves primárias (evitando duplicidade) e tipagem de entrada.
* **Controle de Ciclo de Vida (Inativação Lógica vs. Exclusão Física):**
  * **Opção 4 — Desativação / Finalização:** Permite inativar clientes e carros (alterando o status para inativo sem perda de histórico, bloqueando novas locações para esses registros) e registrar a devolução/finalização de locações em andamento.
  * **Opção 5 — Exclusão Permanente com Integridade Referencial:** Lista os documentos com chave identificadora e campos descritivos, exige confirmação explícita e verifica dependências antes da remoção. Caso um cliente ou carro possua locações vinculadas, o sistema alerta o usuário e oferece a exclusão em cascata dos documentos dependentes; caso contrário, a operação é abortada para preservar a consistência referencial.
* **Relatórios Analíticos (Aggregation Framework):**
  * **Sumarização (`$group`):** Agrupamento de registros e cálculo de métricas consolidadas (ex.: total de locações e faturamento agrupados por veículo ou cliente).
  * **Junção entre Coleções (`$lookup`):** Cruzamento de dados entre `locacoes`, `clientes` e `carros` para exibição de relatórios relacionais completos.
* **Splash Screen Dinâmica:** Consulta em tempo real a contagem de documentos existentes em cada coleção no momento da inicialização.

---

## Stack Tecnológica

* **Linguagem:** Python 3.10+
* **Banco de Dados:** MongoDB (NoSQL Orientado a Documentos)
* **Driver Nativo:** PyMongo (`pymongo`)
* **Gerenciador de Ambiente:** `uv` (Astral)
* **Modelagem:** SQL Power Architect (Diagrama Relacional base)

---

## Arquitetura e Organização do Projeto

```text
├── diagrams/                  # Diagrama relacional da base de dados (PDF/PNG)
├── src/
│   ├── conexion/              # Módulo de conexão com o servidor MongoDB e credenciais
│   ├── model/                 # Classes de domínio (Cliente, Carro, Locacao) com getters/setters e to_string()
│   ├── controller/            # Regras de negócio, validações de integridade e operações CRUD no MongoDB
│   ├── reports/               # Consultas analíticas utilizando Aggregation Pipelines ($group e$lookup)
│   ├── utils/                 # Configurações de menus, constantes e geração da Splash Screen
│   ├── create_collections.py  # Script de inicialização das coleções e carga/migração de documentos
│   └── principal.py           # Ponto de entrada da aplicação e controle de fluxo dos menus
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação técnica e guia de execução
