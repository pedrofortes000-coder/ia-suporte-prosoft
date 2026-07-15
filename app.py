# ==========================================
# ABA 4: RETORNO NÍVEL 2 (FECHAMENTO COM IMAGENS)
# ==========================================
with aba_retorno_n2:
    st.markdown("### 🔄 Consolidação de Encerramento (Nível 2)")
    st.markdown("Preencha o procedimento executado e anexe evidências visuais (prints de configuração, logs, ou testes positivos).")
    
    col_1, col_2 = st.columns(2)
    with col_1:
        descricao_tecnica = st.text_area("Procedimento Técnico:", height=200, placeholder="Ex: Ajuste de permissão, liberação de porta...")
    with col_2:
        transcricao_feedback = st.text_area("Relato/Feedback do Cliente:", height=200, placeholder="Ex: Cliente confirmou que o erro 1433 não ocorre mais.")
    
    # Campo de upload de imagens
    fotos_retorno = st.file_uploader("Anexar evidências (Prints/Logs):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if st.button("Gerar Relatório Final com Evidências", type="primary", use_container_width=True):
        if not descricao_tecnica or not transcricao_feedback:
            st.warning("⚠️ Preencha o procedimento técnico e o feedback antes de gerar.")
        else:
            with st.spinner("Consolidando relatório e analisando evidências..."):
                prompt_fechamento = f"""
                Você é um Analista de Suporte Sênior. Sua tarefa é criar um relatório de encerramento profissional.
                
                Dados fornecidos:
                1. Procedimento Técnico: {descricao_tecnica}
                2. Feedback do Cliente: {transcricao_feedback}
                
                Instrução: Analise as imagens anexadas (se houver) como prova de execução da tarefa.
                Crie um texto profissional contendo:
                - Resumo da solução.
                - Confirmação de que o problema foi sanado.
                - Mencione as evidências visuais anexadas para comprovar que o sistema está operando corretamente.
                """
                
                # Prepara o conteúdo (Texto + Imagens)
                conteudo_final = [prompt_fechamento]
                if fotos_retorno:
                    for foto in fotos_retorno:
                        conteudo_final.append(Image.open(foto))
                
                try:
                    resposta = model.generate_content(conteudo_final)
                    st.success("Relatório de encerramento gerado!")
                    st.markdown("### 📝 Relatório Final para CRM/Cliente")
                    st.info(resposta.text)
                except Exception as e:
                    st.error(f"Erro ao gerar relatório: {e}")
