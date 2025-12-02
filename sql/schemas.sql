-- Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS escola_db;
USE escola_db;

-- 1. Tabela Departamentos (Agrupa professores e cursos)
CREATE TABLE IF NOT EXISTS departamento (
    id_depto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(10) NOT NULL
);

-- 2. Tabela Professores
CREATE TABLE IF NOT EXISTS professor (
    id_prof INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    titulacao VARCHAR(50),
    id_depto INT,
    FOREIGN KEY (id_depto) REFERENCES departamento(id_depto)
);

-- 3. Tabela Alunos (Com campo para FOTO/Binário)
CREATE TABLE IF NOT EXISTS aluno (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_nascimento DATE,
    foto LONGBLOB, -- Requisito: Dado binário
    matricula_ativa BOOLEAN DEFAULT TRUE
);

-- 4. Tabela Disciplinas
CREATE TABLE IF NOT EXISTS disciplina (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    carga_horaria INT NOT NULL,
    ementa TEXT,
    id_depto INT,
    FOREIGN KEY (id_depto) REFERENCES departamento(id_depto)
);

-- 5. Tabela Salas
CREATE TABLE IF NOT EXISTS sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    numero_sala VARCHAR(20) NOT NULL,
    capacidade INT NOT NULL,
    tipo VARCHAR(50) -- Ex: Laboratório, Sala de Aula
);

-- 6. Tabela Turmas (Onde tudo acontece: Prof + Disciplina + Sala)
CREATE TABLE IF NOT EXISTS turma (
    id_turma INT AUTO_INCREMENT PRIMARY KEY,
    ano INT NOT NULL,
    semestre INT NOT NULL, -- 1 ou 2
    id_disciplina INT,
    id_prof INT,
    id_sala INT,
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina),
    FOREIGN KEY (id_prof) REFERENCES professor(id_prof),
    FOREIGN KEY (id_sala) REFERENCES sala(id_sala)
);

-- 7. Tabela Matrículas (Aluno na Turma)
CREATE TABLE IF NOT EXISTS matricula (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT,
    id_turma INT,
    data_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'CURSANDO', -- APROVADO, REPROVADO
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

-- 8. Tabela Avaliações (Definição da prova)
CREATE TABLE IF NOT EXISTS avaliacao (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL, -- Ex: Prova 1, Trabalho Final
    peso DECIMAL(4,2) NOT NULL,
    data_prevista DATE,
    id_turma INT,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

-- 9. Tabela Notas (Nota do aluno na avaliação)
CREATE TABLE IF NOT EXISTS nota (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(4,2), -- Nota de 0 a 10
    id_matricula INT,
    id_avaliacao INT,
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula),
    FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id_avaliacao)
);

-- 10. Tabela Frequência (Presença diária)
CREATE TABLE IF NOT EXISTS frequencia (
    id_frequencia INT AUTO_INCREMENT PRIMARY KEY,
    data_aula DATE NOT NULL,
    presente BOOLEAN DEFAULT FALSE,
    id_matricula INT,
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula)
);