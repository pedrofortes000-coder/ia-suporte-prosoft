import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial da página
st.set_page_config(page_title="Diagnóstico IA: Prosoft", page_icon="🤖", layout="centered")

st.title("🤖 Diagnóstico IA: Lentidão no Sistema")
st.markdown("Preencha os dados abaixo para cruzar o cenário do cliente com a base de conhecimento.")

# Configuração da API
try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
except KeyError:
    st.error("Chave de API não configurada. Configure os Secrets no painel do Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-2.5-flash')

# Bloco 1: Dados do Ambiente
st.markdown("### 🗄️ Dados do Ambiente")
col1, col2 = st.columns(2)

with col1:
    escopo = st.selectbox("Escopo da Lentidão", ["Selecione...", "Geral (Todos os usuários)", "Máquina Isolada", "Rotina Específica"])
    banco = st.selectbox("Versão do Banco de Dados", ["Selecione...", "Pervasive Workgroup v11", "Pervasive Workgroup v13 / v15", "Pervasive Server", "Microsoft SQL Server"])

with col2:
    conexao = st.multiselect("Tipo de Conexão (Pode escolher várias)", ["Rede Local", "Terminal Service (TS)", "Wi-Fi", "VPN"])
    usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)

st.divider()

# Bloco 2: Sintomas
st.markdown("### ⏱️ Sintomas")
col3, col4 = st.columns(2)

with col3:
    rotinas_comuns = st.multiselect("Rotinas Afetadas (Selecione uma ou mais)", ["Abertura inicial do Prosoft", "Inclusão e Gravação de Cadastros", "Folha de Pagamento", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])
    rotinas_extras = st.text_input("Outras Rotinas (Se não estiver na lista, digite separando por vírgula)")

with col4:
    tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")

st.divider()

# Bloco 3: Detalhes e Anexos
st.markdown("### 📝 Contexto Adicional")
detalhes = st.text_area("Observações ou mensagens de erro (Opcional)", placeholder="Digite qualquer detalhe extra relatado pelo cliente...")

fotos_upload = st.file_uploader("Upload de Prints das Configurações ou Erros (Pode selecionar vários arquivos)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

st.divider()

# Bloco 4: Triagem Rápida
st.markdown("### 🩺 Triagem Rápida")
col5, col6 = st.columns(2)

with col5:
    uptime_reboot = st.toggle("Servidor reiniciado recentemente?")
with col6:
    antivirus_ok = st.toggle("Exceções do antivírus estão configuradas?")

st.text("")

# --- SISTEMA DE LEITURA COMBINADA (CORE + ATUALIZAÇÕES) ---

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

base_extra = ""
if os.path.exists("regras.txt"):
    with open("regras.txt", "r", encoding="utf-8") as f:
        base_extra = "\n[REGRAS DINÂMICAS DA EQUIPE]\n" + f.read()

base_conhecimento_completa = base_padrao + base_extra

# Botão de Ação
if st.button("Analisar com Inteligência Artificial", type="primary", use_container_width=True):
    if escopo == "Selecione..." or banco == "Selecione..." or len(conexao) == 0 or (len(rotinas_comuns) == 0 and rotinas_extras.strip() == ""):
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios (selecione pelo menos uma Conexão e uma Rotina).")
    else:
        with st.spinner("Analisando padrões e avaliando múltiplas evidências..."):
            reboot_texto = "Sim" if uptime_reboot else "Não"
            antivirus_texto = "Sim" if antivirus_ok else "Não"
            contexto_extra = detalhes if detalhes.strip() != "" else "Nenhum detalhe adicional informado."
            
            conexao_texto = ", ".join(conexao)
            rotinas_texto = ", ".join(rotinas_comuns)
            if rotinas_extras.strip() != "":
                rotinas_texto += f", {rotinas_extras}"

            prompt_gerado = f"""
            Você é um Especialista de Suporte Nível 3 focado no sistema Prosoft.
            Sua base de conhecimento completa (Core + Atualizações):
            {base_conhecimento_completa}
            
            Cenário atual relatado:
            - Escopo: {escopo} | Conexões Envolvidas: {conexao_texto} | Banco: {banco} | Usuários: {usuarios}
            - Rotinas Afetadas: {rotinas_texto} | Tempo: {tempo_resposta}s
            - Reboot? {reboot_texto} | Antivírus ok? {antivirus_texto}
            - Contexto Extra: {contexto_extra}
            
            Instrução Especial: Se houverem imagens anexadas, analise TODAS como um conjunto de evidências para o diagnóstico. Priorize as regras dinâmicas em caso de conflito. 
            REGRAS DE ESTILO: Escreva a resposta de forma natural e direta. É ESTRITAMENTE PROIBIDO citar os números ou os nomes das regras no texto (ex: NUNCA escreva "conforme a Regra 8" ou "(Regra Fixa 5)"). Apenas aplique o conhecimento na sua explicação.
            
            Com base EXCLUSIVAMENTE nas regras, nos dados e nas imagens (se fornecidas), forneça:
            1. Diagnóstico do provável motivo.
            2. Plano de ação para o Nível 1.
            """
            
            try:
                conteudo_final = [prompt_gerado]
                if fotos_upload:
                    for foto in fotos_upload:
                        img_aberta = Image.open(foto)
                        conteudo_final.append(img_aberta)

                resposta = model.generate_content(conteudo_final)
                st.success("Diagnóstico concluído com sucesso!")
                st.markdown("### 🤖 Parecer do Especialista (IA)")
                st.info(resposta.text)
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")
