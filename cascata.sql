-- teste de deleção em cascata do paciente e suas consultas
-- mostrando o paciente e suas consultas 
SELECT * FROM consulta WHERE CpfPaciente = '11122233344';

DELETE FROM paciente WHERE CpfPaciente = '11122233344';

-- mostrando o paciente e suas consultas depois do delete em cascata
SELECT * FROM consulta WHERE CpfPaciente = '11122233344';
