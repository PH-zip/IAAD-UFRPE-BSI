import streamlit as st
import mysql.connector
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Sistema de Consultas Médicas", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para interface profissional
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #e3f2fd;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    .trigger-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏥 Sistema de Consultas Médicas</div>', unsafe_allow_html=True)

# Conectar com o workbench
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Art2005@",
        database="consultasmedicas"
    )

# Função para obter estatísticas do dashboard
def obter_estatisticas():
    try:
        con = conectar()
        cursor = con.cursor()
        
        stats = {}
        
        # Total de pacientes
        cursor.execute("SELECT COUNT(*) FROM paciente")
        stats['total_pacientes'] = cursor.fetchone()[0]
        
        # Total de consultas
        cursor.execute("SELECT COUNT(*) FROM consulta")
        stats['total_consultas'] = cursor.fetchone()[0]
        
        # Total de médicos
        cursor.execute("SELECT COUNT(*) FROM medico")
        stats['total_medicos'] = cursor.fetchone()[0]
        
        # Total de clínicas
        cursor.execute("SELECT COUNT(*) FROM clinica")
        stats['total_clinicas'] = cursor.fetchone()[0]
        
        # Consultas hoje
        cursor.execute("SELECT COUNT(*) FROM consulta WHERE DATE(Data_Hora) = CURDATE()")
        stats['consultas_hoje'] = cursor.fetchone()[0]
        
        # Consultas próximos 7 dias
        cursor.execute("""
            SELECT COUNT(*) FROM consulta 
            WHERE DATE(Data_Hora) BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        """)
        stats['consultas_proximos_7_dias'] = cursor.fetchone()[0]
        
        cursor.close()
        con.close()
        
        return stats
    except mysql.connector.Error as err:
        st.error(f"Erro ao obter estatísticas: {err}")
        return None

