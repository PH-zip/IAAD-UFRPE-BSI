# 📊 Informações do Dataset - Consultas Médicas

## 🎯 Resumo do Dataset

Este banco de dados contém um sistema completo de gestão de consultas médicas com dados robustos para análise e desenvolvimento.

---

## 📈 Estatísticas Totais

| Tabela | Quantidade de Registros |
|--------|------------------------|
| 🏥 **Clínicas** | **30** |
| 👨‍⚕️ **Médicos** | **50** |
| 👤 **Pacientes** | **70** |
| 📅 **Consultas** | **450** |

---

## 🏥 Clínicas (30 registros)

Distribuídas por diversas regiões de São Paulo e outras cidades:
- Clínicas especializadas (Cardiologia, Oftalmologia, Dermatologia, etc.)
- Hospitais gerais e regionais
- Centros médicos de diagnóstico
- Clínicas populares
- Unidades de atendimento especializadas

**Exemplos:**
- Clínica Saúde Total
- Hospital Infantil Pequeno Príncipe
- Centro de Diagnósticos MedImagem
- Clínica Neurológica NeuroVida
- Hospital Regional Norte

---

## 👨‍⚕️ Médicos (50 registros)

### Especialidades Disponíveis:
- **Cardiologia** (3 médicos)
- **Pediatria** (3 médicos)
- **Ortopedia** (2 médicos)
- **Neurologia** (2 médicos)
- **Dermatologia** (2 médicos)
- **Ginecologia** (2 médicos)
- **Oftalmologia** (2 médicos)
- **Clínico Geral** (2 médicos)
- E mais 25+ especialidades únicas

### Distribuição por Gênero:
- Médicos (M): 25
- Médicas (F): 25
- **Perfeitamente equilibrado!**

---

## 👤 Pacientes (70 registros)

### Diversidade Demográfica:
- **Faixa Etária:** De recém-nascidos (2020) a idosos (1960)
- **Gênero:** Distribuição equilibrada entre masculino e feminino
- **Localizações:** Telefones de SP (11) e PE (81)

### Exemplos de Pacientes:
- Crianças: Davi Nascimento (2018), Giovanna Lima (2011)
- Adultos: Ana Souza (1990), Miguel Andrade (1987)
- Idosos: João Pedro (1960), Roberto Carlos (1965)

---

## 📅 Consultas (450 registros)

### Distribuição Temporal:

#### **Histórico (2023-2024)**
- 10 consultas realizadas
- Útil para análise retrospectiva

#### **Ano de 2025**
- **Novembro:** 58 consultas
- **Dezembro:** 29 consultas
- **Total 2025:** 87 consultas

#### **Ano de 2026 (Agendamentos Futuros)**
- **Janeiro:** 23 consultas
- **Fevereiro:** 20 consultas
- **Março:** 20 consultas
- **Abril:** 20 consultas
- **Maio:** 20 consultas
- **Junho:** 40 consultas
- **Julho:** 40 consultas
- **Agosto:** 40 consultas
- **Setembro:** 40 consultas
- **Outubro:** 40 consultas
- **Novembro:** 50 consultas
- **Total 2026:** 353 consultas

### Características das Consultas:
- ✅ Horários realistas (08:00 às 16:00)
- ✅ Distribuição entre todas as clínicas
- ✅ Todos os médicos com atendimentos
- ✅ Pacientes com consultas recorrentes
- ✅ Mix de consultas passadas e futuras

---

## 🔍 Casos de Uso para Análise

### 1️⃣ **Análises Temporais**
- Tendências mensais de consultas
- Picos de atendimento
- Sazonalidade

### 2️⃣ **Análises de Desempenho**
- Médicos com mais consultas
- Clínicas mais procuradas
- Especialidades em alta demanda

### 3️⃣ **Análises de Pacientes**
- Pacientes com mais retornos
- Distribuição etária dos atendimentos
- Padrões de consulta por gênero

### 4️⃣ **Análises Geográficas**
- Distribuição de consultas por clínica
- Concentração de atendimentos por região

