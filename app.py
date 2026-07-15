import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

# Configuração da API via Secrets
try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro ao configurar a API. Verifique o seu st.secrets no painel do Streamlit.")
    st.stop()

st.title("🤖 Portal IA: Diagnóstico, Relacionamento e Performance")

# --- CRIAÇÃO DAS 4 ABAS ---
aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2 = st.tabs([
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno Nível 2"
])

# ==========================================
# ABA 4: RETORNO NÍVEL 2 (FECHAMENTO)
# ==========================================
with aba_retorno_n2:
    st.markdown("### 🔄 Consolidação de Encerramento (Nível 2)")
    st.markdown("Preencha o que foi executado tecnicamente e o feedback do cliente para gerar o relatório final de fechamento.")
    
    col_1, col_2 = st.columns(2)
    with col_1:
        descricao_tecnica = st.text_area("O que foi feito (Procedimento Técnico):", height=200, placeholder="Ex: Ajuste de permissão no Pervasive, migração de arquivo .BTR, liberação de porta...")
    with col_2:
        transcricao_feedback = st.text_area("Transcrição/Relato do Cliente (Feedback):", height=200, placeholder="Ex: O cliente confirmou que a lentidão parou e a folha processou em 30 segundos.")
    
    if st.button("Gerar Relatório Final de Encerramento", type="primary", use_container_width=True):
        if not descricao_tecnica or not transcricao_feedback:
            st.warning("⚠️ Preencha ambos os campos para gerar o relatório.")
        else:
            with st.spinner("Consolidando informações..."):
                prompt_fechamento = f"""
                Você é um Analista de Suporte Sênior. Sua tarefa é consolidar as informações do chamado em um único relatório de encerramento profissional.
                
                1. Procedimento Técnico Executado: {descricao_tecnica}
                2. Feedback/Transcrição do Cliente: {transcricao_feedback}
                
                Crie um texto único e profissional, pronto para ser enviado ao cliente ou colado no CRM/Sistema de Chamados, contendo:
                - Resumo da solução aplicada.
                - Confirmação de que o problema foi sanado (baseado no feedback).
                - Recomendação final ou alerta preventivo (se necessário).
                """
                
                try:
                    resposta = model.generate_content(prompt_fechamento)
                    st.success("Relatório de encerramento gerado!")
                    st.markdown("### 📝 Relatório Final para CRM/Cliente")
                    st.info(resposta.text)
                except Exception as e:
                    st.error(f"Erro ao gerar relatório: {e}")

# (As outras abas permanecem com o código que você já validou antes...)
with aba_suporte:
    st.info("Módulo Suporte N1 Ativo.")
    # ... seu código da aba suporte ...

with aba_relacionamento:
    st.info("Módulo Relacionamento Ativo.")
    # ... seu código da aba relacionamento ...

with aba_performance:
    st.info("Módulo Performance Ativo.")
    # ... seu código da aba performance ...
