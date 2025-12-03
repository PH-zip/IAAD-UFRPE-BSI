import mysql.connector
import sys

# Teste de conexão
print("🔍 Testando conexão com MySQL...")
print("-" * 50)

# Primeira tentativa com a senha do código
senha = "Art2005@"

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senha
    )
    
    if conexao.is_connected():
        print(f"✅ Conectado ao MySQL com sucesso!")
        print(f"   Host: localhost")
        print(f"   Usuário: root")
        
        cursor = conexao.cursor()
        
        # Verificar se o banco consultasmedicas existe
        cursor.execute("SHOW DATABASES LIKE 'consultasmedicas'")
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"✅ Banco 'consultasmedicas' encontrado!")
            
            # Verificar tabelas
            cursor.execute("USE consultasmedicas")
            cursor.execute("SHOW TABLES")
            tabelas = cursor.fetchall()
            
            print(f"\n📋 Tabelas encontradas: {len(tabelas)}")
            for tabela in tabelas:
                print(f"   - {tabela[0]}")
                
            # Contar registros
            print(f"\n📊 Resumo de dados:")
            cursor.execute("SELECT COUNT(*) FROM clinica")
            print(f"   Clínicas: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM medico")
            print(f"   Médicos: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM paciente")
            print(f"   Pacientes: {cursor.fetchone()[0]}")
            
            cursor.execute("SELECT COUNT(*) FROM consulta")
            print(f"   Consultas: {cursor.fetchone()[0]}")
            
            print(f"\n✅ Tudo pronto para rodar o sistema!")
            
        else:
            print(f"⚠️  Banco 'consultasmedicas' NÃO encontrado!")
            print(f"   Execute: mysql -u root -p < DatabaseIAAD.sql")
        
        cursor.close()
        conexao.close()
        
except mysql.connector.Error as erro:
    print(f"❌ Erro na conexão: {erro}")
    print(f"\n💡 Possíveis soluções:")
    print(f"   1. Verifique se o MySQL está rodando")
    print(f"   2. Verifique se a senha '{senha}' está correta")
    print(f"   3. Execute: Get-Service -Name MySQL*")
    sys.exit(1)

except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)
