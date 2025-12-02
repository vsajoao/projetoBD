USE escola_db;

-- 1. DEPARTAMENTOS
INSERT INTO departamento (nome, sigla) VALUES 
('Ciências Exatas e Tecnologia', 'CET'),
('Ciências Humanas e Sociais', 'CHS'),
('Ciências Biológicas', 'BIO'),
('Linguagens e Artes', 'ART'),
('Educação Física e Esportes', 'EFI');

-- 2. SALAS
INSERT INTO sala (numero_sala, capacidade, tipo) VALUES
('101-A', 40, 'Sala de Aula'),
('102-B', 35, 'Sala de Aula'),
('LAB-INFO-1', 20, 'Laboratório'),
('AUDITORIO', 100, 'Auditório'),
('LAB-QUI', 15, 'Laboratório');

-- 3. PROFESSORES
INSERT INTO professor (nome, email, titulacao, id_depto) VALUES
('Dr. Roberto Campos', 'roberto@escola.com', 'Doutorado', 1), -- Exatas
('Profa. Ana Clara', 'ana@escola.com', 'Mestrado', 2), -- Humanas
('Carlos Mendes', 'carlos@escola.com', 'Especialista', 1), -- Exatas
('Dra. Julia Paiva', 'julia@escola.com', 'Doutorado', 3), -- Bio
('Marcos Vinicius', 'marcos@escola.com', 'Mestrado', 4), -- Artes
('Fernanda Souza', 'fernanda@escola.com', 'Especialista', 5), -- Ed. Fisica
('Ricardo Oliveira', 'ricardo@escola.com', 'Mestrado', 1), -- Exatas
('Sofia Luz', 'sofia@escola.com', 'Doutorado', 2); -- Humanas

-- 4. DISCIPLINAS
INSERT INTO disciplina (nome, carga_horaria, ementa, id_depto) VALUES
('Cálculo I', 80, 'Limites, Derivadas e Integrais', 1),
('Algoritmos e Programação', 60, 'Lógica de programação e Python', 1),
('História da Arte', 40, 'Renascimento ao Modernismo', 2),
('Anatomia Humana', 60, 'Sistemas do corpo humano', 3),
('Literatura Brasileira', 40, 'Romantismo e Realismo', 4),
('Física Mecânica', 80, 'Leis de Newton e movimento', 1),
('Sociologia', 40, 'Indivíduo e Sociedade', 2),
('Banco de Dados', 60, 'Modelagem e SQL', 1);

-- 5. ALUNOS (15 Alunos para dar volume)
INSERT INTO aluno (nome, email, data_nascimento, matricula_ativa) VALUES
('Alice Ferreira', 'alice@aluno.com', '2005-01-10', 1),
('Bruno Silva', 'bruno@aluno.com', '2004-05-20', 1),
('Carla Dias', 'carla@aluno.com', '2005-03-15', 1),
('Daniel Rocha', 'daniel@aluno.com', '2003-11-30', 1),
('Eduarda Lima', 'duda@aluno.com', '2005-07-07', 1),
('Fabio Santos', 'fabio@aluno.com', '2004-02-28', 1),
('Gabriela Costa', 'gabi@aluno.com', '2005-09-12', 1),
('Hugo Almeida', 'hugo@aluno.com', '2003-12-25', 1),
('Isabela Martins', 'isa@aluno.com', '2005-04-18', 1),
('João Victor', 'joao@aluno.com', '2004-08-05', 1),
('Karina Melo', 'ka@aluno.com', '2005-06-22', 1),
('Lucas Pereira', 'lucas@aluno.com', '2003-10-10', 1),
('Mariana Alves', 'mari@aluno.com', '2005-01-30', 1),
('Nicolas Gomes', 'nick@aluno.com', '2004-03-03', 0), -- INATIVO
('Olivia Nunes', 'olivia@aluno.com', '2005-12-12', 1);

-- 6. TURMAS (Criando turmas variadas)
INSERT INTO turma (ano, semestre, id_disciplina, id_prof, id_sala) VALUES
(2025, 1, 2, 1, 3), -- Algoritmos (Lab Info) com Roberto
(2025, 1, 8, 3, 3), -- Banco de Dados (Lab Info) com Carlos
(2025, 1, 3, 2, 1), -- História Arte (Sala 101) com Ana
(2025, 1, 4, 4, 5), -- Anatomia (Lab Qui) com Julia
(2025, 1, 1, 7, 2), -- Cálculo (Sala 102) com Ricardo
(2025, 1, 5, 5, 1); -- Literatura (Sala 101) com Marcos

-- 7. AVALIAÇÕES (Criando provas para as turmas)
INSERT INTO avaliacao (descricao, peso, data_prevista, id_turma) VALUES
('Prova 1 - Lógica', 10.0, '2025-04-10', 1), -- Turma 1
('Projeto Final BD', 10.0, '2025-06-20', 2), -- Turma 2
('Seminário Renascimento', 10.0, '2025-05-15', 3), -- Turma 3
('Prova Prática Anatomia', 10.0, '2025-05-20', 4), -- Turma 4
('Teste de Derivadas', 5.0, '2025-04-05', 5), -- Turma 5
('Prova Final Cálculo', 5.0, '2025-06-30', 5); -- Turma 5

-- 8. MATRÍCULAS (Distribuindo alunos)
-- Turma 1 (Algoritmos)
INSERT INTO matricula (id_aluno, id_turma) VALUES (1, 1), (2, 1), (3, 1), (4, 1), (5, 1);
-- Turma 2 (Banco de Dados)
INSERT INTO matricula (id_aluno, id_turma) VALUES (1, 2), (2, 2), (6, 2), (7, 2), (8, 2);
-- Turma 3 (História da Arte)
INSERT INTO matricula (id_aluno, id_turma) VALUES (9, 3), (10, 3), (11, 3);
-- Turma 5 (Cálculo)
INSERT INTO matricula (id_aluno, id_turma) VALUES (12, 5), (13, 5), (15, 5), (4, 5);

-- 9. NOTAS (Lançando notas variadas para testar dashboards)
-- Notas de Algoritmos (Turma 1 - Avaliação 1)
INSERT INTO nota (valor, id_matricula, id_avaliacao) VALUES
(9.5, 1, 1), -- Alice
(8.0, 2, 1), -- Bruno
(4.5, 3, 1), -- Carla (Vermelha)
(10.0, 4, 1), -- Daniel
(7.0, 5, 1); -- Eduarda

-- Notas de BD (Turma 2 - Avaliação 2)
INSERT INTO nota (valor, id_matricula, id_avaliacao) VALUES
(8.0, 6, 2), -- Alice
(6.5, 7, 2), -- Bruno
(9.0, 8, 2), -- Fabio
(2.0, 9, 2), -- Gabriela (Nota baixa)
(10.0, 10, 2); -- Hugo

-- 10. FREQUÊNCIA (Simulando uma aula)
-- Aula de Algoritmos (Turma 1)
INSERT INTO frequencia (data_aula, presente, id_matricula) VALUES
('2025-03-10', 1, 1),
('2025-03-10', 1, 2),
('2025-03-10', 0, 3), -- Carla faltou
('2025-03-10', 1, 4),
('2025-03-10', 1, 5);