# Criar menu de navegação
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2382/2382461.png", width=100)
    st.markdown("### 📊 Navegação")
    menu = st.selectbox(
        "Selecione uma opção:",
        ["🏠 Dashboard", "👥 Gerenciar Pacientes", "📅 Gerenciar Consultas", "📋 Logs de Auditoria", "⚙️ Triggers do Sistema"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📈 Resumo Rápido")
    stats = obter_estatisticas()
    if stats:
        st.metric("Pacientes", stats['total_pacientes'])
        st.metric("Consultas", stats['total_consultas'])
        st.metric("Médicos", stats['total_medicos'])

# ==================== DASHBOARD ====================
if menu == "🏠 Dashboard":
    st.header("📊 Dashboard Principal")
    
    stats = obter_estatisticas()
    
    if stats:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👥 Total de Pacientes",
                value=stats['total_pacientes'],
                delta="Cadastrados"
            )
        
        with col2:
            st.metric(
                label="📅 Total de Consultas",
                value=stats['total_consultas'],
                delta=f"+{stats['consultas_hoje']} hoje"
            )
        
        with col3:
            st.metric(
                label="👨‍⚕️ Médicos Ativos",
                value=stats['total_medicos'],
                delta="Disponíveis"
            )
        
        with col4:
            st.metric(
                label="🏥 Clínicas",
                value=stats['total_clinicas'],
                delta="Ativas"
            )
        
        st.markdown("---")
        
        # Gráficos interativos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Consultas por Dia da Semana")
            try:
                con = conectar()
                df_consultas = pd.read_sql("""
                    SELECT 
                        DAYNAME(Data_Hora) as dia_semana,
                        COUNT(*) as total
                    FROM consulta
                    GROUP BY DAYNAME(Data_Hora), DAYOFWEEK(Data_Hora)
                    ORDER BY DAYOFWEEK(Data_Hora)
                """, con)
                con.close()
                
                if not df_consultas.empty:
                    # Traduzir dias da semana
                    dias_pt = {
                        'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                        'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
                    }
                    df_consultas['dia_semana'] = df_consultas['dia_semana'].map(dias_pt)
                    
                    fig1 = px.bar(
                        df_consultas,
                        x='dia_semana',
                        y='total',
                        color='total',
                        color_continuous_scale='Blues',
                        labels={'dia_semana': 'Dia da Semana', 'total': 'Número de Consultas'},
                        title=""
                    )
                    fig1.update_layout(showlegend=False, height=350)
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("Nenhuma consulta agendada ainda.")
            except Exception as e:
                st.error(f"Erro ao gerar gráfico: {e}")
        
        with col2:
            st.subheader("🩺 Consultas por Especialidade")
            try:
                con = conectar()
                df_especialidade = pd.read_sql("""
                    SELECT 
                        m.Especialidade,
                        COUNT(*) as total
                    FROM consulta c
                    JOIN medico m ON c.CodMed = m.CodMed
                    GROUP BY m.Especialidade
                    ORDER BY total DESC
                """, con)
                con.close()
                
                if not df_especialidade.empty:
                    fig2 = px.pie(
                        df_especialidade,
                        values='total',
                        names='Especialidade',
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        title=""
                    )
                    fig2.update_traces(textposition='inside', textinfo='percent+label')
                    fig2.update_layout(height=350)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("Nenhuma consulta agendada ainda.")
            except Exception as e:
                st.error(f"Erro ao gerar gráfico: {e}")
        
        # Gráfico de linha - Consultas ao longo do tempo
        st.subheader("📅 Tendência de Consultas nos Últimos 30 Dias")
        try:
            con = conectar()
            df_tempo = pd.read_sql("""
                SELECT 
                    DATE(Data_Hora) as data,
                    COUNT(*) as total
                FROM consulta
                WHERE Data_Hora >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY DATE(Data_Hora)
                ORDER BY data
            """, con)
            con.close()
            
            if not df_tempo.empty:
                fig3 = px.line(
                    df_tempo,
                    x='data',
                    y='total',
                    markers=True,
                    labels={'data': 'Data', 'total': 'Número de Consultas'},
                    title=""
                )
                fig3.update_traces(line_color='#1f77b4', line_width=3)
                fig3.update_layout(height=400)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Nenhuma consulta nos últimos 30 dias.")
        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {e}")
        
        # Tabela de próximas consultas
        st.subheader("🔔 Próximas Consultas")
        try:
            con = conectar()
            df_proximas = pd.read_sql("""
                SELECT 
                    c.Data_Hora as 'Data/Hora',
                    p.NomePac as 'Paciente',
                    m.NomeMed as 'Médico',
                    m.Especialidade,
                    cl.NomeCli as 'Clínica'
                FROM consulta c
                JOIN paciente p ON c.CpfPaciente = p.CpfPaciente
                JOIN medico m ON c.CodMed = m.CodMed
                JOIN clinica cl ON c.CodCli = cl.CodCli
                WHERE c.Data_Hora >= NOW()
                ORDER BY c.Data_Hora
                LIMIT 10
            """, con)
            con.close()
            
            if not df_proximas.empty:
                st.dataframe(df_proximas, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhuma consulta futura agendada.")
        except Exception as e:
            st.error(f"Erro ao carregar próximas consultas: {e}")
    else:
        st.warning("Não foi possível carregar as estatísticas do dashboard.")

# ==================== GERENCIAR PACIENTES ====================
elif menu == "👥 Gerenciar Pacientes":
    st.header("👥 Gerenciamento de Pacientes")
    
    # Estatísticas rápidas
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM paciente")
        total_pac = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM paciente WHERE Sexo = 'M'")
        total_m = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM paciente WHERE Sexo = 'F'")
        total_f = cursor.fetchone()[0]
        cursor.close()
        con.close()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Pacientes", total_pac)
        col2.metric("Masculino", total_m)
        col3.metric("Feminino", total_f)
        st.markdown("---")
    except:
        pass
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Cadastrar", "✏️ Atualizar", "🗑️ Excluir"])
    
    # READ - Listar Pacientes
    with tab1:
        st.subheader("Lista de Pacientes")
        
        if st.button("Carregar Pacientes", key="btn_listar"):
            try:
                con = conectar()
                cursor = con.cursor()
                cursor.execute("""
                    SELECT CpfPaciente, NomePac, DataNascimento, Sexo, Telefone, Email 
                    FROM paciente 
                    ORDER BY NomePac
                """)
                dados = cursor.fetchall()
                
                if dados:
                    st.write(f"**Total de pacientes:** {len(dados)}")
                    for cpf, nome, data_nasc, sexo, telefone, email in dados:
                        with st.expander(f"👤 {nome} - CPF: {cpf}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Data de Nascimento:** {data_nasc}")
                                st.write(f"**Sexo:** {sexo}")
                            with col2:
                                st.write(f"**Telefone:** {telefone}")
                                st.write(f"**Email:** {email}")
                else:
                    st.info("Nenhum paciente cadastrado.")
                
                cursor.close()
                con.close()
            except mysql.connector.Error as err:
                st.error(f"Erro ao listar pacientes: {err}")
    
    # CREATE - Cadastrar Paciente
    with tab2:
        st.subheader("Cadastrar Novo Paciente")
        
        with st.form("form_cadastrar_paciente"):
            cpf = st.text_input("CPF (11 dígitos)", max_chars=11, placeholder="12345678900")
            nome = st.text_input("Nome Completo", placeholder="João da Silva")
            data_nasc = st.date_input("Data de Nascimento", min_value=date(1900, 1, 1))
            sexo = st.selectbox("Sexo", ["M", "F"])
            telefone = st.text_input("Telefone", max_chars=13, placeholder="11999998888")
            email = st.text_input("Email", placeholder="email@exemplo.com")
            
            submitted = st.form_submit_button("Cadastrar Paciente")
            
            if submitted:
                if not cpf or len(cpf) != 11:
                    st.error("CPF deve ter exatamente 11 dígitos!")
                elif not nome:
                    st.error("Nome é obrigatório!")
                else:
                    try:
                        con = conectar()
                        cursor = con.cursor()
                        cursor.execute("""
                            INSERT INTO paciente (CpfPaciente, NomePac, DataNascimento, Sexo, Telefone, Email)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (cpf, nome, data_nasc, sexo, telefone, email))
                        con.commit()
                        cursor.close()
                        con.close()
                        st.success(f"✅ Paciente {nome} cadastrado com sucesso!")
                    except mysql.connector.Error as err:
                        st.error(f"Erro ao cadastrar paciente: {err}")
    
    # UPDATE - Atualizar Paciente
    with tab3:
        st.subheader("Atualizar Dados do Paciente")
        
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT CpfPaciente, NomePac FROM paciente ORDER BY NomePac")
            pacientes = cursor.fetchall()
            cursor.close()
            con.close()
            
            if pacientes:
                paciente_options = {f"{nome} - CPF: {cpf}": cpf for cpf, nome in pacientes}
                paciente_selecionado = st.selectbox("Selecione o Paciente", list(paciente_options.keys()))
                
                if paciente_selecionado:
                    cpf_selecionado = paciente_options[paciente_selecionado]
                    
                    # Buscar dados atuais do paciente
                    con = conectar()
                    cursor = con.cursor()
                    cursor.execute("""
                        SELECT NomePac, DataNascimento, Sexo, Telefone, Email 
                        FROM paciente WHERE CpfPaciente = %s
                    """, (cpf_selecionado,))
                    dados_atuais = cursor.fetchone()
                    cursor.close()
                    con.close()
                    
                    if dados_atuais:
                        with st.form("form_atualizar_paciente"):
                            novo_nome = st.text_input("Nome Completo", value=dados_atuais[0])
                            nova_data_nasc = st.date_input("Data de Nascimento", value=dados_atuais[1])
                            novo_sexo = st.selectbox("Sexo", ["M", "F"], index=0 if dados_atuais[2] == "M" else 1)
                            novo_telefone = st.text_input("Telefone", value=dados_atuais[3] or "")
                            novo_email = st.text_input("Email", value=dados_atuais[4] or "")
                            
                            submitted = st.form_submit_button("Atualizar Dados")
                            
                            if submitted:
                                try:
                                    con = conectar()
                                    cursor = con.cursor()
                                    cursor.execute("""
                                        UPDATE paciente 
                                        SET NomePac = %s, DataNascimento = %s, Sexo = %s, 
                                            Telefone = %s, Email = %s
                                        WHERE CpfPaciente = %s
                                    """, (novo_nome, nova_data_nasc, novo_sexo, novo_telefone, novo_email, cpf_selecionado))
                                    con.commit()
                                    cursor.close()
                                    con.close()
                                    st.success(f"✅ Dados de {novo_nome} atualizados com sucesso!")
                                except mysql.connector.Error as err:
                                    st.error(f"Erro ao atualizar paciente: {err}")
            else:
                st.info("Nenhum paciente cadastrado para atualizar.")
        except mysql.connector.Error as err:
            st.error(f"Erro ao carregar pacientes: {err}")
    
    # DELETE - Excluir Paciente
    with tab4:
        st.subheader("Excluir Paciente")
        st.warning("⚠️ Atenção: Ao excluir um paciente, todas as consultas associadas também serão excluídas (CASCADE).")
        
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT CpfPaciente, NomePac FROM paciente ORDER BY NomePac")
            pacientes = cursor.fetchall()
            cursor.close()
            con.close()
            
            if pacientes:
                paciente_options = {f"{nome} - CPF: {cpf}": cpf for cpf, nome in pacientes}
                paciente_selecionado = st.selectbox("Selecione o Paciente para Excluir", list(paciente_options.keys()), key="del_select")
                
                if paciente_selecionado:
                    cpf_selecionado = paciente_options[paciente_selecionado]
                    
                    # Verificar se há consultas associadas
                    con = conectar()
                    cursor = con.cursor()
                    cursor.execute("SELECT COUNT(*) FROM consulta WHERE CpfPaciente = %s", (cpf_selecionado,))
                    num_consultas = cursor.fetchone()[0]
                    cursor.close()
                    con.close()
                    
                    if num_consultas > 0:
                        st.warning(f"Este paciente possui {num_consultas} consulta(s) que será(ão) excluída(s) automaticamente.")
                    
                    confirmar = st.checkbox("Confirmo que desejo excluir este paciente")
                    
                    if st.button("Excluir Paciente", type="primary") and confirmar:
                        try:
                            con = conectar()
                            cursor = con.cursor()
                            cursor.execute("DELETE FROM paciente WHERE CpfPaciente = %s", (cpf_selecionado,))
                            con.commit()
                            cursor.close()
                            con.close()
                            st.success("✅ Paciente excluído com sucesso!")
                            st.rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Erro ao excluir paciente: {err}")
            else:
                st.info("Nenhum paciente cadastrado para excluir.")
        except mysql.connector.Error as err:
            st.error(f"Erro ao carregar pacientes: {err}")

# ==================== GERENCIAR CONSULTAS ====================
elif menu == "📅 Gerenciar Consultas":
    st.header("📅 Gerenciamento de Consultas")
    
    # Alert sobre triggers
    st.markdown("""
    <div class="trigger-box">
        <h4>⚡ Triggers Ativos:</h4>
        <ul>
            <li><strong>trg_horario_comercial:</strong> Valida horário 08:00-18:00 (BEFORE INSERT)</li>
            <li><strong>trg_auditoria_consulta:</strong> Registra log automaticamente (AFTER INSERT)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Agendar", "✏️ Atualizar", "🗑️ Cancelar"])
    
    # READ - Listar Consultas
    with tab1:
        st.subheader("Lista de Consultas")
        
        if st.button("Carregar Consultas", key="btn_listar_consultas"):
            try:
                con = conectar()
                cursor = con.cursor()
                cursor.execute("""
                    SELECT c.IdConsulta, c.Data_Hora, p.NomePac, m.NomeMed, m.Especialidade, cl.NomeCli
                    FROM consulta c
                    JOIN paciente p ON c.CpfPaciente = p.CpfPaciente
                    JOIN medico m ON c.CodMed = m.CodMed
                    JOIN clinica cl ON c.CodCli = cl.CodCli
                    ORDER BY c.Data_Hora DESC
                """)
                dados = cursor.fetchall()
                
                if dados:
                    st.write(f"**Total de consultas:** {len(dados)}")
                    for id_consulta, data_hora, nome_pac, nome_med, especialidade, nome_cli in dados:
                        with st.expander(f"🩺 Consulta #{id_consulta} - {data_hora.strftime('%d/%m/%Y %H:%M')}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Paciente:** {nome_pac}")
                                st.write(f"**Médico:** {nome_med}")
                            with col2:
                                st.write(f"**Especialidade:** {especialidade}")
                                st.write(f"**Clínica:** {nome_cli}")
                else:
                    st.info("Nenhuma consulta agendada.")
                
                cursor.close()
                con.close()
            except mysql.connector.Error as err:
                st.error(f"Erro ao listar consultas: {err}")
    
    # CREATE - Agendar Consulta
    with tab2:
        st.subheader("Agendar Nova Consulta")
        st.warning("⏰ Lembre-se: Consultas só podem ser agendadas entre 08:00 e 18:00 (Trigger ativo)")
        
        try:
            con = conectar()
            cursor = con.cursor()
            
            # Buscar listas
            cursor.execute("SELECT CodCli, NomeCli FROM clinica ORDER BY NomeCli")
            clinicas = cursor.fetchall()
            
            cursor.execute("SELECT CodMed, NomeMed, Especialidade FROM medico ORDER BY NomeMed")
            medicos = cursor.fetchall()
            
            cursor.execute("SELECT CpfPaciente, NomePac FROM paciente ORDER BY NomePac")
            pacientes = cursor.fetchall()
            
            cursor.close()
            con.close()
            
            with st.form("form_agendar_consulta"):
                clinica_options = {f"{nome}": cod for cod, nome in clinicas}
                clinica_selecionada = st.selectbox("Clínica", list(clinica_options.keys()))
                
                medico_options = {f"{nome} - {esp}": cod for cod, nome, esp in medicos}
                medico_selecionado = st.selectbox("Médico", list(medico_options.keys()))
                
                paciente_options = {f"{nome}": cpf for cpf, nome in pacientes}
                paciente_selecionado = st.selectbox("Paciente", list(paciente_options.keys()))
                
                col1, col2 = st.columns(2)
                with col1:
                    data_consulta = st.date_input("Data da Consulta", min_value=date.today())
                with col2:
                    hora_consulta = st.time_input("Horário da Consulta", value=None)
                
                submitted = st.form_submit_button("Agendar Consulta")
                
                if submitted:
                    if hora_consulta is None:
                        st.error("Por favor, selecione um horário!")
                    else:
                        data_hora = datetime.combine(data_consulta, hora_consulta)
                        
                        try:
                            con = conectar()
                            cursor = con.cursor()
                            cursor.execute("""
                                INSERT INTO consulta (CodCli, CodMed, CpfPaciente, Data_Hora)
                                VALUES (%s, %s, %s, %s)
                            """, (
                                clinica_options[clinica_selecionada],
                                medico_options[medico_selecionado],
                                paciente_options[paciente_selecionado],
                                data_hora
                            ))
                            con.commit()
                            cursor.close()
                            con.close()
                            st.success(f"✅ Consulta agendada com sucesso para {data_hora.strftime('%d/%m/%Y às %H:%M')}!")
                            st.info("📝 Um registro foi adicionado ao log de auditoria (visualize na aba 'Visualizar Logs de Auditoria')")
                        except mysql.connector.Error as err:
                            if "Consultas só podem ser marcadas entre 08:00 e 18:00" in str(err):
                                st.error("❌ TRIGGER ATIVADO: Consultas só podem ser marcadas entre 08:00 e 18:00!")
                            else:
                                st.error(f"Erro ao agendar consulta: {err}")
        except mysql.connector.Error as err:
            st.error(f"Erro ao carregar dados: {err}")
    
    # UPDATE - Atualizar Consulta
    with tab3:
        st.subheader("Atualizar Consulta")
        
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("""
                SELECT c.IdConsulta, c.Data_Hora, p.NomePac
                FROM consulta c
                JOIN paciente p ON c.CpfPaciente = p.CpfPaciente
                ORDER BY c.Data_Hora DESC
            """)
            consultas = cursor.fetchall()
            cursor.close()
            con.close()
            
            if consultas:
                consulta_options = {f"Consulta #{id_c} - {nome_pac} em {data_hora.strftime('%d/%m/%Y %H:%M')}": id_c 
                                    for id_c, data_hora, nome_pac in consultas}
                consulta_selecionada = st.selectbox("Selecione a Consulta", list(consulta_options.keys()))
                
                if consulta_selecionada:
                    id_consulta_selecionada = consulta_options[consulta_selecionada]
                    
                    with st.form("form_atualizar_consulta"):
                        nova_data = st.date_input("Nova Data", min_value=date.today())
                        nova_hora = st.time_input("Novo Horário")
                        
                        submitted = st.form_submit_button("Atualizar Consulta")
                        
                        if submitted:
                            nova_data_hora = datetime.combine(nova_data, nova_hora)
                            
                            try:
                                con = conectar()
                                cursor = con.cursor()
                                cursor.execute("""
                                    UPDATE consulta 
                                    SET Data_Hora = %s
                                    WHERE IdConsulta = %s
                                """, (nova_data_hora, id_consulta_selecionada))
                                con.commit()
                                cursor.close()
                                con.close()
                                st.success("✅ Consulta atualizada com sucesso!")
                            except mysql.connector.Error as err:
                                if "Consultas só podem ser marcadas entre 08:00 e 18:00" in str(err):
                                    st.error("❌ TRIGGER ATIVADO: Consultas só podem ser marcadas entre 08:00 e 18:00!")
                                else:
                                    st.error(f"Erro ao atualizar consulta: {err}")
            else:
                st.info("Nenhuma consulta disponível para atualizar.")
        except mysql.connector.Error as err:
            st.error(f"Erro ao carregar consultas: {err}")
    
    # DELETE - Cancelar Consulta
    with tab4:
        st.subheader("Cancelar Consulta")
        
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("""
                SELECT c.IdConsulta, c.Data_Hora, p.NomePac, m.NomeMed
                FROM consulta c
                JOIN paciente p ON c.CpfPaciente = p.CpfPaciente
                JOIN medico m ON c.CodMed = m.CodMed
                ORDER BY c.Data_Hora DESC
            """)
            consultas = cursor.fetchall()
            cursor.close()
            con.close()
            
            if consultas:
                consulta_options = {f"Consulta #{id_c} - {nome_pac} com {nome_med} em {data_hora.strftime('%d/%m/%Y %H:%M')}": id_c 
                                    for id_c, data_hora, nome_pac, nome_med in consultas}
                consulta_selecionada = st.selectbox("Selecione a Consulta para Cancelar", list(consulta_options.keys()), key="cancel_select")
                
                if consulta_selecionada:
                    id_consulta_selecionada = consulta_options[consulta_selecionada]
                    
                    confirmar = st.checkbox("Confirmo que desejo cancelar esta consulta")
                    
                    if st.button("Cancelar Consulta", type="primary") and confirmar:
                        try:
                            con = conectar()
                            cursor = con.cursor()
                            cursor.execute("DELETE FROM consulta WHERE IdConsulta = %s", (id_consulta_selecionada,))
                            con.commit()
                            cursor.close()
                            con.close()
                            st.success("✅ Consulta cancelada com sucesso!")
                            st.rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Erro ao cancelar consulta: {err}")
            else:
                st.info("Nenhuma consulta disponível para cancelar.")
        except mysql.connector.Error as err:
            st.error(f"Erro ao carregar consultas: {err}")

# ==================== VISUALIZAR LOGS DE AUDITORIA ====================
elif menu == "📋 Logs de Auditoria":
    st.header("📋 Logs de Auditoria")
    
    st.markdown("""
    <div class="trigger-box">
        <h4>📝 Trigger: trg_auditoria_consulta</h4>
        <p>Toda vez que uma consulta é agendada, este trigger registra automaticamente um log na tabela log_auditoria.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Histórico de Logs")
    with col2:
        if st.button("🔄 Atualizar Logs", use_container_width=True):
            st.rerun()
    
    try:
        con = conectar()
        
        # Total de logs
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM log_auditoria")
        total_logs = cursor.fetchone()[0]
        cursor.close()
        
        st.metric("Total de Registros de Auditoria", total_logs)
        
        # Gráfico de logs por data
        df_logs_tempo = pd.read_sql("""
            SELECT 
                DATE(DataOcorrencia) as data,
                COUNT(*) as total
            FROM log_auditoria
            GROUP BY DATE(DataOcorrencia)
            ORDER BY data DESC
            LIMIT 30
        """, con)
        
        if not df_logs_tempo.empty:
            fig_logs = px.bar(
                df_logs_tempo,
                x='data',
                y='total',
                labels={'data': 'Data', 'total': 'Logs Gerados'},
                title="Logs de Auditoria por Data",
                color='total',
                color_continuous_scale='Greens'
            )
            fig_logs.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_logs, use_container_width=True)
        
        # Tabela de logs
        df_logs = pd.read_sql("""
            SELECT 
                IdLog as 'ID',
                Mensagem,
                DATE_FORMAT(DataOcorrencia, '%d/%m/%Y %H:%i:%s') as 'Data/Hora'
            FROM log_auditoria 
            ORDER BY DataOcorrencia DESC
            LIMIT 100
        """, con)
        con.close()
        
        if not df_logs.empty:
            st.dataframe(
                df_logs,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Mensagem": st.column_config.TextColumn("Mensagem", width="large"),
                    "Data/Hora": st.column_config.TextColumn("Data/Hora", width="medium")
                }
            )
        else:
            st.info("Nenhum log de auditoria registrado ainda. Agende uma consulta para gerar registros automáticos!")
        
    except mysql.connector.Error as err:
        st.error(f"Erro ao carregar logs: {err}")

# ==================== TRIGGERS DO SISTEMA ====================
elif menu == "⚙️ Triggers do Sistema":
    st.header("⚙️ Triggers do Sistema")
    
    st.markdown("""
    Este sistema utiliza **triggers MySQL** para automatizar validações e registros. 
    Os triggers garantem integridade de dados e rastreabilidade de operações.
    """)
    
    # Trigger 1
    st.markdown("---")
    st.subheader("🔒 Trigger 1: Validação de Horário Comercial")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>trg_horario_comercial</h4>
            <p><strong>Tipo:</strong> BEFORE INSERT</p>
            <p><strong>Tabela:</strong> consulta</p>
            <p><strong>Função:</strong> Valida se a consulta está sendo agendada entre 08:00 e 18:00</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.code("""
DELIMITER $$
CREATE TRIGGER trg_horario_comercial
BEFORE INSERT ON consulta
FOR EACH ROW
BEGIN
    IF TIME(NEW.Data_Hora) < '08:00:00' 
       OR TIME(NEW.Data_Hora) > '18:00:00' 
    THEN        
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 
        'Consultas só podem ser marcadas 
        entre 08:00 e 18:00.';
    END IF;
END$$
DELIMITER ;
        """, language="sql")
    
    st.markdown("**💡 Demonstração:**")
    st.info("Tente agendar uma consulta antes das 08:00 ou depois das 18:00 na aba 'Gerenciar Consultas' e veja o trigger em ação!")
    
    # Trigger 2
    st.markdown("---")
    st.subheader("📝 Trigger 2: Auditoria Automática")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>trg_auditoria_consulta</h4>
            <p><strong>Tipo:</strong> AFTER INSERT</p>
            <p><strong>Tabela:</strong> consulta</p>
            <p><strong>Função:</strong> Registra automaticamente cada nova consulta na tabela log_auditoria</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.code("""
DELIMITER $$
CREATE TRIGGER trg_auditoria_consulta
AFTER INSERT ON consulta
FOR EACH ROW
BEGIN
    INSERT INTO log_auditoria 
        (Mensagem, DataOcorrencia)
    VALUES (
        CONCAT('Nova consulta agendada. ID: ', 
               NEW.IdConsulta, 
               ' - Paciente: ', 
               NEW.CpfPaciente), 
        NOW()
    );
END$$
DELIMITER ;
        """, language="sql")
    
    st.markdown("**💡 Demonstração:**")
    st.info("Agende uma nova consulta e depois verifique a aba 'Logs de Auditoria' para ver o registro automático!")
    
    # Estatísticas dos triggers
    st.markdown("---")
    st.subheader("📊 Estatísticas de Triggers")
    
    try:
        con = conectar()
        cursor = con.cursor()
        
        # Consultas no horário comercial
        cursor.execute("""
            SELECT COUNT(*) FROM consulta 
            WHERE TIME(Data_Hora) BETWEEN '08:00:00' AND '18:00:00'
        """)
        consultas_validas = cursor.fetchone()[0]
        
        # Total de logs
        cursor.execute("SELECT COUNT(*) FROM log_auditoria")
        total_logs = cursor.fetchone()[0]
        
        # Total de consultas
        cursor.execute("SELECT COUNT(*) FROM consulta")
        total_consultas = cursor.fetchone()[0]
        
        cursor.close()
        con.close()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Consultas no Horário Comercial", consultas_validas, 
                   delta=f"{consultas_validas}/{total_consultas}")
        col2.metric("Logs de Auditoria Gerados", total_logs)
        col3.metric("Taxa de Auditoria", f"{(total_logs/max(total_consultas,1)*100):.0f}%")
        
        # Gráfico de distribuição horária
        st.subheader("🕐 Distribuição de Consultas por Horário")
        df_horarios = pd.read_sql("""
            SELECT 
                HOUR(Data_Hora) as hora,
                COUNT(*) as total
            FROM consulta
            GROUP BY HOUR(Data_Hora)
            ORDER BY hora
        """, conectar())
        
        if not df_horarios.empty:
            fig_horario = go.Figure()
            
            # Adicionar barras com cores diferentes para dentro/fora do horário comercial
            cores = ['#ff6b6b' if h < 8 or h > 18 else '#51cf66' for h in df_horarios['hora']]
            
            fig_horario.add_trace(go.Bar(
                x=df_horarios['hora'],
                y=df_horarios['total'],
                marker_color=cores,
                text=df_horarios['total'],
                textposition='outside'
            ))
            
            # Linhas de referência
            fig_horario.add_vline(x=8, line_dash="dash", line_color="green", 
                                 annotation_text="Início (08:00)")
            fig_horario.add_vline(x=18, line_dash="dash", line_color="red", 
                                 annotation_text="Fim (18:00)")
            
            fig_horario.update_layout(
                xaxis_title="Hora do Dia",
                yaxis_title="Número de Consultas",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_horario, use_container_width=True)
            
            st.caption("🟢 Verde: Dentro do horário comercial (08:00-18:00) | 🔴 Vermelho: Fora do horário comercial")
        
    except mysql.connector.Error as err:
        st.error(f"Erro ao carregar estatísticas: {err}")
    
    # Informações adicionais
    st.markdown("---")
    st.subheader("ℹ️ Informações Adicionais")
    
    with st.expander("📚 O que são Triggers?"):
        st.markdown("""
        **Triggers (Gatilhos)** são procedimentos armazenados no banco de dados que são executados automaticamente 
        quando eventos específicos ocorrem em uma tabela.
        
        **Tipos de Triggers:**
        - **BEFORE INSERT/UPDATE/DELETE:** Executado antes da operação
        - **AFTER INSERT/UPDATE/DELETE:** Executado após a operação
        
        **Vantagens:**
        - ✅ Automatização de tarefas
        - ✅ Validação de dados
        - ✅ Auditoria automática
        - ✅ Manutenção da integridade de dados
        """)
    
    with st.expander("🔧 Como testar os Triggers?"):
        st.markdown("""
        **Teste do Trigger de Horário:**
        1. Vá para 'Gerenciar Consultas'
        2. Tente agendar uma consulta às 07:00 ou 19:00
        3. O sistema bloqueará a operação com uma mensagem de erro
        
        **Teste do Trigger de Auditoria:**
        1. Vá para 'Gerenciar Consultas'
        2. Agende uma consulta em horário válido
        3. Verifique 'Logs de Auditoria' - um novo registro foi criado automaticamente
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Sistema de Consultas Médicas v2.0 | Desenvolvido com Streamlit & MySQL | 
    Triggers Ativos: trg_horario_comercial, trg_auditoria_consulta
</div>
""", unsafe_allow_html=True)
