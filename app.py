import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

# Configuração da API via Secrets (puxa da configuração do servidor)
try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro ao configurar a API. Verifique o seu st.secrets no painel do Streamlit.")
    st.stop()

st.title("🤖 Portal IA: Diagnóstico, Relacionamento e Performance")

# --- CRIAÇÃO DAS 3 ABAS ---
aba_suporte, aba_relacionamento, aba_performance = st.tabs(["🛠️ Suporte Técnico (Nível 1)", "🤝 Relacionamento (Nível 2)", "📊 Performance de Notas"])

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
    fotos_upload = st.file_uploader("Upload de Prints (Configurações/Erro)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    # Base de Conhecimento (Core)
    base_padrao = "[REGRAS FIXAS] 1. Lentidão Geral: Servidor min 12GB RAM. 2. Lentidão Isolada: Estação min 4GB RAM, .NET 4.8. 8. VPN/Wi-Fi: Causa degradação, mapear por IP."
    base_extra = ""
    if os.path.exists("regras.txt"):
        with open("regras.txt", "r", encoding="utf-8") as f:
            base_extra = "\n[REGRAS DINÂMICAS]\n" + f.read()
    
    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True):
        with st.spinner("Analisando..."):
            prompt = f"Você é especialista Prosoft. Base: {base_padrao + base_extra}. Analise o cenário: {escopo}, {conexao}, {banco}. Sintomas: {rotinas_comuns} {rotinas_extras}."
            conteudo = [prompt]
            if fotos_upload:
                for f in fotos_upload: conteudo.append(Image.open(f))
            try:
                resposta = model.generate_content(conteudo)
                st.info(resposta.text)
            except Exception as e:
                st.error(f"Erro: {e}")

# ==========================================
# ABA 2: RELACIONAMENTO (Transcrição)
# ==========================================
with aba_relacionamento:
    st.markdown("### 🗣️ Análise de Transcrição (Meet)")
    texto_transcricao = st.text_area("Cole a transcrição aqui:", height=300)
    
    if st.button("Gerar Dossiê Nível 2", type="primary", use_container_width=True):
        if texto_transcricao:
            prompt_relac = f"Analise esta transcrição de reunião e crie um dossiê técnico para o Nível 2: {texto_transcricao}"
            resposta = model.generate_content(prompt_relac)
            st.info(resposta.text)

# ==========================================
# ABA 3: PERFORMANCE DE NOTAS
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Performance")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Quantidade de Notas", min_value=1)
    tempo = c2.number_input("Tempo Total (Segundos)", min_value=0.1)
    
    if st.button("Analisar Eficiência", type="primary"):
        prompt_perf = f"Analise a performance: {qtd} notas em {tempo} segundos."
        resposta = model.generate_content(prompt_perf)
        st.info(resposta.text)
