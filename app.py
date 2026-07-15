import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Debug IA", layout="centered")
st.title("🔍 Rastreador de Modelos da API")

try:
    # Puxa a chave e limpa
    chave = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave)
    
    st.success("✅ Autenticação aceita! Buscando os modelos liberados para a sua chave específica...")
    
    # Lista todos os modelos que suportam geração de texto
    modelos = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Remove o prefixo "models/" para facilitar a cópia
            nome_limpo = m.name.replace("models/", "")
            modelos.append(nome_limpo)
    
    st.markdown("### 📋 Modelos Disponíveis:")
    st.write("Copie um dos nomes exatos desta lista para usarmos no código final:")
    st.json(modelos)
    
except KeyError:
    st.error("Chave de API não encontrada nos Secrets.")
except Exception as e:
    st.error(f"Erro ao conectar com a IA: {e}")
