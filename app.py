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

st.title("🤖 Portal IA: Diagnóstico, Relacionamento, Auditoria e Fechamento")

# --- CORREÇÃO VISUAL AGRESSIVA: QUEBRA DE LINHA NO BLOCO DE CÓDIGO ---
st.markdown("""
<style>
/* Força a quebra de linha em qualquer bloco de código ou texto pré-formatado */
div[data-testid="stCodeBlock"] pre, 
div[data-testid="stCodeBlock"] code,
pre, code {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    overflow-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# --- CRIAÇÃO DAS 6 ABAS ---
aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2, aba_auditoria, aba_finalizacao = st.tabs([
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno N2",
    "⚖️ Auditoria",
    "✅ Finalização N2"
])

# --- BASE DE CONHECIMENTO (CORE) ---
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

# ==========================================
# ABA 1: SUPORTE TÉCNICO (N1)
# ==========================================
with aba_suporte:
    st.markdown("### 🗄️ Dados do Ambiente")
    col1, col2 = st.columns(2)
    with col1:
        escopo = st.selectbox("Escopo da Lentidão", ["Selecione...", "Geral (Todos os usuários)", "Máquina Isolada", "Rotina Específica"], key="escopo")
        banco = st.selectbox("Versão do Banco de Dados", ["Selecione...", "Pervasive Workgroup v11", "Pervasive Workgroup v13 / v15", "Pervasive Server", "Microsoft SQL Server"], key="banco")
    with col2:
        conexao = st.multiselect("Tipo de Conexão", ["Rede Local", "Terminal Service (TS)", "Wi-Fi", "VPN"])
        usuarios = st.number_input("Quantidade de Usuários Afetados", min_value=1, step=1)
    
    st.divider()
    
    st.markdown("### ⏱️ Sintomas")
    col3, col4 = st.columns(2)
    with col3:
        rotinas_comuns = st.multiselect("Rotinas Afetadas", ["Abertura inicial do Prosoft", "Inclusão e Gravação de Cadastros", "Folha de Pagamento", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])
        rotinas_extras = st.text_input("Outras Rotinas (separar por vírgula)")
    with col4:
        tempo_resposta = st.number_input("Tempo de Resposta (Segundos)", min_value=0.0, step=0.5, format="%.1f")
    
    st.divider()
    fotos_upload = st.file_uploader("Upload de Prints (Configurações/Erro)", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_n1")
    
    if st.button("Analisar Chamado Nível 1", type="primary", use_container_width=True):
        with st.spinner("Analisando..."):
            base_extra = ""
            if os.path.exists("regras.txt"):
                with open("regras.txt", "r", encoding="utf-8") as f:
                    base_extra = "\n[REGRAS DINÂMICAS]\n" + f.read()
            
            prompt = f"""
            Você é especialista Prosoft. Base: {base_padrao + base_extra}. 
            Analise o cenário: {escopo}, {conexao}, {banco}. Sintomas: {rotinas_comuns} {rotinas_extras}.
            
            REGRAS RÍGIDAS DE RETORNO:
            1. Entregue APENAS o diagnóstico técnico.
            2. É ESTRITAMENTE PROIBIDO avaliar o comportamento das pessoas, gerar "feedbacks", "pontos fortes" ou qualquer tipo de avaliação de desempenho pessoal ou profissional.
            3. Mantenha a resposta impessoal e direta ao ponto.
            """
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
    texto_transcricao = st.text_area("Cole a transcrição aqui (opcional se enviar prints):", height=300)
    fotos_relacionamento = st.file_uploader("Upload de prints da reunião (Chat/Comentários/Tela):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_relac")
    
    if st.button("Gerar Dossiê para Nível 2", type="primary", use_container_width=True):
        if texto_transcricao or fotos_relacionamento:
            with st.spinner("Analisando transcrição e lendo imagens do chat..."):
                prompt_relac = f"""
                Você é um analista técnico escrivão. Analise a transcrição e/ou as imagens anexadas e crie um dossiê técnico para o Nível 2.

                NOVA INSTRUÇÃO DE LEITURA DE IMAGENS (OCR CONTEXTUAL):
                Se imagens foram enviadas (como prints de chat da reunião ou telas do sistema), você DEVE extrair as frases, comentários e erros presentes nelas.
                Cruze os comentários extraídos das imagens com o texto da transcrição. Insira as frases lidas das imagens no exato contexto onde elas se encaixam no dossiê.

                REGRAS DE FORMATAÇÃO ESTRITAS E INEGOCIÁVEIS:
                1. Retorne APENAS o resumo técnico, o ambiente relatado, o problema central, as falas extraídas do chat/imagens e a ação tomada.
                2. É ESTRITAMENTE PROIBIDO gerar seções de "Feedback", "Pontos Fortes", "Oportunidades de Melhoria".
                3. É ESTRITAMENTE PROIBIDO avaliar o comportamento ou proatividade das pessoas.
                4. Mantenha o tom frio, técnico e focado apenas na documentação do chamado.

                Transcrição:
                {texto_transcricao}
                """
                
                conteudo_relac = [prompt_relac]
                if fotos_relacionamento:
                    for f in fotos_relacionamento: conteudo_relac.append(Image.open(f))
                
                resposta = model.generate_content(conteudo_relac)
                st.success("✅ Dossiê gerado com extração de imagens!")
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Dossiê (TXT)", resposta.text, "dossie_n2.txt", use_container_width=True)
        else:
            st.warning("⚠️ Insira a transcrição em texto ou anexe pelo menos uma imagem do chat para gerar o dossiê.")

# ==========================================
# ABA 3: PERFORMANCE
# ==========================================
with aba_performance:
    st.markdown("### 📊 Calculadora de Performance")
    c1, c2 = st.columns(2)
    qtd = c1.number_input("Quantidade de Notas", min_value=1)
    tempo = c2.number_input("Tempo Total (Segundos)", min_value=0.1)
    
    if st.button("Analisar Eficiência", type="primary"):
        with st.spinner("Analisando eficiência..."):
            prompt_perf = f"""
            Analise a performance: {qtd} notas em {tempo} segundos. Lembre-se: abaixo de 1 nota/s indica gargalo.
            
            REGRA: Responda APENAS com a análise matemática e técnica de banco de dados. Sem saudações e sem feedback comportamental.
            """
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
            prompt_fechamento = f"""
            Crie um relatório de encerramento profissional com: {descricao_tecnica_retorno} e feedback: {transcricao_feedback}
            
            REGRAS RÍGIDAS: 
            É ESTRITAMENTE PROIBIDO avaliar o comportamento, gerar seções de feedback pessoal ou dar notas para a atuação do analista ou do cliente. Mantenha o tom estritamente documental.
            """
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
    st.markdown("### ⚖️ Auditoria de Atendimentos N2 (Validação 16/07/2026)")
    parecer_auditoria = st.text_area("Histórico do Parecer/Atendimento:", height=300)
    fotos_auditoria = st.file_uploader("Evidências (Prints e-mail/Jira):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_auditoria")
    
    if st.button("Executar Auditoria Rigorosa", type="primary", use_container_width=True):
        if not parecer_auditoria:
            st.warning("⚠️ Cole o histórico do parecer.")
        else:
            with st.spinner("Auditorando atendimentos..."):
                prompt_auditor = f"""
                Você é um Auditor de Qualidade Sênior da Prosoft. Sua missão é auditar o atendimento de Nível 2 abaixo.
                
                --- REGRAS DE BOM SENSO ---
                1. Análise de Finalização: Se o chamado foi encerrado pelo analista e consta no parecer que a solução foi aplicada, ou que o cliente ficou responsável por monitorar/reiniciar, o analista NÃO deve ser penalizado por "Contato" ou "Contato p/ finalizar". O atendimento é considerado "Finalizado Corretamente".
                2. O que não está no parecer não conta: A avaliação é feita EXCLUSIVAMENTE pelo que está registrado no texto e nas imagens anexadas.
                3. É ESTRITAMENTE PROIBIDO gerar seções de "Feedback pessoal", "Pontos Fortes", "Melhorias de comunicação" ou avaliar a postura de qualquer pessoa. Atenha-se puramente aos critérios abaixo.
                
                --- CRITÉRIOS DE AUDITORIA ---
                1. Contato (Grave): Ignorar se o chamado foi finalizado corretamente.
                2. Registro (Leve): Ações registradas com intervalo máx de 2 dias úteis.
                3. Vínculo MAN/PDP (Leve): Deve constar código (MAN, PDP, ANR, etc) e link do Jira.
                4. Divulgação da MAN/PDP (Grave): E-mail com supervisão em cópia e assunto "Criado projeto no Jira: [CODIGO] - [ASSUNTO]".
                5. Notificação ao cliente (Grave): Informar cliente sobre análise do Dev.
                6. Justificativa de CR/Artigo (Leve): Referenciar base (ID/Link). Artigo A124 para procedimentos internos.
                7. Contato agendado (Grave): Cumprir data.
                8. Contato p/ finalizar (Grave): Ignorar se o cliente aceitou monitorar ou reiniciar o sistema.
                9. Erros gramaticais (Leve): Comprometimento da compreensão.
                10. Campo Produto (Leve): Preenchimento correto.
                11. LGPD (Grave): Texto padrão registrado.
                12. Controle diretório (Leve): Caminho/Link da base salva.
                13. Tipo 1882 (Leve): Respostas coerentes ao script obrigatório.

                Analise o parecer e as imagens e gere:
                - Tabela: [Regra] | [Status: Passou/Falhou/Isento] | [Severidade] | [Justificativa]
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
    st.markdown("### ✅ Finalização Profissional de Chamado (Nível 2)")
    st.markdown("Preencha os campos abaixo para gerar um parecer técnico interno de encerramento padronizado para o CRM.")
    
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
                Você é um Analista de Suporte Sênior. Sua tarefa é criar um PARECER TÉCNICO INTERNO de encerramento para ser salvo no sistema de chamados (CRM/Jira) da Prosoft.
                
                REGRAS RÍGIDAS DE FORMATAÇÃO:
                - NÃO escreva como um e-mail para o cliente. Não use "Prezado", "Atenciosamente" ou saudações.
                - Escreva um log de registro interno, na terceira pessoa, objetivo e estritamente formal.
                - É ESTRITAMENTE PROIBIDO incluir avaliações de desempenho, feedbacks comportamentais ou ditar o que o técnico ou o cliente fizeram de certo/errado.
                
                Dados da tratativa:
                - Contato: {nome_cliente}
                - Telefone: {telefone_contato}
                - Procedimento Técnico Realizado: {resolucao}
                
                Estruture o parecer EXATAMENTE com os seguintes tópicos:
                
                **1. Registro de Contato:**
                (Confirme o contato com o cliente no número informado de forma objetiva).
                
                **2. Procedimento Técnico Executado:**
                (Traduza a ação realizada para uma linguagem técnica, clara e detalhada do que foi alterado/corrigido no ambiente do cliente).
                
                **3. Status de Encerramento:**
                (Confirme que os testes foram validados e que o ticket está sendo finalizado com sucesso).
                """
                
                resposta = model.generate_content(prompt_finalizacao)
                st.success("✅ Parecer interno gerado com sucesso!")
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Parecer Técnico (TXT)", resposta.text, "parecer_interno_n2.txt", use_container_width=True)
