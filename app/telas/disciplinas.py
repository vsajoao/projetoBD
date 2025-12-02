import streamlit as st
import pandas as pd
from database import run_query, run_action

def render():
    st.header("Gerenciamento de Disciplinas")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Listar Disciplinas", "Nova Disciplina", "Editar Disciplina", "Excluir Disciplina"])
    with tab1:
        st.subheader("Disciplinas Cadastradas")
        df = run_query("""
            SELECT d.nome, d.carga_horaria, d.ementa, dep.nome as departamento
            FROM disciplina d
            JOIN departamento dep ON d.id_depto = dep.id_depto
            ORDER BY d.nome
        """)
        
        if not df.empty:
            st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.info("Nenhuma disciplina cadastrada.")
    with tab2:
        st.subheader("Cadastrar Nova Disciplina")
        deptos = run_query("SELECT id_depto, nome FROM departamento")
        
        if not deptos.empty:
            with st.form("form_nova_disc"):
                nome = st.text_input("Nome da Disciplina")
                carga = st.number_input("Carga Horária", min_value=10, step=10, value=60)
                ementa = st.text_area("Ementa (Descrição)")
                depto_dict = {row['nome']: row['id_depto'] for _, row in deptos.iterrows()}
                sel_depto = st.selectbox("Departamento", list(depto_dict.keys()))
                
                if st.form_submit_button("Salvar Disciplina"):
                    sql = """
                        INSERT INTO disciplina (nome, carga_horaria, ementa, id_depto) 
                        VALUES (:n, :c, :e, :id_d)
                    """
                    params = {
                        "n": nome,
                        "c": carga,
                        "e": ementa,
                        "id_d": depto_dict[sel_depto]
                    }
                    success, msg = run_action(sql, params)
                    
                    if success:
                        st.success(f"Disciplina '{nome}' cadastrada!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao salvar: {msg}")
        else:
            st.warning("Cadastre Departamentos no banco de dados primeiro.")
    with tab3:
        st.subheader("Editar Disciplina")
        discs = run_query("SELECT id_disciplina, nome FROM disciplina")
        
        if not discs.empty:
            disc_dict = {row['nome']: row['id_disciplina'] for _, row in discs.iterrows()}
            sel_disc_nome = st.selectbox("Selecione para Editar", list(disc_dict.keys()))
            id_sel = disc_dict[sel_disc_nome]
            dados = run_query(f"SELECT * FROM disciplina WHERE id_disciplina = {id_sel}").iloc[0]
            with st.form("form_edit_disc"):
                novo_nome = st.text_input("Nome", value=dados['nome'])
                nova_carga = st.number_input("Carga Horária", min_value=10, step=10, value=int(dados['carga_horaria']))
                nova_ementa = st.text_area("Ementa", value=dados['ementa'])
       
                deptos_edit = run_query("SELECT id_depto, nome FROM departamento")
                depto_dict_edit = {row['nome']: row['id_depto'] for _, row in deptos_edit.iterrows()}
                
                id_dep_atual = dados['id_depto']
                nome_dep_atual = next((k for k, v in depto_dict_edit.items() if v == id_dep_atual), None)

                index_dep = list(depto_dict_edit.keys()).index(nome_dep_atual) if nome_dep_atual else 0
                
                novo_depto_nome = st.selectbox("Departamento", list(depto_dict_edit.keys()), index=index_dep)
                
                if st.form_submit_button("Atualizar Dados"):
                    sql = """
                        UPDATE disciplina 
                        SET nome = :n, carga_horaria = :c, ementa = :e, id_depto = :id_d
                        WHERE id_disciplina = :id
                    """
                    params = {
                        "n": novo_nome,
                        "c": nova_carga,
                        "e": nova_ementa,
                        "id_d": depto_dict_edit[novo_depto_nome],
                        "id": id_sel
                    }
                    success, msg = run_action(sql, params)
                    
                    if success:
                        st.success("Disciplina atualizada!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {msg}")
    with tab4:
        st.subheader("Excluir Disciplina")
        
        if not discs.empty:
            sel_del_nome = st.selectbox("Selecione para Excluir", list(disc_dict.keys()), key="del_disc")
            
            st.warning("Atenção: Você só pode excluir disciplinas que NÃO tenham turmas cadastradas.")
            
            if st.button("Confirmar Exclusão"):
                id_del = disc_dict[sel_del_nome]
                sql = "DELETE FROM disciplina WHERE id_disciplina = :id"
                success, msg = run_action(sql, {"id": id_del})
                
                if success:
                    st.success("Disciplina excluída!")
                    st.rerun()
                else:
                    st.error(f"Não foi possível excluir. Verifique se há turmas vinculadas. ({msg})")