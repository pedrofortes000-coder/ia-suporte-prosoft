import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# --- CONFIGURAÇÃO E SEGURANÇA ---
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro ao configurar a API. Verifique o seu st.secrets no painel do Streamlit.")
    st.stop()

st.title("🤖 Portal IA: Diagnóstico, Relacionamento, Performance e Auditoria")

# --- CRIAÇÃO DAS 5 ABAS ---
aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2, aba_auditoria = st.tabs([
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno N2",
    "⚖️ Auditoria"
])

# ==========================================
# ABA 1: SUPORTE TÉCNICO (N1)
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
    fotos_upload = st.file_uploader("Upload de Prints (Configurações/Erro)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True):
        with st.spinner("Analisando..."):
            base_extra = ""
            if os.path.exists("regras.txt"):
                with open("regras.txt", "r", encoding="utf-8") as f:
                    base_extra = "\n[REGRAS DINÂMICAS]\n" + f.read()
            
            prompt = f"Você é especialista Prosoft. Analise: {escopo}, {conexao}, {banco}. Base Extra: {base_extra}"
            conteudo = [prompt]
            if fotos_upload:
                for f in fotos_upload: conteudo.append(Image.open(f))
            
            resposta = model.generate_content(conteudo)
            st.code(resposta.text, language="markdown")
            st.download_button("💾 Baixar Diagnóstico (TXT)", resposta.text, "diagnostico_n1.txt", use_container_width=True)

# ==========================================
# ABA 2: RELACIONAMENTO (N2 - Dossiê)
# ==========================================
with aba_relacionamento:
    st.markdown("### 🗣️ Análise de Transcrição (Meet)")
    texto_transcricao = st.text_area("Cole a transcrição aqui:", height=300)
    
    if st.button("Gerar Dossiê para Nível 2", type="primary", use_container_width=True):
        if texto_transcricao:
            resposta = model.generate_content(f"Analise esta transcrição de reunião e crie um dossiê técnico: {texto_transcricao}")
            st.code(resposta.text, language="markdown")
            st.download_button("💾 Baixar Dossiê (TXT)", resposta.text, "dossie_n2.txt", use_container_width=True)

# ==========================================
# ABA 3: PERFORMANCE
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Performance")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Quantidade de Notas", min_value=1)
    tempo = c2.number_input("Tempo Total (Segundos)", min_value=0.1)
    
    if st.button("Analisar Eficiência", type="primary"):
        resposta = model.generate_content(f"Analise a performance: {qtd} notas em {tempo} segundos.")
        st.code(resposta.text, language="markdown")
        st.download_button("💾 Baixar Laudo de Performance (TXT)", resposta.text, "performance.txt", use_container_width=True)

# ==========================================
# ABA 4: RETORNO NÍVEL 2 (FECHAMENTO)
# ==========================================
with aba_retorno_n2:
    st.markdown("### 🔄 Consolidação de Encerramento (Nível 2)")
    c_1, c_2 = st.columns(2)
    with c_1:
        descricao_tecnica = st.text_area("Procedimento Técnico:", height=200)
    with c_2:
        transcricao_feedback = st.text_area("Feedback do Cliente:", height=200)
    
    fotos_retorno = st.file_uploader("Evidências visuais (Prints/Logs):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Gerar Relatório Final", type="primary", use_container_width=True):
        prompt_fechamento = f"Crie um relatório de encerramento profissional com: {descricao_tecnica} e feedback: {transcricao_feedback}"
        conteudo_final = [prompt_fechamento]
        if fotos_retorno:
            for f in fotos_retorno: conteudo_final.append(Image.open(f))
        
        resposta = model.generate_content(conteudo_final)
        st.code(resposta.text, language="markdown")
        st.download_button("💾 Baixar Fechamento (TXT)", resposta.text, "encerramento_n2.txt", use_container_width=True)

# ==========================================
# ABA 5: AUDITORIA
# ==========================================
with aba_auditoria:
    st.markdown("### ⚖️ Auditoria de Atendimentos N2")
    parecer_auditoria = st.text_area("Histórico do Parecer/Atendimento:", height=300)
    fotos_auditoria = st.file_uploader("Evidências (Prints e-mail/Jira):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Executar Auditoria Rigorosa", type="primary", use_container_width=True):
        if parecer_auditoria:
            prompt_auditor = f"""
            Você é um Auditor de Qualidade Sênior da Prosoft.
            --- REGRAS ---
            1. Análise de Finalização: Se chamado encerrado por solução aplicada ou monitoramento do cliente, NÃO penalizar por contato.
            2. O que não está no parecer não conta.
            Analise: {parecer_auditoria}
            """
            conteudo = [prompt_auditor]
            if fotos_auditoria:
                for f in fotos_auditoria: conteudo.append(Image.open(f))
            
            resposta = model.generate_content(conteudo)
            st.code(resposta.text, language="markdown")
            st.download_button("💾 Baixar Laudo Auditoria (TXT)", resposta.text, "laudo_auditoria.txt", use_container_width=True)
