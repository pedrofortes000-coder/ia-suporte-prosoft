import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# --- CONFIGURAÇÃO E SEGURANÇA ---
st.set_page_config(page_title="QA Desk AI - Portal de Triagem", page_icon="🚀", layout="wide")

try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro ao configurar a API. Verifique o seu st.secrets no painel do Streamlit.")
    st.stop()

# --- VARIÁVEIS DE ESTADO (MEMÓRIA DO SISTEMA) ---
# Se for a primeira vez abrindo a página, cria as variáveis em branco ou com exemplos genéricos.
if 'nome_sistema' not in st.session_state:
    st.session_state['nome_sistema'] = "Software Exemplo"
if 'modulos_sistema' not in st.session_state:
    st.session_state['modulos_sistema'] = ["Módulo Cadastros", "Módulo Financeiro", "Módulo Relatórios", "Integrações"]
if 'regras_base' not in st.session_state:
    st.session_state['regras_base'] = "Insira as regras de infraestrutura e procedimentos padrão do seu sistema aqui."

st.title("🚀 QA Desk AI: Triagem e Auditoria Inteligente")

# --- CRIAÇÃO DAS 7 ABAS ---
aba_setup, aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2, aba_auditoria, aba_finalizacao = st.tabs([
    "⚙️ Setup (Admin)",
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno N2",
    "⚖️ Auditoria",
    "✅ Finalização"
])

# ==========================================
# ABA 0: SETUP DA EMPRESA (NOVO MÓDULO WHITE-LABEL)
# ==========================================
with aba_setup:
    st.markdown("### ⚙️ Configuração do Ambiente (White-label)")
    st.markdown("Personalize o portal para o seu software. A IA adotará a identidade e as regras configuradas aqui.")
    
    novo_nome = st.text_input("Nome do Sistema/Software:", value=st.session_state['nome_sistema'])
    
    st.markdown("Quais são as principais rotinas ou módulos do seu sistema? (Separe por vírgulas)")
    novos_modulos_str = st.text_input("Módulos do Sistema:", value=", ".join(st.session_state['modulos_sistema']))
    
    novas_regras = st.text_area("Base de Conhecimento (Regras de Infra e Negócio):", value=st.session_state['regras_base'], height=250)
    
    if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
        st.session_state['nome_sistema'] = novo_nome
        # Limpa espaços e transforma a string separada por vírgulas em uma lista
        st.session_state['modulos_sistema'] = [m.strip() for m in novos_modulos_str.split(",") if m.strip()]
        st.session_state['regras_base'] = novas_regras
        st.success(f"✅ Configurações salvas com sucesso! A IA agora atua como especialista em **{novo_nome}**.")

# ==========================================
# ABA 1: SUPORTE TÉCNICO (N1)
# ==========================================
with aba_suporte:
    st.markdown(f"### 🗄️ Dados do Ambiente ({st.session_state['nome_sistema']})")
    col1, col2 = st.columns(2)
    with col1:
        escopo = st.selectbox("Escopo do Problema", ["Selecione...", "Geral (Todos os usuários)", "Máquina Isolada", "Rotina Específica"], key="escopo")
        banco = st.selectbox("Versão do Banco de Dados", ["Selecione...", "PostgreSQL", "SQL Server", "MySQL", "Oracle", "Pervasive", "Outro"], key="banco")
    with col2:
        conexao = st.multiselect("Tipo de Conexão", ["Rede Local", "Nuvem/Cloud", "Terminal Service (TS)", "Wi-Fi", "VPN"])
        usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)
    
    st.divider()
    
    st.markdown("### ⏱️ Sintomas")
    col3, col4 = st.columns(2)
    with col3:
        # Aqui a mágica acontece: as opções vêm do Setup!
        rotinas_comuns = st.multiselect("Rotinas Afetadas", st.session_state['modulos_sistema'])
        rotinas_extras = st.text_input("Outras Rotinas (separar por vírgula)")
    with col4:
        tempo_resposta = st.number_input("Tempo de Resposta (Segundos) - Opcional", min_value=0.0, step=0.5, format="%.1f")
    
    st.divider()
    fotos_upload = st.file_uploader("Upload de Prints (Configurações/Erro)", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_n1")
    
    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True):
        with st.spinner("Analisando..."):
            prompt = f"Você é especialista de suporte técnico no sistema {st.session_state['nome_sistema']}. Base de regras: {st.session_state['regras_base']}. Analise o cenário: {escopo}, {conexao}, {banco}. Sintomas: {rotinas_comuns} {rotinas_extras}."
            conteudo = [prompt]
            if fotos_upload:
                for f in fotos_upload: conteudo.append(Image.open(f))
            try:
                resposta = model.generate_content(conteudo)
                st.success("✅ Diagnóstico concluído!")
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Diagnóstico (TXT)", resposta.text, "diagnostico_n1.txt", use_container_width=True)
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
                prompt_relac = f"Você atua no sistema {st.session_state['nome_sistema']}. Analise esta transcrição de reunião e crie um dossiê técnico para o Nível 2: {texto_transcricao}"
                resposta = model.generate_content(prompt_relac)
                st.success("✅ Dossiê gerado!")
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Dossiê (TXT)", resposta.text, "dossie_n2.txt", use_container_width=True)

