DELIMITER //

CREATE PROCEDURE sp_atualizar_status_aluno(IN p_id_matricula INT)
BEGIN
    -- Declaração de variáveis para armazenar os cálculos
    DECLARE v_media DECIMAL(4,2) DEFAULT 0.0;
    DECLARE v_total_aulas INT DEFAULT 0;
    DECLARE v_presencas INT DEFAULT 0;
    DECLARE v_freq_perc DECIMAL(5,2) DEFAULT 100.0;
    
    -- 1. Calcular a Média das Notas
    SELECT COALESCE(AVG(valor), 0) INTO v_media
    FROM nota
    WHERE id_matricula = p_id_matricula;
    
    -- 2. Calcular Frequência (Total de Aulas vs Presenças)
    SELECT 
        COUNT(*), 
        COALESCE(SUM(CASE WHEN presente = 1 THEN 1 ELSE 0 END), 0)
    INTO v_total_aulas, v_presencas
    FROM frequencia
    WHERE id_matricula = p_id_matricula;
    
    -- 3. Calcular Porcentagem de Frequência
    -- Evita divisão por zero se não houver chamadas lançadas
    IF v_total_aulas > 0 THEN
        SET v_freq_perc = (v_presencas / v_total_aulas) * 100;
    ELSE
        SET v_freq_perc = 100.0; -- Assume 100% se não houve aula
    END IF;
    
    -- 4. Lógica de Aprovação (Regra de Negócio)
    -- Regra 1: Reprovação por Falta (< 75% de frequência)
    IF v_freq_perc < 75.0 THEN
        UPDATE matricula 
        SET status = 'REPROVADO POR FALTA' 
        WHERE id_matricula = p_id_matricula;
        
    -- Regra 2: Reprovação por Nota (< 6.0)
    ELSEIF v_media < 6.0 THEN
        UPDATE matricula 
        SET status = 'REPROVADO POR NOTA' 
        WHERE id_matricula = p_id_matricula;
        
    -- Regra 3: Aprovado
    ELSE
        UPDATE matricula 
        SET status = 'APROVADO' 
        WHERE id_matricula = p_id_matricula;
    END IF;
    
END //

DELIMITER ;