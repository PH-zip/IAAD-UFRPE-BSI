-- Aqui serão testados os erros gerados pelos triggers

-- teste de marcar consulta com medico que não existe
INSERT INTO consulta (CodCli, CodMed, CpfPaciente, Data_Hora) 
VALUES (1, 'MED999', '12345678900', '2025-12-25 14:00:00');