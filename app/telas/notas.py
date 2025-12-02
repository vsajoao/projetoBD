import streamlit as st
from database import run_query, run_action

def render():
    st.header("Lançar Notas")
    
    mats = run_query("""
        SELECT m.id_matricula, a.nome, d.nome as disc 
        FROM matricula m 
        JOIN aluno a ON m.id_aluno = a.id_aluno
        JOIN turma t ON m.id_turma = t.id_turma
        JOIN disciplina d ON t.id_disciplina = d.id_disciplina
    """)
    avals = run_query("SELECT id_avaliacao, descricao FROM avaliacao")
    
    if not mats.empty and not avals.empty:
        with st.form("nota_form"):
            mat_map = {f"{row['nome']} - {row['disc']}": row['id_matricula'] for _, row in mats.iterrows()}
            aval_map = {row['descricao']: row['id_avaliacao'] for _, row in avals.iterrows()}
            sel_mat = st.selectbox("Aluno", list(mat_map.keys()))
            sel_aval = st.selectbox("Avaliação", list(aval_map.keys()))
            val_nota = st.number_input("Nota (0-10)", step=0.1)
            
            if st.form_submit_button("Salvar"):
                sql = "INSERT INTO nota (valor, id_matricula, id_avaliacao) VALUES (:v, :m, :a)"
                success, msg = run_action(sql, {"v": val_nota, "m": mat_map[sel_mat], "a": aval_map[sel_aval]})
                if success: st.success("Nota salva!")
                else: st.error(f"Erro do Banco: {msg}")