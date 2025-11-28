-- impedir a marcacao de consultas fora do horario
DROP TRIGGER IF EXISTS trg_horario_comercial;
DELIMITER $$

CREATE TRIGGER trg_horario_comercial
BEFORE INSERT ON consulta
FOR EACH ROW
BEGIN
    -- bloqueia fora do horário comercial 08:00:00 - 18:00:00
    IF TIME(NEW.Data_Hora) < '08:00:00' OR TIME(NEW.Data_Hora) > '18:00:00' THEN        
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Consultas só podem ser marcadas entre 08:00 e 18:00.';
    END IF;
END$$
DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_auditoria_consulta
AFTER INSERT ON consulta
FOR EACH ROW
BEGIN
    --vai registrar uma mensagem na tabela de log_auditoria
    INSERT INTO log_auditoria (Mensagem, DataOcorrencia)
    VALUES (CONCAT('Nova consulta agendada. ID: ', NEW.IdConsulta, ' - Paciente: ', NEW.CpfPaciente), NOW());
END$$

DELIMITER ;