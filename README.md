🏥 Sistema de Gestão de Consultas Médicas 

Este repositório reúne todos os materiais desenvolvidos para a 2ª VA da disciplina de Banco de Dados(IAAD-UFRPE). O projeto foi dividido em duas partes:

a criação de um sistema CRUD com interface gráfica usando MySQL, e uma análise prática sobre bancos NoSQL utilizando MongoDB.

📋 Sobre o Projeto

A proposta é simular um pequeno sistema de consultas médicas, permitindo gerenciar pacientes, médicos, clínicas e seus respectivos agendamentos.

🚀 Tecnologias Utilizadas
Linguagem: Python 3.10+
Interface: Streamlit
Banco Relacional: MySQL 8.0
Banco NoSQL: MongoDB

## 🎯 Como Começar - GUIA RÁPIDO

### 1️⃣ Instalar MySQL
Siga o guia detalhado: **[COMO_RODAR_MYSQL.md](COMO_RODAR_MYSQL.md)**

### 2️⃣ Criar e Popular o Banco de Dados
```powershell
# Opção A: MySQL Workbench (Recomendado)
# - Abra o MySQL Workbench
# - File → Open SQL Script → DatabaseIAAD.sql
# - Execute (ícone do raio ⚡)
# - Pronto! O banco já vem com 450 consultas!

# Opção B: Linha de Comando
mysql -u root -p
# Digite a senha, depois:
SOURCE DatabaseIAAD.sql;
exit;
```

### 3️⃣ Verificar os Dados
```powershell
# Opção A: MySQL Workbench
# Execute o arquivo: verificar_dataset.sql

# Opção B: Linha de Comando
mysql -u root -p consultasmedicas < verificar_dataset.sql
```

### 4️⃣ Testar a Conexão
```powershell
python teste_conexao.py
```

### 5️⃣ Rodar a Aplicação
```powershell
pip install -r requirements.txt
streamlit run main.py
```

---

## 📁 Estrutura dos Arquivos

```
📦 IAAD-UFRPE-BSI/
├── 📄 DatabaseIAAD.sql          # Criação do banco + dados iniciais
├── 📄 popular_dados.sql         # Dados adicionais (116+ consultas)
├── 📄 cascata.sql               # Teste de deleção em cascata
├── 📄 trigger.sql               # Trigger de auditoria
├── 📄 queries.sql               # Consultas úteis
├── 📄 main.py                   # Aplicação Streamlit
├── 📄 popular_banco.py          # Script para popular banco
├── 📄 teste_conexao.py          # Teste rápido de conexão
├── 📄 COMO_RODAR_MYSQL.md       # Guia completo de instalação
└── 📄 requirements.txt          # Dependências Python
```

---

⚙️ Parte 1: Implementação MySQL

Nesta primeira parte, estamos desenvolvendo um sistema web simples para administrar informações da clínica.

 CRUD completo: cadastrar, visualizar, editar e excluir registros.
 Controle de integridade: tratamento de chaves estrangeiras e deleção em cascata (ex.: excluir um paciente remove suas consultas).
 Trigger de auditoria: registro automático de ações críticas na tabela log_auditoria.
 Dashboard: gráficos e métricas para acompanhar o funcionamento da clínica.

🗄️ Estrutura do Banco de Dados (DER)

O banco consultasmedicas é formado pelas seguintes tabelas:
- **clinica** – informações das unidades de atendimento (15 clínicas)
- **medico** – dados dos profissionais e suas especialidades (30 médicos)
- **paciente** – informações pessoais dos pacientes (40 pacientes)
- **consulta** – agendamentos, relacionando médico + paciente + clínica (116+ consultas)
- **log_auditoria** – histórico de logs gerado pelo trigger

## 📊 Estatísticas do Dataset

O banco de dados já vem completamente populado no arquivo `DatabaseIAAD.sql`:
- ✅ **30 clínicas** cadastradas em diversas regiões
- ✅ **50 médicos** de 25+ especialidades diferentes
- ✅ **70 pacientes** com perfis demográficos variados
- ✅ **450 consultas** distribuídas de 2023 até novembro/2026
- ✅ **Logs de auditoria** automáticos via trigger
- ✅ **Total: 600 registros** prontos para uso

**Distribuição temporal das consultas:**
- 📅 2023-2024: 10 consultas (histórico)
- 📅 2025: 87 consultas (novembro e dezembro)
- 📅 2026: 353 consultas agendadas (janeiro a novembro)

👉 **Atende perfeitamente o requisito de 250-500 consultas!**
