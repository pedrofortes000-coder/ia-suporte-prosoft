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
    conexao = st.selectbox("Tipo de Conexão", ["Selecione...", "Rede Local", "Terminal Service (TS)", "Wi-Fi", "VPN"])
    usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)

st.divider()

# Bloco 2: Sintomas
st.markdown("### ⏱️ Sintomas")
col3, col4 = st.columns(2)

with col3:
    rotinas = st.text_input("Rotinas Afetadas (separe por vírgula)", placeholder="Ex: Abertura do Prosoft, Folha, eSocial")

with col4:
    tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")

st.divider()

# Bloco 3: Detalhes e Anexos
st.markdown("### 📝 Contexto Adicional")
detalhes = st.text_area("Observações ou mensagens de erro (Opcional)", placeholder="Digite qualquer detalhe extra relatado pelo cliente...")
foto_upload = st.file_uploader("Upload de Print das Configurações do Servidor/Máquina (Opcional)", type=["png", "jpg", "jpeg"])

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

# 1. Base Fixa (O Core do sistema)
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
9. Análise de Disco (CrystalDiskMark): Se o usuário anexar um print do CrystalDiskMark, analise os números de leitura (Read) e gravação (Write). 
- Gargalo Sequencial: Se o valor de "SEQ1M" estiver abaixo de 80 MB/s, o disco está muito lento para carregar o sistema e transferir arquivos grandes.
- Gargalo de Banco de Dados: Se o valor de "RND4K" estiver abaixo de 0.5 MB/s, o disco físico é o culpado pela lentidão nas rotinas do Prosoft (gravação de dados e relatórios). 
- Solução Nível 1: Se qualquer um desses gargalos for identificado na imagem, o diagnóstico deve apontar falha/esgotamento do disco físico e o plano de ação deve recomendar um teste de saúde do HD (SMART) ou o upgrade imediato para um SSD.
"""

# 2. Base Dinâmica (O arquivo TXT com as novidades da equipe)
base_extra = ""
if os.path.exists("regras.txt"):
    with open("regras.txt", "r", encoding="utf-8") as f:
        base_extra = "\n[REGRAS DINÂMICAS DA EQUIPE]\n" + f.read()

# 3. Junta tudo para a IA analisar
base_conhecimento_completa = base_padrao + base_extra

# Botão de Ação
if st.button("Analisar com Inteligência Artificial", type="primary", use_container_width=True):
    if escopo == "Selecione..." or banco == "Selecione..." or conexao == "Selecione..." or rotinas.strip() == "":
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios em 'Dados do Ambiente' e 'Sintomas'.")
    else:
        with st.spinner("Analisando padrões e anexos..."):
            reboot_texto = "Sim" if uptime_reboot else "Não"
            antivirus_texto = "Sim" if antivirus_ok else "Não"
            contexto_extra = detalhes if detalhes.strip() != "" else "Nenhum detalhe adicional informado."

            prompt_gerado = f"""
            Você é um Especialista de Suporte Nível 3 focado no sistema Prosoft.
            Sua base de conhecimento completa (Core + Atualizações):
            {base_conhecimento_completa}
            
            Cenário atual relatado:
            - Escopo: {escopo} | Conexão: {conexao} | Banco: {banco} | Usuários: {usuarios}
            - Rotinas: {rotinas} | Tempo: {tempo_resposta}s
            - Reboot? {reboot_texto} | Antivírus ok? {antivirus_texto}
            - Contexto Extra: {contexto_extra}
            
            Instrução Especial: Se houver uma imagem anexada, cruze os dados de Hardware mostrados nela com as regras da base. Use a regra que melhor solucione o problema principal relatado, priorizando regras dinâmicas se houver conflito.
            
            Com base EXCLUSIVAMENTE nas regras, nos dados e na imagem (se fornecida), forneça:
            1. Diagnóstico do provável motivo.
            2. Plano de ação para o Nível 1.
            """
            
            try:
                if foto_upload is not None:
                    img_aberta = Image.open(foto_upload)
                    conteudo_final = [prompt_gerado, img_aberta]
                else:
                    conteudo_final = prompt_gerado

                resposta = model.generate_content(conteudo_final)
                st.success("Diagnóstico concluído com sucesso!")
                st.markdown("### 🤖 Parecer do Especialista (IA)")
                st.info(resposta.text)
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: {e}")
