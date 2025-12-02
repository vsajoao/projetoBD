USE escola_db;

CREATE VIEW vw_boletim_completo AS
SELECT 
    m.id_matricula,
    a.id_aluno,
    a.nome AS Aluno_Nome,
    a.foto AS Aluno_Foto,
    a.email AS Aluno_Email,
    
    -- Dados da Turma e Disciplina
    d.nome AS Disciplina,
    dept.sigla AS Depto,
    p.nome AS Professor,
    CONCAT(t.ano, '/', t.semestre) AS Periodo,
    s.numero_sala AS Sala,
    
    -- Subconsulta 1: Cálculo da Média das notas lançadas
    (
        SELECT ROUND(COALESCE(AVG(n.valor), 0), 2) 
        FROM nota n 
        WHERE n.id_matricula = m.id_matricula
    ) AS Media_Final,
    
    -- Subconsulta 2: Concatena as descrições das provas e notas (Ex: "P1: 8.0 | P2: 9.5")
    (
        SELECT GROUP_CONCAT(CONCAT(av.descricao, ': ', n.valor) SEPARATOR ' | ')
        FROM nota n
        JOIN avaliacao av ON n.id_avaliacao = av.id_avaliacao
        WHERE n.id_matricula = m.id_matricula
    ) AS Detalhe_Notas,
    
    -- Subconsulta 3: Total de Aulas (Dias lançados na frequência)
    (
        SELECT COUNT(*) 
        FROM frequencia f 
        WHERE f.id_matricula = m.id_matricula
    ) AS Total_Aulas_Registradas,
    
    -- Subconsulta 4: Total de Presenças (Soma onde presente = true)
    (
        SELECT SUM(CASE WHEN f.presente = 1 THEN 1 ELSE 0 END) 
        FROM frequencia f 
        WHERE f.id_matricula = m.id_matricula
    ) AS Total_Presencas,
    
    -- Status da Matrícula
    m.status AS Situacao_Matricula

FROM matricula m
JOIN aluno a ON m.id_aluno = a.id_aluno
JOIN turma t ON m.id_turma = t.id_turma
JOIN disciplina d ON t.id_disciplina = d.id_disciplina
JOIN departamento dept ON d.id_depto = dept.id_depto
JOIN professor p ON t.id_prof = p.id_prof
LEFT JOIN sala s ON t.id_sala = s.id_sala;