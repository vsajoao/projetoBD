USE escola_db;

DELIMITER //

CREATE TRIGGER trg_validar_nota_insert
BEFORE INSERT ON nota
FOR EACH ROW
BEGIN
    IF NEW.valor < 0 OR NEW.valor > 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERRO DE VALIDAÇÃO: A nota deve ser um valor entre 0.0 e 10.0';
    END IF;
END //

CREATE TRIGGER trg_validar_nota_update
BEFORE UPDATE ON nota
FOR EACH ROW
BEGIN
    IF NEW.valor < 0 OR NEW.valor > 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERRO DE VALIDAÇÃO: A nota atualizada deve ser um valor entre 0.0 e 10.0';
    END IF;
END //

DELIMITER ;