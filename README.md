# Exemplo de Sistema em Python fazendo CRUD no mongoDB

Sistema desenvolvido em Python para gerenciar uma locadora de veículos utilizando um banco de dados Oracle.

## Funcionalidades

- Cadastro, consulta e alteração de clientes e carros;
- Desativação de clientes e carros, preservando seus registros no banco;
- Cadastro, consulta, alteração e finalização de locações;
- Exclusão permanente de clientes, carros e locações;
- Registro da devolução dos veículos;
- Relatórios relacionados às operações da locadora.

### Desativação e exclusão de registros

No menu principal, a opção **4** mantém a desativação de clientes e carros e a
finalização de locações. Desativar um cliente ou carro altera seu status para
inativo, sem remover o registro do banco de dados.

A opção **5** permite excluir permanentemente um cliente, um carro ou uma
locação. O sistema lista os registros com suas chaves e campos descritivos,
permite selecionar um deles por número e solicita confirmação antes de excluir.
Para clientes ou carros que possuem locações vinculadas, o sistema pergunta se
as locações também devem ser excluídas. Se a resposta for negativa, o registro
principal não é removido; se for positiva, as locações relacionadas e o registro
selecionado são excluídos na mesma transação.

## Tecnologias

- Python;
- MongoDB;
- PyMongo (biblioteca para conexão e execução de comandos MongoDB).
- 
## Organização do projeto

- `src/model`: classes que representam as entidades do sistema;
- `src/controller`: classes responsáveis pelas operações CRUD nas coleções MongoDB;
- `src/conexion`: conexão com o banco de dados MongoDB;
- `src/reports`: relatórios do sistema utilizando Aggregation e Lookup;
- `src/utils`: configurações dos menus e Splash Screen;
- `src/sql`: consultas e comandos MongoDB utilizados nos relatórios, caso exista esse diretório;
- `src/principal.py`: interface principal entre o usuário e o sistema;
- `src/create_collections.py`: script responsável pela criação das coleções e inserção de documentos iniciais.
  
## Andamento do projeto

### Feito

### Em andamento
- [ ] Estruturação inicial
### Pendente
- [ ] Models (classes das entidades);
- [ ] Controllers (operações CRUD no MongoDB);
- [ ] Criação das coleções;
- [ ] Diagrama relacional;
- [ ] Reports (relatórios com Aggregation e Lookup);
- [ ] Utils (menus e Splash Screen);
- [ ] Principal (menu e fluxo de execução);
- [ ] Script Python para criação das coleções;
- [ ] Inserção de documentos;
- [ ] Remoção de documentos;
- [ ] Atualização de documentos;
- [ ] README.md (documentação de execução no Linux);
- [ ] Vídeo demonstrativo;
- [ ] Testes.


### Configuração do ambiente de desenvolvimento sem SUDO


### 1. Instalação do `uv` sem sudo

O ambiente Linux utiliza Python 3.12, incompatível com algumas das versões antigas de bibliotecas exigidas pelo projeto. Para evitar alterações na instalação global do Python e não depender de permissões administrativas, foi utilizado o **uv**, gerenciador de versões e ambientes Python.

Instale o `uv` no diretório do usuário:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Caso o comando `uv` não seja encontrado após a instalação, adicione o diretório de instalação ao `PATH`. No ambiente utilizado, foi necessário executar:

```bash
export PATH="$HOME/snap/code/205/.local/bin:$PATH"
```

Esse caminho pode variar conforme o ambiente. Para conferir a instalação:

```bash
uv --version
```

### 2. Criação do ambiente Python 3.10

Na pasta `src` do projeto, instale o Python 3.10 e crie o ambiente virtual:

```bash
uv python install 3.10
uv venv .venv310 --python 3.10
source .venv310/bin/activate
```

Com o ambiente ativado, instale as dependências:

```bash
uv pip install cx-Oracle==8.3.0 pandas==1.4.4 numpy==1.23.2
```

O ambiente virtual mantém as bibliotecas isoladas do Python global do sistema.

### 3. Ajustes na conexão com o banco


### 4. Configuração do banco de dados


### 5. Execução e validação


