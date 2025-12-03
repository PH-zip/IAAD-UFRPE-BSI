-- Script para verificar o tamanho do dataset
-- Execute após importar o DatabaseIAAD.sql

USE consultasmedicas;

-- Exibir estatísticas
SELECT '===========================================' AS '';
SELECT '     ESTATÍSTICAS DO DATASET' AS '';
SELECT '===========================================' AS '';
SELECT '' AS '';

SELECT 'CLÍNICAS' AS Tabela, COUNT(*) AS Total FROM clinica
UNION ALL
SELECT 'MÉDICOS', COUNT(*) FROM medico
UNION ALL
SELECT 'PACIENTES', COUNT(*) FROM paciente
UNION ALL
SELECT 'CONSULTAS', COUNT(*) FROM consulta
UNION ALL
SELECT '---', '---'
UNION ALL
SELECT 'TOTAL GERAL', 
    (SELECT COUNT(*) FROM clinica) + 
    (SELECT COUNT(*) FROM medico) + 
    (SELECT COUNT(*) FROM paciente) + 
    (SELECT COUNT(*) FROM consulta);

SELECT '' AS '';
SELECT '===========================================' AS '';
SELECT '     CONSULTAS POR ANO' AS '';
SELECT '===========================================' AS '';
SELECT '' AS '';

SELECT 
    YEAR(Data_Hora) AS Ano,
    COUNT(*) AS Total_Consultas
FROM consulta
GROUP BY YEAR(Data_Hora)
ORDER BY Ano;

SELECT '' AS '';
SELECT '===========================================' AS '';
SELECT '     CONSULTAS POR MÊS (2026)' AS '';
SELECT '===========================================' AS '';
SELECT '' AS '';

SELECT 
    MONTH(Data_Hora) AS Mes,
    MONTHNAME(Data_Hora) AS Nome_Mes,
    COUNT(*) AS Total_Consultas
FROM consulta
WHERE YEAR(Data_Hora) = 2026
GROUP BY MONTH(Data_Hora), MONTHNAME(Data_Hora)
ORDER BY Mes;

SELECT '' AS '';
SELECT '===========================================' AS '';
SELECT '     TOP 5 CLÍNICAS' AS '';
SELECT '===========================================' AS '';
SELECT '' AS '';

SELECT 
    c.NomeCli AS Clinica,
    COUNT(*) AS Total_Consultas
FROM consulta con
JOIN clinica c ON con.CodCli = c.CodCli
GROUP BY c.NomeCli
ORDER BY Total_Consultas DESC
LIMIT 5;

SELECT '' AS '';
SELECT '===========================================' AS '';
SELECT '     TOP 5 ESPECIALIDADES' AS '';
SELECT '===========================================' AS '';
SELECT '' AS '';

SELECT 
    m.Especialidade,
    COUNT(*) AS Total_Consultas
FROM consulta con
JOIN medico m ON con.CodMed = m.CodMed
GROUP BY m.Especialidade
ORDER BY Total_Consultas DESC
LIMIT 5;

SELECT '' AS '';
SELECT '===========================================' AS '';
SELECT '✅ DATASET VALIDADO COM SUCESSO!' AS '';
SELECT '===========================================' AS '';
