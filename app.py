import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# --- CONFIGURAÇÃO E SEGURANÇA ---
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

try:
    # A chave deve estar configurada no painel do Streamlit (Secrets)
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro ao configurar a API. Verifique o seu st.secrets no painel do Streamlit.")
    st.stop()

st.title("🤖 Portal IA: Diagnóstico, Relacionamento e Performance")

# --- CRIAÇÃO DAS ABAS ---
aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2 = st.tabs([
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno Nível 2"
])

# --- BASE DE CONHECIMENTO (CORE) ---
base_padrao = """
[REGRAS FIXAS DE INFRAESTRUTURA]
1. Lentidão Generalizada: Servidor mínimo de 12GB e processador de 2GHz x64. Rede mínimo 10Mb/s (recomendado 1Gb/s).
2. Lentidão Isolada: Estação local com 4GB de RAM, Win PRO/ENTERPRISE, .NET 4.8 e Java 8.
3. Comunicação Externa: "Prosoft Serviço de Integração" atualizado, internet min 4Mb/s, portas 80/8080 liberadas.
4. Esgotamento de Memória: Para TS (Terminal Service), 8GB RAM base + 1GB por usuário. Reiniciar servidor libera memória presa.
5. Limite Pervasive: Workgroup 11 (max 10 usuários). Workgroup 13/15 (max 35 usuários). Server (max 500 usuários).
6. Antivírus: Leitura constante de pastas causa lentidão severa. Exigir exceções.
7. Reinf/eSocial: Liberar porta 5984 (CouchDB) e 1433/1434 (SQL Server).
8. Rede e VPN: Uso de Wi-Fi ou VPN causa degradação; mapear estação por IP reduz lentidão.
"""

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
    
    st.markdown("### ⏱️ Sintomas")
    col3, col4 = st.columns(2)
    with col3:
        rotinas_comuns = st.multiselect("Rotinas Afetadas", ["Abertura inicial do Prosoft", "Inclusão e Gravação de Cadastros", "Folha de Pagamento", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])
        rotinas_extras = st.text_input("Outras Rotinas (separar por vírgula)")
    with col4:
        tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")
    
    st.divider()
    fotos_upload = st.file_uploader("Upload de Prints (Configurações/Erro)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True):
        with st.spinner("Analisando..."):
            base_extra = ""
            if os.path.exists("regras.txt"):
                with open("regras.txt", "r", encoding="utf-8") as f:
                    base_extra = "\n[REGRAS DINÂMICAS]\n" + f.read()
            
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
# ABA 2: RELACIONAMENTO (N2 - Dossiê)
# ==========================================
with aba_relacionamento:
    st.markdown("### 🗣️ Análise de Transcrição (Meet)")
    texto_transcricao = st.text_area("Cole a transcrição aqui:", height=300)
    
    if st.button("Gerar Dossiê para Nível 2", type="primary", use_container_width=True):
        if texto_transcricao:
            with st.spinner("Extraindo dores do cliente..."):
                prompt_relac = f"Analise esta transcrição de reunião e crie um dossiê técnico para o Nível 2: {texto_transcricao}"
                resposta = model.generate_content(prompt_relac)
                st.info(resposta.text)

# ==========================================
# ABA 3: PERFORMANCE
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Performance")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Quantidade de Notas", min_value=1)
    tempo = c2.number_input("Tempo Total (Segundos)", min_value=0.1)
    
    if st.button("Analisar Eficiência", type="primary"):
        prompt_perf = f"Analise a performance: {qtd} notas em {tempo} segundos. É saudável?"
        resposta = model.generate_content(prompt_perf)
        st.info(resposta.text)

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
        with st.spinner("Consolidando..."):
            prompt_fechamento = f"Crie um relatório de encerramento profissional com: {descricao_tecnica} e feedback: {transcricao_feedback}"
            conteudo_final = [prompt_fechamento]
            if fotos_retorno:
                for f in fotos_retorno: conteudo_final.append(Image.open(f))
            
            resposta = model.generate_content(conteudo_final)
            st.info(resposta.text)
