# 🚀 Guia de Instalação - MongoDB

## 📥 Passo 1: Baixar e Instalar

### Opção A: MongoDB Community Edition (Recomendado)

1. **Baixe o instalador:**
   - Acesse: https://www.mongodb.com/try/download/community
   - Selecione:
     - Version: `7.0.x` (mais recente)
     - Platform: `Windows`
     - Package: `MSI`

2. **Execute o instalador:**
   - Aceite os termos
   - Escolha: **Complete** installation
   - ✅ Marque: "Install MongoDB as a Service"
   - ✅ Marque: "Install MongoDB Compass" (interface gráfica)

3. **Finalize a instalação**

---

## 📥 Passo 2: Instalar MongoDB Compass (se não veio junto)

O **Compass** é a interface gráfica oficial (como o MySQL Workbench).

- Download: https://www.mongodb.com/try/download/compass
- Instale normalmente

---

## ✅ Passo 3: Verificar Instalação

Abra o PowerShell e teste:

```powershell
# Verificar versão do MongoDB
mongod --version

# Verificar versão do cliente
mongosh --version
```

Se aparecer a versão, está instalado! ✅

---

## 🐍 Passo 3.5: Instalar pymongo na Virtual Environment

Para usar MongoDB com Python, você precisa instalar o driver `pymongo`:

```powershell
# 1. Ative a virtual environment (se não estiver ativada)
& C:\Users\PC\IAAD-UFRPE-BSI\.venv\Scripts\Activate.ps1

# 2. Instale o pymongo
pip install pymongo

# 3. Verifique a instalação
python -c "import pymongo; print(pymongo.__version__)"
```

**Resultado esperado:** Versão do pymongo (ex: `4.15.5`)

**Nota:** O `pymongo` é necessário para executar os scripts Python de importação e CRUD!

---

## 🔧 Passo 4: Iniciar o MongoDB

### Windows (Serviço automático)

Se instalou como serviço, o MongoDB já está rodando! Verifique:

```powershell
Get-Service MongoDB
```

Deve mostrar: **Status: Running**

Se não estiver rodando:

```powershell
Start-Service MongoDB
```

---

## 🗂️ Passo 5: Importar os Dados do Projeto

### Método 1: Via Terminal (mongoimport)

Navegue até a pasta MongoDB do projeto:

```powershell
cd C:\Users\PC\IAAD-UFRPE-BSI\MongoDB

# Importar cada coleção
mongoimport --db ConsultasMedicas --collection Pacientes --file ConsultasMedicas.Pacientes.json --jsonArray

mongoimport --db ConsultasMedicas --collection Medicos --file ConsultasMedicas.Medicos.json --jsonArray

mongoimport --db ConsultasMedicas --collection Clinicas --file ConsultasMedicas.Clinicas.json --jsonArray

mongoimport --db ConsultasMedicas --collection Consultas --file ConsultasMedicas.Consultas.json --jsonArray
```

**Resultado esperado:** 
```
imported X documents
```

---

### Método 2: Via MongoDB Compass (Interface Gráfica)

1. **Abra o MongoDB Compass**
2. **Conecte ao servidor local:**
   - Connection string: `mongodb://localhost:27017`
   - Clique em **Connect**

3. **Crie o banco de dados:**
   - Clique em: **+ Create Database**
   - Database Name: `ConsultasMedicas`
   - Collection Name: `Pacientes`
   - Clique em **Create Database**

4. **Importar documentos:**
   - Selecione a coleção `Pacientes`
   - Clique em **ADD DATA** → **Import JSON or CSV file**
   - Selecione: `ConsultasMedicas.Pacientes.json`
   - Clique em **Import**

5. **Repita para as outras coleções:**
   - Medicos
   - Clinicas
   - Consultas

---

## 📊 Passo 6: Verificar os Dados

### Via Compass:
- Navegue em: `ConsultasMedicas` → Cada coleção
- Veja os documentos importados

### Via Terminal (mongosh):

```powershell
# Abrir shell do MongoDB
mongosh

# Usar o banco
use ConsultasMedicas

# Contar documentos
db.Pacientes.countDocuments()
db.Medicos.countDocuments()
db.Clinicas.countDocuments()
db.Consultas.countDocuments()

# Ver um documento de exemplo
db.Pacientes.findOne()
```

---

## 🎯 Comandos Úteis

### Listar bancos de dados:
```javascript
show dbs
```

### Usar um banco:
```javascript
use ConsultasMedicas
```

### Listar coleções:
```javascript
show collections
```

### Buscar todos os documentos:
```javascript
db.Pacientes.find().pretty()
```

### Buscar com filtro:
```javascript
db.Pacientes.find({ Sexo: "F" })
```

### Contar documentos:
```javascript
db.Pacientes.countDocuments()
```

---

## 🆘 Solução de Problemas

### Erro: "mongoimport não reconhecido"
**Solução:** Adicione o MongoDB ao PATH do Windows:
1. Painel de Controle → Sistema → Configurações avançadas
2. Variáveis de Ambiente
3. Editar PATH
4. Adicionar: `C:\Program Files\MongoDB\Server\7.0\bin`

### Erro: "Failed to connect"
**Solução:** 
```powershell
# Verificar se o serviço está rodando
Get-Service MongoDB

# Se não estiver, inicie:
Start-Service MongoDB
```

### Erro na importação: "EOF"
**Solução:** Verifique se o arquivo JSON está correto (não pode ter vírgula extra no final).

---

## 📚 Recursos Adicionais

- **Documentação oficial:** https://www.mongodb.com/docs/
- **MongoDB University (grátis):** https://university.mongodb.com/
- **Compass Tutorial:** https://www.mongodb.com/docs/compass/

---

## ✅ Checklist Final

- [ ] MongoDB instalado e rodando
- [ ] MongoDB Compass instalado
- [ ] Conectado ao servidor local
- [ ] Banco `ConsultasMedicas` criado
- [ ] 4 coleções importadas (Pacientes, Medicos, Clinicas, Consultas)
- [ ] Dados verificados no Compass

---

**Pronto! Seu MongoDB está configurado e pronto para uso!** 🎉
