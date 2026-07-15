import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

# Configuração da API
try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro na configuração. Verifique os Secrets.")
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

# ... [As abas anteriores permanecem iguais ao código anterior] ...

# ==========================================
# ABA 5: AUDITORIA (NOVO MÓDULO)
# ==========================================
with aba_auditoria:
    st.markdown("### ⚖️ Auditoria de Atendimentos N2 (Validação 16/07/2026)")
    st.markdown("Cole o histórico do parecer e anexe prints das evidências (E-mails, Jira, Logs).")
    
    parecer_auditoria = st.text_area("Histórico do Parecer/Atendimento:", height=300, placeholder="Cole aqui o texto completo do parecer...")
    fotos_auditoria = st.file_uploader("Evidências (Prints de e-mail, Jira, etc):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Executar Auditoria Rigorosa", type="primary", use_container_width=True):
        if not parecer_auditoria:
            st.warning("⚠️ Cole o histórico do parecer.")
        else:
            with st.spinner("Auditorando atendimentos..."):
                prompt_auditor = f"""
                Você é um Auditor de Qualidade Sênior da Prosoft. Sua missão é auditar o atendimento de Nível 2 abaixo.
                
                REGRA DE OURO: A avaliação é feita EXCLUSIVAMENTE pelo que está registrado no texto e nas imagens anexadas. O que não estiver explícito no parecer ou nas imagens NÃO CONTA.
                
                Critérios de Auditoria (16/07/2026):
                1. Contato (Grave): 3 tentativas em dias/horários diferentes.
                2. Registro (Leve): Ações registradas com intervalo máx de 2 dias úteis.
                3. Vínculo MAN/PDP (Leve): Deve constar código (MAN, PDP, ANR, etc) e link do Jira.
                4. Divulgação da MAN/PDP (Grave): E-mail com supervisão em cópia e assunto "Criado projeto no Jira: [CODIGO] - [ASSUNTO]".
                5. Notificação ao cliente (Grave): Informar cliente sobre análise do Dev.
                6. Justificativa de CR/Artigo (Leve): Referenciar base (ID/Link). Artigo A124 para procedimentos internos.
                7. Contato agendado (Grave): Cumprir data.
                8. Contato p/ finalizar (Grave): Confirmar solução com cliente (pref. telefone).
                9. Erros gramaticais (Leve): Comprometimento da compreensão/postura.
                10. Campo Produto (Leve): Preenchimento correto.
                11. LGPD (Grave): Texto padrão registrado.
                12. Controle diretório (Leve): Caminho/Link da base salva.
                13. Tipo 1882 (Leve): Respostas coerentes ao script obrigatório.

                Analise o parecer e as imagens e gere:
                - Tabela: [Regra] | [Status: Passou/Falhou] | [Severidade: Grave/Leve] | [Motivo/Evidência]
                - Veredito Final: [ATENDIMENTO VÁLIDO] ou [ATENDIMENTO PENALIZADO].
                - Se Penalizado, liste o que causou a penalidade.
                
                Texto do Parecer:
                {parecer_auditoria}
                """
                
                conteudo = [prompt_auditor]
                if fotos_auditoria:
                    for f in fotos_auditoria: conteudo.append(Image.open(f))
                
                try:
                    resposta = model.generate_content(conteudo)
                    st.markdown("### 📋 Relatório de Auditoria")
                    st.info(resposta.text)
                except Exception as e:
                    st.error(f"Erro na auditoria: {e}")

# (Certifique-se de manter o conteúdo das outras abas abaixo disso)
