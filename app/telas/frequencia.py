import streamlit as st
import pandas as pd
from datetime import date
from database import run_query, run_action

def render():
    st.header("Diário de Classe (Frequência)")

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

    col_data, col_vazio = st.columns([1, 3])
    data_chamada = col_data.date_input("Data da Aula", value=date.today())

    st.divider()

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


    df_chamada['Presente'] = df_chamada['Presente'].astype(bool)

    st.subheader(f"Lista de Presença - {data_chamada.strftime('%d/%m/%Y')}")
    st.caption("Marque a caixa para PRESENTE. Desmarque para AUSENTE.")

    df_editado = st.data_editor(
        df_chamada[['id_matricula', 'Nome do Aluno', 'Presente']],
        column_config={
            "Presente": st.column_config.CheckboxColumn(
                "Presença",
                help="Marque se o aluno estava presente",
                default=False,
            ),
            "id_matricula": None,
        },
        disabled=["id_matricula", "Nome do Aluno"],
        hide_index=True,
        width='stretch'
    )

    if st.button("Salvar Chamada"):
        sucesso_total = True
        
        for index, row in df_editado.iterrows():
            presenca_valor = 1 if row['Presente'] else 0
            id_mat = row['id_matricula']
    
            id_freq_existente = df_chamada.iloc[index]['id_frequencia']

            if pd.isna(id_freq_existente):
                sql_save = "INSERT INTO frequencia (data_aula, presente, id_matricula) VALUES (:dt, :p, :idm)"
                params = {"dt": data_chamada, "p": presenca_valor, "idm": id_mat}
            else:
                sql_save = "UPDATE frequencia SET presente = :p WHERE id_frequencia = :idf"
                params = {"p": presenca_valor, "idf": id_freq_existente}
            
            success, _ = run_action(sql_save, params)
            if not success:
                sucesso_total = False
        
        if sucesso_total:
            st.success("Frequência salva com sucesso!")
            st.rerun()
        else:
            st.error("Houve um erro ao salvar alguns registros.")