# ==========================================
# ABA 3: PERFORMANCE
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Performance")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Quantidade de Registros/Notas", min_value=1)
    tempo = c2.number_input("Tempo Total (Segundos)", min_value=0.1)
    
    if st.button("Analisar Eficiência", type="primary"):
        with st.spinner("Analisando eficiência..."):
            prompt_perf = f"Analise a performance no sistema {st.session_state['nome_sistema']}: {qtd} registros em {tempo} segundos. É uma média saudável para bancos de dados modernos?"
            resposta = model.generate_content(prompt_perf)
            st.success("✅ Diagnóstico de performance gerado!")
            st.code(resposta.text, language="markdown")
            st.download_button("💾 Baixar Laudo de Performance (TXT)", resposta.text, "performance.txt", use_container_width=True)

# ==========================================
# ABA 4: RETORNO NÍVEL 2 (FECHAMENTO)
# ==========================================
with aba_retorno_n2:
    st.markdown("### 🔄 Consolidação de Encerramento (Nível 2)")
    c_1, c_2 = st.columns(2)
    with c_1:
        descricao_tecnica_retorno = st.text_area("Procedimento Técnico:", height=200, key="desc_tec_ret")
    with c_2:
        transcricao_feedback = st.text_area("Feedback do Cliente:", height=200)
    
    fotos_retorno = st.file_uploader("Evidências visuais (Prints/Logs):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_n2")
    
    if st.button("Gerar Relatório de Retorno", type="primary", use_container_width=True):
        with st.spinner("Consolidando..."):
            prompt_fechamento = f"Crie um relatório de encerramento profissional para o suporte do sistema {st.session_state['nome_sistema']} com: {descricao_tecnica_retorno} e feedback: {transcricao_feedback}"
            conteudo_final = [prompt_fechamento]
            if fotos_retorno:
                for f in fotos_retorno: conteudo_final.append(Image.open(f))
            
            resposta = model.generate_content(conteudo_final)
            st.success("✅ Relatório gerado!")
            st.code(resposta.text, language="markdown")
            st.download_button("💾 Baixar Retorno (TXT)", resposta.text, "retorno_n2.txt", use_container_width=True)

# ==========================================
# ABA 5: AUDITORIA
# ==========================================
with aba_auditoria:
    st.markdown("### ⚖️ Auditoria de Atendimentos de QA")
    parecer_auditoria = st.text_area("Histórico do Parecer/Atendimento:", height=300)
    fotos_auditoria = st.file_uploader("Evidências (Prints e-mail/Jira):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_auditoria")
    
    if st.button("Executar Auditoria Rigorosa", type="primary", use_container_width=True):
        if not parecer_auditoria:
            st.warning("⚠️ Cole o histórico do parecer.")
        else:
            with st.spinner("Auditorando atendimentos..."):
                prompt_auditor = f"""
                Você é um Auditor de Qualidade Sênior. Audite este atendimento baseado NAS SEGUINTES REGRAS DA EMPRESA:
                {st.session_state['regras_base']}
                
                --- REGRAS DE BOM SENSO ---
                1. Análise de Finalização: Se o chamado foi encerrado pelo analista com solução aplicada, o atendimento é "Finalizado Corretamente".
                2. A avaliação é feita EXCLUSIVAMENTE pelo que está registrado no texto e nas imagens.
                
                Analise o parecer e as imagens e gere:
                - Tabela: [Regra/Critério] | [Status: Passou/Falhou/Isento] | [Justificativa]
                - Veredito Final: [ATENDIMENTO VÁLIDO] ou [ATENDIMENTO PENALIZADO].
                
                Texto do Parecer:
                {parecer_auditoria}
                """
                
                conteudo = [prompt_auditor]
                if fotos_auditoria:
                    for f in fotos_auditoria: conteudo.append(Image.open(f))
                
                try:
                    resposta = model.generate_content(conteudo)
                    st.success("✅ Auditoria finalizada!")
                    st.code(resposta.text, language="markdown")
                    st.download_button("💾 Baixar Laudo Auditoria (TXT)", resposta.text, "laudo_auditoria.txt", use_container_width=True)
                except Exception as e:
                    st.error(f"Erro na auditoria: {e}")

# ==========================================
# ABA 6: FINALIZAÇÃO N2 (MÓDULO DE FECHAMENTO)
# ==========================================
with aba_finalizacao:
    st.markdown("### ✅ Finalização Profissional de Chamado (Parecer Interno)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        nome_cliente = st.text_input("Nome do Cliente / Contato:")
        telefone_contato = st.text_input("Telefone de Contato:")
    
    resolucao = st.text_area("Descrição Técnica da Resolução:", height=200, placeholder="Descreva tecnicamente o que foi executado...")
    
    if st.button("Gerar Parecer Técnico Interno", type="primary", use_container_width=True):
        if not nome_cliente or not resolucao:
            st.warning("⚠️ Preencha Nome do Cliente e Resolução.")
        else:
            with st.spinner("Estruturando parecer técnico..."):
                prompt_finalizacao = f"""
                Você é um Analista de Suporte Sênior do sistema {st.session_state['nome_sistema']}. Sua tarefa é criar um PARECER TÉCNICO INTERNO de encerramento para o CRM.
                
                REGRAS:
                - NÃO escreva como um e-mail. Não use "Prezado" ou "Atenciosamente".
                - Escreva na terceira pessoa, objetivo e estritamente formal.
                
                Dados:
                - Contato: {nome_cliente}
                - Telefone: {telefone_contato}
                - Procedimento: {resolucao}
                
                Estruture em:
                **1. Registro de Contato:** (Confirme o contato).
                **2. Procedimento Técnico Executado:** (Explique tecnicamente a ação).
                **3. Status de Encerramento:** (Confirme a validação e encerramento).
                """
                
                resposta = model.generate_content(prompt_finalizacao)
                st.success("✅ Parecer interno gerado com sucesso!")
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Parecer Técnico (TXT)", resposta.text, "parecer_interno.txt", use_container_width=True)
