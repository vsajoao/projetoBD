# Sistema de Gerenciamento Escolar - Projeto Banco de Dados 2025.2

## Sobre o Projeto
Este projeto consiste em um Sistema de Gerenciamento Escolar desenvolvido para a disciplina de Banco de Dados da Universidade de Brasília (UnB). O sistema permite a administração completa de uma instituição de ensino, segregando as funções entre Secretaria e Corpo Docente, utilizando um banco de dados relacional e uma interface gráfica para o usuário final.


## Tecnologias Utilizadas
* Linguagem: Python 3.10+
* Interface Gráfica: Streamlit
* Banco de Dados: MySQL 8.0 (via Docker)
* Bibliotecas Principais: mysql-connector-python, pandas, sqlalchemy

## Funcionalidades e Módulos do Sistema

### 1. Módulo Secretaria
Responsável pela gestão administrativa e estrutural da escola.
* Gerenciar Salas: Cadastro de salas físicas e controle de capacidade (CRUD).
* Gerenciar Disciplinas: Cadastro de matérias e departamentos (CRUD).
* Gerenciar Turmas: Abertura de turmas vinculando Disciplina, Professor e Sala (CRUD).
* Gerenciar Alunos: Cadastro completo com upload de foto de perfil (BLOB).
* Nova Matrícula: Associação de alunos a turmas com validação de regras de negócio (Triggers de lotação e status).

### 2. Módulo Área do Professor
Responsável pela gestão acadêmica diária.
* Frequência (Chamada): Registro de presença ou ausência por data.
* Avaliações: Agendamento de provas e trabalhos por turma.
* Lançar Notas: Registro de notas com validação automática de valores.

### 3. Módulo Relatórios & Fechamento
Responsável pela visualização de dados consolidados e processamento final.
* Boletim (View): Relatório que exibe dados do aluno, calcula médias, contabiliza frequência e detalha notas.
* Fechar Semestre (Procedure): Automação que calcula a situação final do aluno (Aprovado, Reprovado por Nota ou Reprovado por Falta).

## Recursos Avançados de Banco de Dados Implementados
1. Views: Visualização complexa para geração de boletins dinâmicos.
2. Stored Procedures: Lógica procedural para encerramento de semestre e atualização de status.
3. Triggers: Validação de Notas (0 a 10).

## Estrutura de Arquivos

projetoBD/
├── app/
│   ├── app.py               # Arquivo principal (Navegação e Rotas)
│   ├── database.py          # Gerenciamento de conexão (SQLAlchemy)
│   └── telas/               # Módulos da interface gráfica
│       ├── alunos.py
│       ├── avaliacoes.py
│       ├── boletim.py
│       ├── dashboard.py
│       ├── disciplinas.py
│       ├── fechamento.py
│       ├── frequencia.py
│       ├── matriculas.py
│       ├── notas.py
│       ├── salas.py
│       └── turmas.py
├── sql/
│   ├── schemas.sql          # Script DDL (Tabelas)
│   ├── data.sql             # Script DML (Dados iniciais)
│   ├── view.sql             # Script de Criação de Views
│   ├── procedure.sql        # Script de Stored Procedures
│   └── trigger.sql          # Script de Triggers
├── modelo_relacional.png    # Imagem do DER/Modelo Relacional
├── requirements.txt         # Dependências do Python
└── README.md                # Documentação

## Como Executar o Projeto

### Pré-requisitos
* Docker Desktop.
* Python 3.

### Passo 1: Inicializar o Banco de Dados
Execute o comando para subir o container do MySQL:

docker run --name escola-db -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0

### Passo 2: Configurar Schema e Dados
Utilize um cliente SQL para conectar ao banco (localhost:3306, user: root, pass: root) e execute os scripts da pasta /sql nesta ordem:
1. schemas.sql
2. data.sql
3. view.sql
4. procedure.sql
5. trigger.sql

### Passo 3: Instalar Dependências
Na raiz do projeto, execute:

pip install -r requirements.txt

### Passo 4: Executar a Aplicação
Inicie o servidor do Streamlit:

python -m streamlit run app/app.py