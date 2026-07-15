import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# Configuração inicial da página (Layout wide para aproveitar melhor a tela com as abas)
st.set_page_config(page_title="Portal IA: Prosoft", page_icon="🤖", layout="wide")

st.title("🤖 Portal IA: Diagnóstico e Relacionamento")
st.markdown("Selecione o módulo de atendimento abaixo:")

# Configuração da API
try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
except KeyError:
    st.error("Chave de API não configurada. Configure os Secrets no painel do Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-2.5-flash')

# --- CRIAÇÃO DAS ABAS ---
aba_suporte, aba_relacionamento = st.tabs(["🛠️ Suporte Técnico (Nível 1)", "🤝 Relacionamento (Transcrição)"])

# ==========================================
# ABA 1: SUPORTE TÉCNICO (O QUE JÁ FIZEMOS)
# ==========================================
with aba_suporte:
    st.markdown("### 🗄️ Dados do Ambiente")
    col1, col2 = st.columns(2)

    with col1:
        escopo = st.selectbox("Escopo da Lentidão", ["Selecione...", "Geral (Todos os usuários)", "Máquina Isolada", "Rotina Específica"], key="escopo")
        banco = st.selectbox("Versão do Banco de Dados", ["Selecione...", "Pervasive Workgroup v11", "Pervasive Workgroup v13 / v15", "Pervasive Server", "Microsoft SQL Server"], key="banco")

    with col2:
        conexao = st.multiselect("Tipo de Conexão (Pode escolher várias)", ["Rede Local", "Terminal Service (TS)", "Wi-Fi", "VPN"])
        usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)

    st.divider()

    st.markdown("### ⏱️ Sintomas")
    col3, col4 = st.columns(2)

    with col3:
        rotinas_comuns = st.multiselect("Rotinas Afetadas (Selecione uma ou mais)", ["Abertura inicial do Prosoft", "Inclusão e Gravação de Cadastros", "Folha de Pagamento", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])
        rotinas_extras = st.text_input("Outras Rotinas (Se não estiver na lista, digite separando por vírgula)")

    with col4:
        tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")

    st.divider()

    st.markdown("### 📝 Contexto Adicional")
    detalhes = st.text_area("Observações ou mensagens de erro (Opcional)", placeholder="Digite qualquer detalhe extra relatado pelo cliente...", key="detalhes_n1")
    fotos_upload = st.file_uploader("Upload de Prints das Configurações ou Erros", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    st.divider()

    st.markdown("### 🩺 Triagem Rápida")
    col5, col6 = st.columns(2)

    with col5:
        uptime_reboot = st.toggle("Servidor reiniciado recentemente?")
    with col6:
        antivirus_ok = st.toggle("Exceções do antivírus estão configuradas?")

    st.text("")

    # Leitura Combinada (Core + Atualizações)
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

    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True, key="btn_n1"):
        if escopo == "Selecione..." or banco == "Selecione..." or len(conexao) == 0 or (len(rotinas_comuns) == 0 and rotinas_extras.strip() == ""):
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios em 'Dados do Ambiente' e 'Sintomas'.")
        else:
            with st.spinner("Analisando padrões e avaliando múltiplas evidências..."):
                reboot_texto = "Sim" if uptime_reboot else "Não"
                antivirus_texto = "Sim" if antivirus_ok else "Não"
                contexto_extra = detalhes if detalhes.strip() != "" else "Nenhum detalhe adicional."
                
                conexao_texto = ", ".join(conexao)
                rotinas_texto = ", ".join(rotinas_comuns)
                if rotinas_extras.strip() != "":
                    rotinas_texto += f", {rotinas_extras}"

                prompt_gerado = f"""
                Você é um Especialista de Suporte Nível 3 focado no sistema Prosoft.
                Sua base de conhecimento completa: {base_conhecimento_completa}
                
                Cenário relatado:
                - Escopo: {escopo} | Conexões: {conexao_texto} | Banco: {banco} | Usuários: {usuarios}
                - Rotinas Afetadas: {rotinas_texto} | Tempo: {tempo_resposta}s
                - Reboot? {reboot_texto} | Antivírus ok? {antivirus_texto}
                - Contexto Extra: {contexto_extra}
                
                Instrução Especial: Analise imagens anexadas como evidências. Priorize regras dinâmicas em caso de conflito. 
                REGRAS DE ESTILO: Escreva a resposta de forma natural e direta. É ESTRITAMENTE PROIBIDO citar os números ou os nomes das regras no texto.
                
                Forneça:
                1. Diagnóstico do provável motivo.
                2. Plano de ação para o Nível 1.
                """
                try:
                    conteudo_final = [prompt_gerado]
                    if fotos_upload:
                        for foto in fotos_upload:
                            conteudo_final.append(Image.open(foto))
                    resposta = model.generate_content(conteudo_final)
                    st.success("Diagnóstico concluído!")
                    st.markdown("### 🤖 Parecer do Especialista")
                    st.info(resposta.text)
                except Exception as e:
                    st.error(f"Erro: {e}")


# ==========================================
# ABA 2: RELACIONAMENTO (NOVO MÓDULO)
# ==========================================
with aba_relacionamento:
    st.markdown("### 🗣️ Análise de Transcrição de Reunião (Meet)")
    st.markdown("Cole abaixo a transcrição da reunião com o cliente para gerar o Dossiê de Escalonamento para o Nível 2.")
    
    texto_transcricao = st.text_area("Transcrição Bruta", height=300, placeholder="Ex: [00:00] João: A folha de pagamento travou de novo ontem. [00:05] Maria: Sim, e estamos perdendo muito tempo com isso...")
    
    st.divider()
    
    if st.button("Gerar Dossiê para Nível 2", type="primary", use_container_width=True, key="btn_n2"):
        if texto_transcricao.strip() == "":
            st.warning("⚠️ Cole o texto da transcrição antes de analisar.")
        else:
            with st.spinner("Lendo transcrição e extraindo dores do cliente..."):
                prompt_relacionamento = f"""
                Você é um Especialista de Customer Success Senior e um Analista de Escalonamento de Nível 2.
                Sua tarefa é ler a transcrição bruta de uma reunião (Google Meet) entre a nossa equipe de relacionamento e o cliente. 
                
                Você deve ignorar conversas paralelas, cumprimentos e focos fora do produto. Extraia os problemas reais do sistema (Prosoft/Alterdata) e formate um Dossiê Técnico e Comportamental claro e objetivo para a equipe de Nível 2 assumir o caso.
                
                Transcrição da reunião:
                "{texto_transcricao}"
                
                Apresente o seu relatório ESTRITAMENTE nesta estrutura:
                
                **1. Resumo Executivo**
                (Um parágrafo resumindo o clima da reunião e o impacto geral relatado).
                
                **2. Principais Dores (Pain Points)**
                (Em bullet points, liste os problemas técnicos ou de processo exatos que o cliente relatou).
                
                **3. Impacto no Negócio**
                (Como esses problemas estão afetando o dinheiro, o tempo ou a rotina do cliente).
                
                **4. Encaminhamento Técnico (Ação para o N2)**
                (Com base nas dores relatadas, indique de forma direta o que os analistas de Nível 2 precisam investigar no banco de dados, infraestrutura ou rotina específica do sistema assim que assumirem o chamado).
                """
                
                try:
                    resposta_relacionamento = model.generate_content(prompt_relacionamento)
                    st.success("Dossiê gerado com sucesso!")
                    st.markdown("### 📋 Dossiê de Escalonamento (N2)")
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
                    st.info(resposta_relacionamento.text)
                except Exception as e:
                    st.error(f"Erro ao conectar com a IA: {e}")