### 5️⃣ **Análises Preditivas**
- Previsão de demanda futura
- Otimização de recursos
- Planejamento de escalas médicas

---

## 📊 Queries Úteis

### Top 5 Clínicas com Mais Consultas
```sql
SELECT c.NomeCli, COUNT(*) as total_consultas
FROM consulta con
JOIN clinica c ON con.CodCli = c.CodCli
GROUP BY c.NomeCli
ORDER BY total_consultas DESC
LIMIT 5;
```

### Top 5 Médicos Mais Requisitados
```sql
SELECT m.NomeMed, m.Especialidade, COUNT(*) as total_consultas
FROM consulta con
JOIN medico m ON con.CodMed = m.CodMed
GROUP BY m.CodMed, m.NomeMed, m.Especialidade
ORDER BY total_consultas DESC
LIMIT 5;
```

### Especialidades Mais Procuradas
```sql
SELECT m.Especialidade, COUNT(*) as total_consultas
FROM consulta con
JOIN medico m ON con.CodMed = m.CodMed
GROUP BY m.Especialidade
ORDER BY total_consultas DESC;
```

### Consultas Por Mês (2026)
```sql
SELECT 
    MONTH(Data_Hora) as mes,
    MONTHNAME(Data_Hora) as nome_mes,
    COUNT(*) as total_consultas
FROM consulta
WHERE YEAR(Data_Hora) = 2026
GROUP BY MONTH(Data_Hora), MONTHNAME(Data_Hora)
ORDER BY mes;
```

### Pacientes com Mais Consultas
```sql
SELECT p.NomePac, p.DataNascimento, COUNT(*) as total_consultas
FROM consulta con
JOIN paciente p ON con.CpfPaciente = p.CpfPaciente
GROUP BY p.CpfPaciente, p.NomePac, p.DataNascimento
ORDER BY total_consultas DESC
LIMIT 10;
```

### Taxa de Ocupação por Dia da Semana
```sql
SELECT 
    DAYNAME(Data_Hora) as dia_semana,
    COUNT(*) as total_consultas
FROM consulta
GROUP BY DAYNAME(Data_Hora), DAYOFWEEK(Data_Hora)
ORDER BY DAYOFWEEK(Data_Hora);
```

---

## 🎯 Objetivos Alcançados

✅ **450 consultas** (dentro da faixa solicitada de 250-500)  
✅ **30 clínicas** (variedade de locais)  
✅ **50 médicos** (diversas especialidades)  
✅ **70 pacientes** (perfis diversos)  
✅ **Dados realistas** (horários, datas, distribuição)  
✅ **Relacionamentos completos** (todas as FKs funcionando)  
✅ **Integridade referencial** (CASCADE configurado)  
✅ **Histórico + Futuro** (análise completa temporal)

---

## 🚀 Como Utilizar

1. **Importar o banco:**
   ```bash
   mysql -u root -p < DatabaseIAAD.sql
   ```

2. **Verificar importação:**
   ```sql
   USE consultasmedicas;
   SELECT COUNT(*) FROM consulta; -- Deve retornar 450
   ```

3. **Explorar os dados:**
   - Use as queries de exemplo acima
   - Crie seus próprios relatórios
   - Desenvolva dashboards

---

## 📝 Notas Importantes

- Todas as consultas têm relacionamentos válidos (clínica, médico e paciente existem)
- Datas distribuídas de forma realista ao longo do tempo
- CPFs únicos e válidos para cada paciente
- Códigos de médicos e clínicas únicos
- Pronto para uso em aplicações CRUD, dashboards e análises

---

## 🎓 Ideal Para:

- Projetos acadêmicos de Banco de Dados
- Desenvolvimento de sistemas CRUD
- Prática de SQL (queries complexas, joins, agregações)
- Criação de dashboards e visualizações
- Testes de performance
- Demonstrações de aplicações médicas

---

**Dataset preparado para o projeto IAAD-UFRPE-BSI**  
**Versão: 1.0 - Dezembro 2025**  
**Total de Registros: 600 (30+50+70+450)**
