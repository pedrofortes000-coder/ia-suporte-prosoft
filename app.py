import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial
st.set_config = st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

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

# --- CRIAÇÃO DAS 3 ABAS ---
aba_suporte, aba_relacionamento, aba_performance = st.tabs(["🛠️ Suporte Técnico", "🤝 Relacionamento", "📊 Performance de Notas"])

# ==========================================
# ABA 1: SUPORTE TÉCNICO (Nível 1)
# ==========================================
with aba_suporte:
    # ... (código anterior da aba suporte permanece o mesmo) ...
    st.info("Módulo de Suporte Técnico ativo.")

# ==========================================
# ABA 2: RELACIONAMENTO (Nível 2)
# ==========================================
with aba_relacionamento:
    # ... (código anterior da aba relacionamento permanece o mesmo) ...
    st.info("Módulo de Relacionamento ativo.")

# ==========================================
# ABA 3: PERFORMANCE DE NOTAS (NOVO MÓDULO)
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Eficiência de Importação")
    
    col_a, col_b = st.columns(2)
    with col_a:
        qtd_notas = st.number_input("Quantidade de Notas Importadas", min_value=1, step=1)
    with col_b:
        tempo_total = st.number_input("Tempo Total de Processamento (Segundos)", min_value=0.1, step=0.5, format="%.1f")
    
    # Cálculos
    notas_por_segundo = qtd_notas / tempo_total
    tempo_medio_nota = tempo_total / qtd_notas
    
    # Exibição visual dos KPIs
    col_kpi1, col_kpi2 = st.columns(2)
    col_kpi1.metric("Notas por Segundo", f"{notas_por_segundo:.2f} n/s")
    col_kpi2.metric("Tempo Médio por Nota", f"{tempo_medio_nota:.2f} s")
    
    st.divider()
    
    if st.button("Analisar Eficiência de Processamento", type="primary", use_container_width=True):
        with st.spinner("Analisando eficiência..."):
            prompt_perf = f"""
            Você é um especialista em performance de banco de dados Prosoft.
            O usuário processou {qtd_notas} notas fiscais em {tempo_total} segundos.
            O resultado foi de {notas_por_segundo:.2f} notas/segundo.
            
            Analise: Essa performance é considerada saudável ou indica gargalo?
            Lembre-se: Processamentos abaixo de 1 nota/segundo geralmente indicam gargalo de rede ou disco (Pervasive).
            
            Forneça:
            1. Diagnóstico de performance.
            2. Lista de verificação para otimizar a velocidade (ex: fragmentação de disco, tamanho da memória, ou necessidade de migração para SQL Server).
            """
            
            try:
                resposta = model.generate_content(prompt_perf)
                st.markdown("### 🤖 Diagnóstico de Performance")
                st.info(resposta.text)
            except Exception as e:
                st.error(f"Erro: {e}")
