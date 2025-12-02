import streamlit as st
import pandas as pd
from database import run_query, run_action

def render():
    st.header("Gestão de Avaliações")
    
    tab1, tab2, tab3 = st.tabs(["Agendar & Listar", "Editar Avaliação", "Excluir Avaliação"])
    
    turmas_df = run_query("""
        SELECT t.id_turma, d.nome as disc, p.nome as prof, t.ano, t.semestre 
        FROM turma t
        JOIN disciplina d ON t.id_disciplina = d.id_disciplina
        JOIN professor p ON t.id_prof = p.id_prof
        ORDER BY t.ano DESC, t.semestre DESC
    """)
    
    if turmas_df.empty:
        st.warning("Nenhuma turma cadastrada. Cadastre turmas antes de criar avaliações.")
        return

    turma_dict = {f"{row['disc']} ({row['ano']}/{row['semestre']}) - Prof. {row['prof']}": row['id_turma'] for _, row in turmas_df.iterrows()}

    with tab1:
        st.subheader("Cronograma de Provas")
        
        turma_sel_nome = st.selectbox("Selecione a Turma:", list(turma_dict.keys()), key="sel_turma_tab1")
        id_turma_sel = turma_dict[turma_sel_nome]
        
        st.divider()
        col_list, col_form = st.columns([1, 1])

        with col_list:
            st.markdown("##### Avaliações Agendadas")
            avals = run_query(f"SELECT descricao, peso, data_prevista FROM avaliacao WHERE id_turma = {id_turma_sel}")
            if not avals.empty:
                avals['data_prevista'] = pd.to_datetime(avals['data_prevista']).dt.strftime('%d/%m/%Y')
                st.dataframe(avals, width='stretch')
            else:
                st.info("Nenhuma avaliação nesta turma.")

        with col_form:
            st.markdown("##### ➕ Nova Avaliação")
            with st.form("add_aval_form"):
                desc_aval = st.text_input("Descrição (Ex: Prova 1)")
                peso_aval = st.number_input("Peso", value=10.0, step=0.5)
                data_aval = st.date_input("Data Prevista")
                
                if st.form_submit_button("Agendar"):
                    sql = "INSERT INTO avaliacao (descricao, peso, data_prevista, id_turma) VALUES (:d, :p, :dt, :id)"
                    success, msg = run_action(sql, {"d": desc_aval, "p": peso_aval, "dt": data_aval, "id": id_turma_sel})
                    if success:
                        st.success("Agendado!")
                        st.rerun()
                    else:
                        st.error(msg)
    with tab2:
        st.subheader("Editar Avaliação")
        
        turma_nome_edit = st.selectbox("Selecione a Turma:", list(turma_dict.keys()), key="sel_turma_tab2")
        id_turma_edit = turma_dict[turma_nome_edit]
        
        avals_edit = run_query(f"SELECT id_avaliacao, descricao FROM avaliacao WHERE id_turma = {id_turma_edit}")
        
        if not avals_edit.empty:
            aval_dict = {row['descricao']: row['id_avaliacao'] for _, row in avals_edit.iterrows()}
            aval_nome = st.selectbox("Selecione a Avaliação:", list(aval_dict.keys()), key="sel_aval_edit")
            id_aval = aval_dict[aval_nome]
            
            dados = run_query(f"SELECT * FROM avaliacao WHERE id_avaliacao = {id_aval}").iloc[0]
            
            with st.form("form_edit_aval"):
                novo_desc = st.text_input("Descrição", value=dados['descricao'])
                novo_peso = st.number_input("Peso", value=float(dados['peso']), step=0.5)
                data_obj = pd.to_datetime(dados['data_prevista']).date() if dados['data_prevista'] else None
                nova_data = st.date_input("Data Prevista", value=data_obj)
                
                if st.form_submit_button("Salvar Alterações"):
                    sql = "UPDATE avaliacao SET descricao=:d, peso=:p, data_prevista=:dt WHERE id_avaliacao=:id"
                    success, msg = run_action(sql, {"d": novo_desc, "p": novo_peso, "dt": nova_data, "id": id_aval})
                    if success:
                        st.success("Atualizado!")
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.info("Sem avaliações para editar nesta turma.")

    with tab3:
        st.subheader("Excluir Avaliação")
        st.warning("Ao excluir uma avaliação, todas as NOTAS lançadas para ela serão apagadas.")
        
        turma_nome_del = st.selectbox("Selecione a Turma:", list(turma_dict.keys()), key="sel_turma_del")
        id_turma_del = turma_dict[turma_nome_del]
        
        avals_del = run_query(f"SELECT id_avaliacao, descricao FROM avaliacao WHERE id_turma = {id_turma_del}")
        
        if not avals_del.empty:
            aval_dict_del = {row['descricao']: row['id_avaliacao'] for _, row in avals_del.iterrows()}
            aval_nome_del = st.selectbox("Selecione para Excluir:", list(aval_dict_del.keys()), key="sel_aval_del")
            
            if st.button("Confirmar Exclusão"):
                id_del = aval_dict_del[aval_nome_del]
                run_action("DELETE FROM nota WHERE id_avaliacao = :id", {"id": id_del})
                success, msg = run_action("DELETE FROM avaliacao WHERE id_avaliacao = :id", {"id": id_del})
                
                if success:
                    st.success("Avaliação excluída!")
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.info("Sem avaliações para excluir.")