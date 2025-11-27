import streamlit as st
import mysql.connector

st.title("🏥Consulta")

# Conectar com o workbench
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="root",  #trocar pela sua senha 
        database="consultasmedicas"
    )

st.subheader("Listar Pacientes")

if st.button("Carregar pacientes"):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT NomePac, CpfPaciente FROM paciente")
    dados = cursor.fetchall()

    for nome, cpf in dados:
        st.write(f"**{nome}** : {cpf}")

    cursor.close()
    
    con.close()
