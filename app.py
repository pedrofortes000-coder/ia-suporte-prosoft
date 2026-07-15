import streamlit as st
import google.generativeai as genai

# Configuração inicial da página
st.set_page_config(page_title="Diagnóstico IA: Prosoft", page_icon="🤖", layout="centered")

st.title("🤖 Diagnóstico IA: Lentidão no Sistema")
st.markdown("Preencha os dados abaixo para cruzar o cenário do cliente com a base de conhecimento.")

# Configuração da API puxando da variável segura da nuvem
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("Chave de API não configurada. Configure os Secrets no painel do Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-pro')

# Bloco 1: Dados do Ambiente
st.markdown("### 🗄️ Dados do Ambiente")
col1, col2 = st.columns(2)

with col1:
    escopo = st.selectbox("Escopo da Lentidão", ["Selecione...", "Geral (Todos os usuários)", "Máquina Isolada", "Rotina Específica"])
    banco = st.selectbox("Versão do Banco de Dados", ["Selecione...", "Pervasive Workgroup v11", "Pervasive Workgroup v13 / v15", "Pervasive Server", "Microsoft SQL Server"])

with col2:
    conexao = st.selectbox("Tipo de Conexão", ["Selecione...", "Rede Local", "Terminal Service (TS)", "Wi-Fi", "VPN"])
    usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)

st.divider()

# Bloco 2: Sintomas
st.markdown("### ⏱️ Sintomas")
col3, col4 = st.columns(2)

with col3:
    rotina = st.selectbox("Rotina Afetada", ["Selecione...", "Abertura inicial do Prosoft", "Inclusão e Gravação de Cadastros", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])

with col4:
    tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")

st.divider()

# Bloco 3: Triagem Rápida
st.markdown("### 🩺 Triagem Rápida")
col5, col6 = st.columns(2)

with col5:
    uptime_reboot = st.toggle("Servidor reiniciado recentemente?")
with col6:
    antivirus_ok = st.toggle("Exceções do antivírus estão configuradas?")

st.text("")

# Base de Conhecimento Embutida (Sem precisar de txt)
base_conhecimento = """
1. Lentidão Generalizada: Servidor mínimo de 12GB e processador de 2GHz x64. Rede mínimo 10Mb/s (recomendado 1Gb/s).
2. Lentidão Isolada: Estação local com 4GB de RAM, Win PRO/ENTERPRISE, .NET 4.8 e Java 8.
3. Comunicação Externa: "Prosoft Serviço de Integração" atualizado, internet min 4Mb/s, portas 80/8080 liberadas.
4. Esgotamento de Memória: Para TS (Terminal Service), 8GB RAM base + 1GB por usuário. Reiniciar servidor libera memória presa.
5. Limite Pervasive: Workgroup 11 (max 10 usuários). Workgroup 13/15 (max 35 usuários). Server (max 500 usuários).
6. Antivírus: Leitura constante de pastas causa lentidão severa. Exigir exceções.
7. Reinf/eSocial: Liberar porta 5984 (CouchDB) e 1433/1434 (SQL Server).
8. Rede e VPN: Uso de Wi-Fi ou VPN causa degradação; mapear estação por IP reduz lentidão.
"""

# Botão de Ação
if st.button("Analisar com Inteligência Artificial", type="primary", use_container_width=True):
    if escopo == "Selecione..." or banco == "Selecione..." or conexao == "Selecione..." or rotina == "Selecione...":
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        with st.spinner("Analisando padrões..."):
            reboot_texto = "Sim" if uptime_reboot else "Não"
            antivirus_texto = "Sim" if antivirus_ok else "Não"

            prompt_gerado = f"""
            Você é um Especialista de Suporte Nível 3 focado no sistema Prosoft.
            Regras de negócio:
            {base_conhecimento}
            
            Cenário atual relatado:
            - Escopo: {escopo} | Conexão: {conexao} | Banco: {banco} | Usuários: {usuarios}
            - Rotina: {rotina} | Tempo: {tempo_resposta}s
            - Reboot? {reboot_texto} | Antivírus ok? {antivirus_texto}
            
            Com base EXCLUSIVAMENTE nas regras, forneça:
            1. Diagnóstico do provável motivo.
            2. Plano de ação para o Nível 1.
            """
            
            try:
                resposta = model.generate_content(prompt_gerado)
                st.success("Diagnóstico concluído com sucesso!")
                st.markdown("### 🤖 Parecer do Especialista (IA)")
                st.info(resposta.text)
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")
