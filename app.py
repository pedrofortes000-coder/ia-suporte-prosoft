import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 

# --- CONFIGURAÇÃO E SEGURANÇA ---
st.set_page_config(page_title="Portal IA: Suporte e QA", page_icon="🤖", layout="wide")

try:
    chave_limpa = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=chave_limpa)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Erro ao configurar a API. Verifique o seu st.secrets no painel do Streamlit.")
    st.stop()

st.title("🤖 Portal IA: Diagnóstico, QA, Retornos e Cloud")

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

# --- CRIAÇÃO DAS 7 ABAS ---
aba_suporte, aba_relacionamento, aba_performance, aba_retorno_n2, aba_auditoria, aba_finalizacao, aba_migracao = st.tabs([
    "🛠️ Suporte (N1)", 
    "🤝 Relacionamento (N2)", 
    "📊 Performance", 
    "🔄 Retorno N2",
    "⚖️ Auditoria",
    "✅ Finalização N2",
    "☁️ Migração Cloud"
])

# --- BASE DE CONHECIMENTO (CORE) ---
base_padrao = """
[REGRAS FIXAS DE INFRAESTRUTURA]
1. Lentidão Generalizada: Servidor mínimo de 12GB e processador de 2GHz x64. Rede mínimo 10Mb/s (recomendado 1Gb/s).
2. Lentidão Isolada: Estação local com 4GB de RAM, Win PRO/ENTERPRISE, .NET 4.8 e Java 8.
3. Comunicação Externa: "Serviço de Integração" atualizado, internet min 4Mb/s, portas 80/8080 liberadas.
4. Esgotamento de Memória: Para TS (Terminal Service), 8GB RAM base + 1GB por usuário. Reiniciar servidor libera memória presa.
5. Limites de Banco: Workgroup 11 (max 10 usuários). Workgroup 13/15 (max 35 usuários). Server (max 500 usuários).
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
        rotinas_comuns = st.multiselect("Rotinas Afetadas", ["Abertura inicial", "Inclusão e Gravação de Cadastros", "Folha de Pagamento", "Comunicação Externa (Portal, eSocial, Reinf)", "Processamento/Relatórios"])
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
            Você é especialista de suporte técnico. Base: {base_padrao + base_extra}. 
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
                Você é um analista técnico escrivão. Analise a transcrição e/ou as imagens anexadas e crie um dossiê técnico.

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
    qtd = c1.number_input("Quantidade de Notas/Registros", min_value=1)
    tempo = c2.number_input("Tempo Total (Segundos)", min_value=0.1)
    
    if st.button("Analisar Eficiência", type="primary"):
        with st.spinner("Analisando eficiência..."):
            prompt_perf = f"""
            Analise a performance: {qtd} registros em {tempo} segundos. Lembre-se: abaixo de 1 registro/s indica gargalo.
            
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
    st.markdown("### ⚖️ Auditoria de Atendimentos N2")
    parecer_auditoria = st.text_area("Histórico do Parecer/Atendimento:", height=300)
    fotos_auditoria = st.file_uploader("Evidências (Prints e-mail/Jira):", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_auditoria")
    
    if st.button("Executar Auditoria Rigorosa", type="primary", use_container_width=True):
        if not parecer_auditoria:
            st.warning("⚠️ Cole o histórico do parecer.")
        else:
            with st.spinner("Auditorando atendimentos..."):
                prompt_auditor = f"""
                Você é um Auditor de Qualidade Sênior. Sua missão é auditar o atendimento de Nível 2 abaixo.
                
                --- REGRAS DE BOM SENSO ---
                1. Análise de Finalização: Se o chamado foi encerrado pelo analista e consta no parecer que a solução foi aplicada, ou que o cliente ficou responsável por monitorar/reiniciar, o analista NÃO deve ser penalizado por "Contato" ou "Contato p/ finalizar". O atendimento é considerado "Finalizado Corretamente".
                2. O que não está no parecer não conta: A avaliação é feita EXCLUSIVAMENTE pelo que está registrado no texto e nas imagens anexadas.
                3. É ESTRITAMENTE PROIBIDO gerar seções de "Feedback pessoal", "Pontos Fortes", "Melhorias de comunicação" ou avaliar a postura de qualquer pessoa. Atenha-se puramente aos critérios técnicos.
                
                --- CRITÉRIOS DE AUDITORIA ---
                1. Contato (Grave): Ignorar se o chamado foi finalizado corretamente.
                2. Registro (Leve): Ações registradas com intervalo máx de 2 dias úteis.
                3. Vínculo MAN/PDP (Leve): Deve constar código (MAN, PDP, ANR, etc) e link do Jira.
                4. Divulgação da MAN/PDP (Grave): E-mail com supervisão em cópia e assunto "Criado projeto no Jira: [CODIGO] - [ASSUNTO]".
                5. Notificação ao cliente (Grave): Informar cliente sobre análise do Dev.
                6. Justificativa de CR/Artigo (Leve): Referenciar base (ID/Link).
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
    st.markdown("### ✅ Finalização Profissional de Chamado")
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
                Você é um Analista de Suporte Sênior. Sua tarefa é criar um PARECER TÉCNICO INTERNO de encerramento para ser salvo no sistema de chamados (CRM/Jira).
                
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

# ==========================================
# ABA 7: MIGRAÇÃO CLOUD (NOVO MÓDULO)
# ==========================================
with aba_migracao:
    st.markdown("### ☁️ Dimensionamento de Servidor em Nuvem")
    st.markdown("Insira os dados da infraestrutura atual do cliente para gerar uma recomendação de migração Cloud baseada nas métricas do provedor.")
    
    col_cloud1, col_cloud2 = st.columns(2)
    with col_cloud1:
        cloud_usuarios = st.number_input("Quantidade de Usuários Ativos (Acessos simultâneos)", min_value=1, step=1, max_value=99)
        cloud_ram_atual = st.number_input("Memória RAM Atual do Servidor Físico (GB)", min_value=4, step=2)
    with col_cloud2:
        cloud_banco_tamanho = st.number_input("Tamanho Estimado do Banco de Dados / Arquivos (GB)", min_value=1, step=10)
        cloud_cpu_atual = st.number_input("Cores do Processador Atual", min_value=2, step=2)
        
    st.divider()
    fotos_hardware = st.file_uploader("Opcional: Enviar prints das propriedades do servidor atual", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="fotos_hardware")
    
    if st.button("Gerar Recomendação de Arquitetura Cloud", type="primary", use_container_width=True):
        with st.spinner("Calculando o dimensionamento ideal da nuvem..."):
            prompt_cloud = f"""
            Você atua como um Arquiteto de Soluções Cloud especializado em ERPs. 
            Sua tarefa é ler os dados do cliente e recomendar a configuração ideal para a migração para a nuvem.
            
            Dados atuais do cliente:
            - Usuários Ativos: {cloud_usuarios}
            - RAM Física Atual: {cloud_ram_atual} GB
            - Tamanho dos Arquivos/Banco: {cloud_banco_tamanho} GB
            - CPU Física Atual: {cloud_cpu_atual} Cores
            
            PARÂMETROS OBRIGATÓRIOS DO PROVEDOR CLOUD (Respeite estes limites exatos):
            - Processamento: Escolha entre 2 a 48 Cores (vCPU Dedicados).
            - Memória RAM: Escolha entre 2 a 512 GB (Memória ECC DDR5).
            - SSD NVMe (Armazenamento): Escolha entre 60 GB a 2 TB (Alta velocidade).
            - Usuários suportados na plataforma: 1 a 99 usuários.
            
            REGRA DE CÁLCULO DE RECURSOS (BASEADA NAS REGRAS DO SISTEMA):
            - Memória RAM para Terminal Service (TS): Exige-se um mínimo de 8GB de base para o Sistema Operacional + 1GB adicional para cada usuário.
            - Armazenamento: O SSD NVMe recomendado deve ter espaço suficiente para o tamanho atual do banco de dados + 30% a 50% de folga para crescimento do log transacional e backups locais temporários. O mínimo exigido pelo provedor é 60 GB.
            - CPU: Calcule a vCPU com base no número de usuários e no tamanho do banco, garantindo que não haja gargalos (min 4 Cores recomendados para aplicações corporativas, ou mais, a depender dos usuários).

            Gere um laudo técnico contendo:
            1. Configuração Recomendada (vCPU, RAM, SSD NVMe e Usuários) de forma clara.
            2. Justificativa do Cálculo (explique matematicamente por que escolheu essa RAM e SSD baseando-se na regra do sistema).
            3. Benefícios da Migração frente ao hardware físico atual relatado.
            
            REGRAS RÍGIDAS DE FORMATAÇÃO:
            - É ESTRITAMENTE PROIBIDO gerar feedbacks comportamentais, pontos fortes ou fracos.
            - Seja direto, técnico e utilize listas para facilitar a leitura rápida da recomendação.
            """
            
            conteudo_cloud = [prompt_cloud]
            if fotos_hardware:
                for f in fotos_hardware: conteudo_cloud.append(Image.open(f))
            
            try:
                resposta = model.generate_content(conteudo_cloud)
                st.success("✅ Recomendação Cloud gerada com sucesso!")
                st.code(resposta.text, language="markdown")
                st.download_button("💾 Baixar Proposta Cloud (TXT)", resposta.text, "proposta_cloud.txt", use_container_width=True)
            except Exception as e:
                st.error(f"Erro na geração: {e}")
