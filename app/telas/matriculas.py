import streamlit as st
from database import run_query, run_action

def render():
    st.header("Realizar Matrícula")
    alunos = run_query("SELECT id_aluno, nome FROM aluno")
    turmas = run_query("""
        SELECT t.id_turma, d.nome as disc, p.nome as prof 
        FROM turma t 
        JOIN disciplina d ON t.id_disciplina = d.id_disciplina
        JOIN professor p ON t.id_prof = p.id_prof
    """)
    
    if not alunos.empty and not turmas.empty:
        with st.form("mat_form"):
            aluno_map = {row['nome']: row['id_aluno'] for _, row in alunos.iterrows()}
            turma_map = {f"{row['disc']} ({row['prof']})": row['id_turma'] for _, row in turmas.iterrows()}
            sel_aluno = st.selectbox("Aluno", list(aluno_map.keys()))
            sel_turma = st.selectbox("Turma", list(turma_map.keys()))
            
            if st.form_submit_button("Matricular"):
                sql = "INSERT INTO matricula (id_aluno, id_turma) VALUES (:ida, :idt)"
                success, msg = run_action(sql, {"ida": aluno_map[sel_aluno], "idt": turma_map[sel_turma]})
                if success: st.success("Matrícula realizada!")
                else: st.error(msg)