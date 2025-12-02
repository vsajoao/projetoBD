import streamlit as st
import pandas as pd
from database import run_query, run_action

def render():
    st.header("Gerenciamento de Alunos")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Listar Alunos", "Novo Aluno", "Editar Aluno", "Excluir Aluno"])
    
    # --- LISTAR ---
    with tab1:
        st.subheader("Lista de Alunos")
        df_alunos = run_query("SELECT nome, email, data_nascimento, foto FROM aluno")
        
        if not df_alunos.empty:
            st.dataframe(df_alunos[['nome', 'email', 'data_nascimento']], use_container_width=True, hide_index=True)
            st.markdown("### 📸 Galeria de Fotos")
            cols = st.columns(5)
            for index, row in df_alunos.iterrows():
                with cols[index % 5]:
                    if row['foto']:
                        st.image(row['foto'], caption=row['nome'], width=100)
    
    # --- CADASTRAR ---
    with tab2:
        st.subheader("Cadastrar Novo")
        with st.form("form_cadastro"):
            novo_nome = st.text_input("Nome Completo")
            novo_email = st.text_input("Email")
            nova_data = st.date_input("Data de Nascimento")
            foto_upload = st.file_uploader("Foto", type=['jpg', 'png'])
            
            if st.form_submit_button("Salvar"):
                foto_blob = foto_upload.read() if foto_upload else None
                sql = "INSERT INTO aluno (nome, email, data_nascimento, foto) VALUES (:nome, :email, :dt, :ft)"
                success, msg = run_action(sql, {"nome": novo_nome, "email": novo_email, "dt": nova_data, "ft": foto_blob})
                if success:
                    st.success("Aluno cadastrado!")
                    st.rerun()
                else:
                    st.error(f"Erro: {msg}")

    # --- EDITAR ---
    with tab3:
        st.subheader("Editar Aluno Existente")
        df_select = run_query("SELECT id_aluno, nome FROM aluno")
        
        if not df_select.empty:
            aluno_dict = {row['nome']: row['id_aluno'] for _, row in df_select.iterrows()}
            selected_aluno_nome = st.selectbox("Selecione o Aluno", list(aluno_dict.keys()) if aluno_dict else [])
            
            if selected_aluno_nome:
                id_selecionado = aluno_dict[selected_aluno_nome]
                dados = run_query(f"SELECT * FROM aluno WHERE id_aluno = {id_selecionado}").iloc[0]
                
                with st.form("form_editar"):
                    edit_nome = st.text_input("Nome", value=dados['nome'])
                    edit_email = st.text_input("Email", value=dados['email'])
                    data_obj = pd.to_datetime(dados['data_nascimento']).date() if dados['data_nascimento'] else None
                    edit_data = st.date_input("Data de Nascimento", value=data_obj)
                    edit_foto = st.file_uploader("Alterar Foto (Opcional)", type=['jpg', 'png'])
                    
                    if st.form_submit_button("Atualizar Dados"):
                        if edit_foto:
                            foto_blob = edit_foto.read()
                            sql = "UPDATE aluno SET nome=:n, email=:e, data_nascimento=:d, foto=:f WHERE id_aluno=:id"
                            params = {"n": edit_nome, "e": edit_email, "d": edit_data, "f": foto_blob, "id": id_selecionado}
                        else:
                            sql = "UPDATE aluno SET nome=:n, email=:e, data_nascimento=:d WHERE id_aluno=:id"
                            params = {"n": edit_nome, "e": edit_email, "d": edit_data, "id": id_selecionado}
                        
                        success, msg = run_action(sql, params)
                        if success:
                            st.success("Dados atualizados!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao atualizar: {msg}")

    # --- EXCLUIR ---
    with tab4:
        st.subheader("Excluir Aluno")
        st.warning("⚠️ Atenção: Ao excluir, todas as matrículas e notas serão apagadas.")
        
        if not df_alunos.empty:
            aluno_dict_del = {row['nome']: row['id_aluno'] for _, row in run_query("SELECT id_aluno, nome FROM aluno").iterrows()}
            del_nome = st.selectbox("Selecione para Excluir", list(aluno_dict_del.keys()), key="del_box")
            
            if st.button("Confirmar Exclusão"):
                id_del = aluno_dict_del[del_nome]
                # Cascata manual
                run_action("DELETE FROM nota WHERE id_matricula IN (SELECT id_matricula FROM matricula WHERE id_aluno = :id)", {"id": id_del})
                run_action("DELETE FROM frequencia WHERE id_matricula IN (SELECT id_matricula FROM matricula WHERE id_aluno = :id)", {"id": id_del})
                run_action("DELETE FROM matricula WHERE id_aluno = :id", {"id": id_del})
                success, msg = run_action("DELETE FROM aluno WHERE id_aluno = :id", {"id": id_del})
                
                if success:
                    st.success("Aluno removido!")
                    st.rerun()
                else:
                    st.error(f"Erro: {msg}")