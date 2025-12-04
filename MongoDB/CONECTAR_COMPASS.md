# 🧭 Como Conectar ao MongoDB Compass

## 📍 String de Conexão

```
mongodb://localhost:27017
```

## 🔧 Passos para Conectar:

1. **Abra o MongoDB Compass** (se ainda não estiver instalado, baixe em: https://www.mongodb.com/try/download/compass)

2. **Na tela inicial**, você verá um campo "New Connection"

3. **Cole a string de conexão**:
   ```
   mongodb://localhost:27017
   ```

4. **Clique em "Connect"**

5. **Navegue até o banco de dados**:
   - Você verá "ConsultasMedicas" na lista de databases
   - Clique nele para expandir

6. **Explore as coleções**:
   - 📋 **Pacientes** (4 documentos)
   - 👨‍⚕️ **Medicos** (5 documentos)
   - 📍 **Clinicas** (2 documentos)
   - 📅 **Consultas** (7 documentos)

## 📊 O que você pode fazer no Compass:

✅ **Visualizar** todos os documentos em formato JSON  
✅ **Filtrar** dados usando queries  
✅ **Inserir** novos documentos visualmente  
✅ **Editar** documentos existentes  
✅ **Deletar** documentos  
✅ **Ver estatísticas** das coleções  
✅ **Criar índices** para melhorar performance  
✅ **Executar aggregations** complexas  

## 🔍 Exemplos de Queries no Compass:

### Buscar paciente por nome:
```json
{ "nome": "Paulo Martins" }
```

### Buscar médicos por especialidade:
```json
{ "especialidade": "Pediatria" }
```

### Buscar consultas de um paciente específico:
```json
{ "paciente_id": "58961234752" }
```

## 🎨 Interface Visual:

O Compass mostra os dados de forma muito mais amigável que o terminal, com:
- 📊 Gráficos e estatísticas
- 🎨 Syntax highlighting para JSON
- 🔍 Busca e filtros avançados
- ✏️ Editor visual de documentos
- 📈 Análise de schema
- 🚀 Explain plans para queries

---

**Pronto! Agora você pode explorar seus dados visualmente! 🎉**
