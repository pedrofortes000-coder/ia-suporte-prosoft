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

st.title("🤖 Portal IA: Diagnóstico, Relacionamento, Performance, Auditoria e Encerramento")

# --- CRIAÇÃO DAS 6 ABAS ---
aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2, aba_auditoria, aba_finalizacao = st.tabs([
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno N2",
    "⚖️ Auditoria",
    "✅ Finalização N2"
])

# ... (Mantenha as abas anteriores conforme o último código validado) ...

# ==========================================
# ABA 6: FINALIZAÇÃO N2 (NOVO MÓDULO)
# ==========================================
with aba_finalizacao:
    st.markdown("### ✅ Finalização Profissional de Chamado (Nível 2)")
    st.markdown("Preencha os campos abaixo para gerar um parecer técnico de encerramento padronizado.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        nome_cliente = st.text_input("Nome do Cliente:")
        telefone_contato = st.text_input("Telefone de Contato:")
    
    resolucao = st.text_area("Descrição Técnica da Resolução:", height=200, placeholder="Descreva o que foi feito para sanar a falha...")
    
    if st.button("Gerar Parecer de Encerramento", type="primary", use_container_width=True):
        if not nome_cliente or not resolucao:
            st.warning("⚠️ Preencha Nome do Cliente e Resolução.")
        else:
            with st.spinner("Estruturando parecer..."):
                prompt_finalizacao = f"""
                Você é um Analista de Suporte Sênior. Crie um parecer de finalização de chamado formal e técnico para o sistema Prosoft.
                Dados:
                - Cliente: {nome_cliente}
                - Telefone: {telefone_contato}
                - Resolução Técnica: {resolucao}
                
                Estruture em:
                1. Saudação ao cliente.
                2. Descrição técnica da solução (limpa e profissional).
                3. Informação sobre encerramento do ticket.
                4. Colocação à disposição para suporte adicional.
                """
                
                resposta = model.generate_content(prompt_finalizacao)
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Parecer Final (TXT)", resposta.text, "parecer_final.txt", use_container_width=True)
