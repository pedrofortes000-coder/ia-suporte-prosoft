import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial (Correção do comando de configuração)
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

# --- BARRA LATERAL (CONFIGURAÇÃO) ---
with st.sidebar:
    st.header("⚙️ Configuração")
    chave_inserida = st.text_input("Chave de API", type="password", placeholder="AIzaSy...")

if not chave_inserida:
    st.title("🤖 Portal IA: Diagnóstico e Relacionamento")
    st.warning("👈 Insira a Chave de API na barra lateral para habilitar o sistema.")
    st.stop()

genai.configure(api_key=chave_inserida.strip())
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🤖 Portal IA: Diagnóstico, Relacionamento e Performance")

# --- CRIAÇÃO DAS 3 ABAS (Definição correta aqui) ---
aba_suporte, aba_relacionamento, aba_performance = st.tabs(["🛠️ Suporte Técnico", "🤝 Relacionamento", "📊 Performance de Notas"])

# ==========================================
# ABA 1: SUPORTE TÉCNICO (Nível 1)
# ==========================================
with aba_suporte:
    st.markdown("### 🗄️ Dados do Ambiente")
    col1, col2 = st.columns(2)
    with col1:
        escopo = st.selectbox("Escopo da Lentidão", ["Selecione...", "Geral (Todos os usuários)", "Máquina Isolada", "Rotina Específica"], key="escopo")
        banco = st.selectbox("Versão do Banco de Dados", ["Selecione...", "Pervasive Workgroup v11", "Pervasive Workgroup v13 / v15", "Pervasive Server", "Microsoft SQL Server"], key="banco")
    with col2:
        conexao = st.multiselect("Tipo de Conexão", ["Rede Local", "Terminal Service (TS)", "Wi-Fi", "VPN"])
        usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)
    
    st.divider()
    st.markdown("### ⏱️ Sintomas")
    col3, col4 = st.columns(2)
    with col3:
        rotinas_comuns = st.multiselect("Rotinas Afetadas", ["Abertura inicial do Prosoft", "Inclusão e Gravação de Cadastros", "Folha de Pagamento", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])
        rotinas_extras = st.text_input("Outras Rotinas (separar por vírgula)")
    with col4:
        tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")
    
    st.divider()
    fotos_upload = st.file_uploader("Upload de Prints", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True):
        st.success("Análise de suporte técnico processada!") 
        # (Aqui entra o seu bloco de lógica de suporte que já funcionava)

# ==========================================
# ABA 2: RELACIONAMENTO (Nível 2)
# ==========================================
with aba_relacionamento:
    st.markdown("### 🗣️ Análise de Transcrição de Reunião (Meet)")
    texto_transcricao = st.text_area("Transcrição Bruta", height=300)
    
    if st.button("Gerar Dossiê para Nível 2", type="primary", use_container_width=True):
        if texto_transcricao.strip() == "":
            st.warning("⚠️ Cole a transcrição.")
        else:
            with st.spinner("Lendo transcrição..."):
                prompt = "Analise esta transcrição..." # Seu prompt aqui
                try:
                    resposta = model.generate_content(prompt)
                    st.markdown("### 📋 Dossiê")
                    st.info(resposta.text)
                except Exception as e:
                    st.error(f"Erro: {e}")

# ==========================================
# ABA 3: PERFORMANCE DE NOTAS
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Eficiência")
    col_a, col_b = st.columns(2)
    with col_a:
        qtd_notas = st.number_input("Quantidade de Notas", min_value=1, step=1)
    with col_b:
        tempo_total = st.number_input("Tempo Total (Segundos)", min_value=0.1, step=0.5, format="%.1f")
    
    if tempo_total > 0:
        notas_por_segundo = qtd_notas / tempo_total
        st.metric("Notas por Segundo", f"{notas_por_segundo:.2f} n/s")
    
    if st.button("Analisar Eficiência", type="primary"):
        st.info("Diagnóstico de performance gerado.")
