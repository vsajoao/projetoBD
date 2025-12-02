import streamlit as st
from database import run_query, run_action

def render():
    st.header("Gerenciamento de Turmas")
    
    # Adicionada a aba "Editar Turma"
    tab1, tab2, tab3, tab4 = st.tabs(["Listar Turmas", "Nova Turma", "Editar Turma", "Excluir Turma"])
    
    # --- ABA 1: LISTAR (SEM ID) ---
    with tab1:
        st.subheader("Turmas Ativas")
        # Query ajustada para não trazer o ID, apenas nomes legíveis
        df = run_query("""
            SELECT d.nome as Disciplina, p.nome as Professor, 
                   s.numero_sala as Sala, t.ano as Ano, t.semestre as Semestre
            FROM turma t
            JOIN disciplina d ON t.id_disciplina = d.id_disciplina
            JOIN professor p ON t.id_prof = p.id_prof
            JOIN sala s ON t.id_sala = s.id_sala
            ORDER BY t.ano DESC, t.semestre DESC, d.nome ASC
        """)
        
        if not df.empty:
            # Formatação visual: Sem index e ajustado à largura
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma turma cadastrada.")

    # --- ABA 2: NOVA TURMA ---
    with tab2:
        st.subheader("Abrir Nova Turma")
        discs = run_query("SELECT id_disciplina, nome FROM disciplina")
        profs = run_query("SELECT id_prof, nome FROM professor")
        salas = run_query("SELECT id_sala, numero_sala, tipo FROM sala")
        
        if not discs.empty and not profs.empty and not salas.empty:
            with st.form("nova_turma_form"):
                c1, c2 = st.columns(2)
                ano = c1.number_input("Ano", value=2025, step=1)
                sem = c2.selectbox("Semestre", [1, 2])
                
                disc_map = {r['nome']: r['id_disciplina'] for _, r in discs.iterrows()}
                prof_map = {r['nome']: r['id_prof'] for _, r in profs.iterrows()}
                sala_map = {f"{r['numero_sala']} ({r['tipo']})": r['id_sala'] for _, r in salas.iterrows()}
                
                sel_d = st.selectbox("Disciplina", list(disc_map.keys()))
                sel_p = st.selectbox("Professor", list(prof_map.keys()))
                sel_s = st.selectbox("Sala", list(sala_map.keys()))
                
                if st.form_submit_button("Criar Turma"):
                    sql = "INSERT INTO turma (ano, semestre, id_disciplina, id_prof, id_sala) VALUES (:a, :s, :d, :p, :sl)"
                    params = {"a": ano, "s": sem, "d": disc_map[sel_d], "p": prof_map[sel_p], "sl": sala_map[sel_s]}
                    succ, msg = run_action(sql, params)
                    if succ: st.success("Turma criada!"); st.rerun()
                    else: st.error(msg)
        else:
            st.error("Cadastre Disciplinas, Professores e Salas antes.")

    # --- ABA 3: EDITAR TURMA (NOVO!) ---
    with tab3:
        st.subheader("Editar Turma")
        
        # 1. Selecionar Turma
        turmas = run_query("""
            SELECT t.id_turma, d.nome, t.ano, t.semestre 
            FROM turma t JOIN disciplina d ON t.id_disciplina = d.id_disciplina
            ORDER BY t.ano DESC, t.semestre DESC
        """)
        
        if not turmas.empty:
            t_dict = {f"{r['nome']} - {r['ano']}/{r['semestre']}": r['id_turma'] for _, r in turmas.iterrows()}
            turma_nome = st.selectbox("Selecione para Editar", list(t_dict.keys()), key="sel_edit_t")
            id_t = t_dict[turma_nome]
            
            # 2. Carregar dados atuais da turma
            dados = run_query(f"SELECT * FROM turma WHERE id_turma = {id_t}").iloc[0]
            
            # Carregar listas auxiliares
            discs = run_query("SELECT id_disciplina, nome FROM disciplina")
            profs = run_query("SELECT id_prof, nome FROM professor")
            salas = run_query("SELECT id_sala, numero_sala, tipo FROM sala")
            
            if not discs.empty and not profs.empty and not salas.empty:
                with st.form("edit_turma_form"):
                    c1, c2 = st.columns(2)
                    novo_ano = c1.number_input("Ano", value=int(dados['ano']), step=1)
                    # Hack para pegar index do semestre (0 ou 1)
                    idx_sem = 0 if dados['semestre'] == 1 else 1
                    novo_sem = c2.selectbox("Semestre", [1, 2], index=idx_sem)
                    
                    # Mapas de IDs
                    disc_map = {r['nome']: r['id_disciplina'] for _, r in discs.iterrows()}
                    prof_map = {r['nome']: r['id_prof'] for _, r in profs.iterrows()}
                    sala_map = {f"{r['numero_sala']} ({r['tipo']})": r['id_sala'] for _, r in salas.iterrows()}
                    
                    # Encontrar indices atuais para deixar selecionado
                    # (Lógica: busca a chave cujo valor é igual ao ID salvo no banco)
                    curr_disc_name = next(k for k, v in disc_map.items() if v == dados['id_disciplina'])
                    curr_prof_name = next(k for k, v in prof_map.items() if v == dados['id_prof'])
                    curr_sala_name = next(k for k, v in sala_map.items() if v == dados['id_sala'])
                    
                    idx_d = list(disc_map.keys()).index(curr_disc_name)
                    idx_p = list(prof_map.keys()).index(curr_prof_name)
                    idx_s = list(sala_map.keys()).index(curr_sala_name)
                    
                    sel_d = st.selectbox("Disciplina", list(disc_map.keys()), index=idx_d)
                    sel_p = st.selectbox("Professor", list(prof_map.keys()), index=idx_p)
                    sel_s = st.selectbox("Sala", list(sala_map.keys()), index=idx_s)
                    
                    if st.form_submit_button("Atualizar Turma"):
                        sql = """
                            UPDATE turma 
                            SET ano=:a, semestre=:s, id_disciplina=:d, id_prof=:p, id_sala=:sl 
                            WHERE id_turma=:id
                        """
                        params = {
                            "a": novo_ano, "s": novo_sem, 
                            "d": disc_map[sel_d], "p": prof_map[sel_p], "sl": sala_map[sel_s],
                            "id": id_t
                        }
                        succ, msg = run_action(sql, params)
                        if succ: st.success("Turma atualizada!"); st.rerun()
                        else: st.error(msg)
        else:
            st.info("Nenhuma turma para editar.")

    # --- ABA 4: EXCLUIR TURMA ---
    with tab4:
        st.subheader("Encerrar Turma")
        st.warning("⚠️ Isso apaga TUDO: matrículas, notas, frequências e avaliações desta turma.")
        
        turmas = run_query("SELECT t.id_turma, d.nome, t.ano, t.semestre FROM turma t JOIN disciplina d ON t.id_disciplina = d.id_disciplina")
        if not turmas.empty:
            t_map = {f"{r['nome']} - {r['ano']}/{r['semestre']}": r['id_turma'] for _, r in turmas.iterrows()}
            sel_del = st.selectbox("Selecione para Excluir", list(t_map.keys()), key="del_t")
            
            if st.button("Confirmar Exclusão"):
                id_t = t_map[sel_del]
                # Cascata completa
                run_action("DELETE FROM nota WHERE id_matricula IN (SELECT id_matricula FROM matricula WHERE id_turma = :id)", {"id": id_t})
                run_action("DELETE FROM frequencia WHERE id_matricula IN (SELECT id_matricula FROM matricula WHERE id_turma = :id)", {"id": id_t})
                run_action("DELETE FROM nota WHERE id_avaliacao IN (SELECT id_avaliacao FROM avaliacao WHERE id_turma = :id)", {"id": id_t})
                run_action("DELETE FROM avaliacao WHERE id_turma = :id", {"id": id_t})
                run_action("DELETE FROM matricula WHERE id_turma = :id", {"id": id_t})
                succ, msg = run_action("DELETE FROM turma WHERE id_turma = :id", {"id": id_t})
                
                if succ: st.success("Turma encerrada!"); st.rerun()
                else: st.error(msg)
        else:
            st.info("Nenhuma turma para excluir.")