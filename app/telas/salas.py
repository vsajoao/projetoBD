import streamlit as st
import pandas as pd
from database import run_query, run_action

def render():
    st.header("Gerenciamento de Salas")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Listar Salas", "Nova Sala", "Editar Sala", "Excluir Sala"])
    
    # --- ABA 1: LISTAR ---
    with tab1:
        st.subheader("Salas Cadastradas")
        df = run_query("SELECT numero_sala,capacidade,tipo FROM sala ORDER BY numero_sala")
        
        if not df.empty:
            # Mostra a tabela
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma sala cadastrada.")

    # --- ABA 2: CADASTRAR ---
    with tab2:
        st.subheader("Cadastrar Nova Sala")
        
        with st.form("form_nova_sala"):
            numero = st.text_input("Número/Nome da Sala (Ex: 101, Lab-A)")
            capacidade = st.number_input("Capacidade de Alunos", min_value=1, value=30, step=1)
            tipo = st.selectbox("Tipo da Sala", ["Sala de Aula", "Laboratório", "Auditório", "Biblioteca", "Ginásio"])
            
            if st.form_submit_button("Salvar Sala"):
                sql = "INSERT INTO sala (numero_sala, capacidade, tipo) VALUES (:n, :c, :t)"
                params = {"n": numero, "c": capacidade, "t": tipo}
                
                success, msg = run_action(sql, params)
                if success:
                    st.success(f"Sala {numero} cadastrada!")
                    st.rerun()
                else:
                    st.error(f"Erro ao salvar: {msg}")

    # --- ABA 3: EDITAR ---
    with tab3:
        st.subheader("Editar Sala")
        
        salas = run_query("SELECT id_sala, numero_sala, tipo FROM sala")
        
        if not salas.empty:
            sala_dict = {f"{row['numero_sala']} ({row['tipo']})": row['id_sala'] for _, row in salas.iterrows()}
            sel_nome = st.selectbox("Selecione para Editar", list(sala_dict.keys()))
            id_sel = sala_dict[sel_nome]
            
            # Carregar dados atuais
            dados = run_query(f"SELECT * FROM sala WHERE id_sala = {id_sel}").iloc[0]
            
            with st.form("form_edit_sala"):
                novo_num = st.text_input("Número/Nome", value=dados['numero_sala'])
                nova_cap = st.number_input("Capacidade", min_value=1, value=int(dados['capacidade']))
                
                # Tenta achar o índice do tipo atual na lista padrão
                tipos_opcoes = ["Sala de Aula", "Laboratório", "Auditório", "Biblioteca", "Ginásio"]
                idx_tipo = tipos_opcoes.index(dados['tipo']) if dados['tipo'] in tipos_opcoes else 0
                novo_tipo = st.selectbox("Tipo", tipos_opcoes, index=idx_tipo)
                
                if st.form_submit_button("Atualizar Dados"):
                    sql = "UPDATE sala SET numero_sala = :n, capacidade = :c, tipo = :t WHERE id_sala = :id"
                    params = {"n": novo_num, "c": nova_cap, "t": novo_tipo, "id": id_sel}
                    
                    success, msg = run_action(sql, params)
                    if success:
                        st.success("Sala atualizada!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {msg}")
        else:
            st.warning("Cadastre salas primeiro.")

    # --- ABA 4: EXCLUIR ---
    with tab4:
        st.subheader("Excluir Sala")
        
        if not salas.empty:
            sel_del_nome = st.selectbox("Selecione para Excluir", list(sala_dict.keys()), key="del_sala")
            
            st.warning("⚠️ Atenção: Você não pode excluir uma sala se houver turmas vinculadas a ela.")
            
            if st.button("Confirmar Exclusão"):
                id_del = sala_dict[sel_del_nome]
                sql = "DELETE FROM sala WHERE id_sala = :id"
                success, msg = run_action(sql, {"id": id_del})
                
                if success:
                    st.success("Sala excluída!")
                    st.rerun()
                else:
                    st.error(f"Não foi possível excluir. Provavelmente há turmas usando esta sala. ({msg})")