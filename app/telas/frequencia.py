import streamlit as st
import pandas as pd
from datetime import date
from database import run_query, run_action

def render():
    st.header("Diário de Classe (Frequência)")
    
    # 1. Selecionar Turma
    turmas = run_query("""
        SELECT t.id_turma, d.nome as disc, p.nome as prof, t.ano, t.semestre 
        FROM turma t
        JOIN disciplina d ON t.id_disciplina = d.id_disciplina
        JOIN professor p ON t.id_prof = p.id_prof
        ORDER BY t.ano DESC, t.semestre DESC
    """)
    
    if turmas.empty:
        st.warning("Nenhuma turma cadastrada.")
        return

    turma_dict = {f"{row['disc']} ({row['ano']}/{row['semestre']}) - Prof. {row['prof']}": row['id_turma'] for _, row in turmas.iterrows()}
    turma_selecionada = st.selectbox("Selecione a Turma:", list(turma_dict.keys()))
    id_turma = turma_dict[turma_selecionada]

    # 2. Selecionar Data
    col_data, col_vazio = st.columns([1, 3])
    data_chamada = col_data.date_input("Data da Aula", value=date.today())

    st.divider()

    # 3. Buscar Alunos e Status Atual (se já houve chamada nesse dia)
    # Fazemos um LEFT JOIN com a tabela frequencia para ver se já tem registro nesse dia
    sql = f"""
        SELECT 
            m.id_matricula, 
            a.nome as 'Nome do Aluno', 
            COALESCE(f.presente, 0) as 'Presente', -- Se null, coloca 0 (Falso)
            f.id_frequencia
        FROM matricula m
        JOIN aluno a ON m.id_aluno = a.id_aluno
        LEFT JOIN frequencia f ON m.id_matricula = f.id_matricula AND f.data_aula = '{data_chamada}'
        WHERE m.id_turma = {id_turma}
        ORDER BY a.nome
    """
    
    df_chamada = run_query(sql)

    if df_chamada.empty:
        st.info("Nenhum aluno matriculado nesta turma.")
        return

    # Ajusta o tipo de dado para Boolean para o Streamlit mostrar Checkbox
    df_chamada['Presente'] = df_chamada['Presente'].astype(bool)

    # 4. Tabela Editável (Data Editor)
    st.subheader(f"Lista de Presença - {data_chamada.strftime('%d/%m/%Y')}")
    st.caption("Marque a caixa para PRESENTE. Desmarque para AUSENTE.")

    # O st.data_editor permite editar a tabela na tela
    df_editado = st.data_editor(
        df_chamada[['id_matricula', 'Nome do Aluno', 'Presente']], # Esconde o ID da frequencia
        column_config={
            "Presente": st.column_config.CheckboxColumn(
                "Presença",
                help="Marque se o aluno estava presente",
                default=False,
            ),
            "id_matricula": None, # Esconde o ID visualmente
        },
        disabled=["id_matricula", "Nome do Aluno"], # Impede editar nome/id
        hide_index=True,
        width='stretch'
    )

    # 5. Botão Salvar
    if st.button("Salvar Chamada"):
        sucesso_total = True
        
        # Comparamos o DF editado com o original para saber os IDs ocultos
        # Iteramos sobre as linhas para salvar no banco
        for index, row in df_editado.iterrows():
            presenca_valor = 1 if row['Presente'] else 0
            id_mat = row['id_matricula']
            
            # Recupera o id_frequencia original (se existia) usando o index
            id_freq_existente = df_chamada.iloc[index]['id_frequencia']
            
            # Se id_freq_existente for NaN (pandas) ou None, significa que não tinha registro -> INSERT
            if pd.isna(id_freq_existente):
                sql_save = "INSERT INTO frequencia (data_aula, presente, id_matricula) VALUES (:dt, :p, :idm)"
                params = {"dt": data_chamada, "p": presenca_valor, "idm": id_mat}
            else:
                # Se já existia, faz UPDATE
                sql_save = "UPDATE frequencia SET presente = :p WHERE id_frequencia = :idf"
                params = {"p": presenca_valor, "idf": id_freq_existente}
            
            success, _ = run_action(sql_save, params)
            if not success:
                sucesso_total = False
        
        if sucesso_total:
            st.success("Frequência salva com sucesso!")
            # Recarrega a página para atualizar os IDs
            st.rerun()
        else:
            st.error("Houve um erro ao salvar alguns registros.")