import streamlit as st
import pandas as pd
from database import run_query, run_action

def render():
    st.header("🔒 Fechamento de Semestre (Procedure)")
    
    # 1. Selecionar Aluno
    alunos = run_query("SELECT id_aluno, nome FROM aluno ORDER BY nome")
    
    if not alunos.empty:
        aluno_dict = {row['nome']: row['id_aluno'] for _, row in alunos.iterrows()}
        nome_aluno = st.selectbox("Selecione o Aluno:", list(aluno_dict.keys()))
        id_aluno_sel = aluno_dict[nome_aluno]
        
        # 2. Selecionar Disciplina/Matrícula do Aluno
        # Buscamos as matrículas desse aluno para saber o que fechar
        matriculas = run_query(f"""
            SELECT m.id_matricula, d.nome as disciplina, m.status, t.ano, t.semestre
            FROM matricula m
            JOIN turma t ON m.id_turma = t.id_turma
            JOIN disciplina d ON t.id_disciplina = d.id_disciplina
            WHERE m.id_aluno = {id_aluno_sel}
        """)
        
        if not matriculas.empty:
            st.divider()
            
            # Criação do dicionário para o selectbox
            # Ex: "Matemática (2025/1) - Status: CURSANDO"
            mat_opcoes = {
                f"{row['disciplina']} ({row['ano']}/{row['semestre']}) - Status Atual: {row['status']}": row['id_matricula'] 
                for _, row in matriculas.iterrows()
            }
            
            materia_label = st.selectbox("Selecione a Disciplina para encerrar:", list(mat_opcoes.keys()))
            id_matricula_final = mat_opcoes[materia_label]
            
            # Botão de Ação
            if st.button("Processar Fechamento", type="primary"):
                with st.spinner("Executando cálculos no banco de dados..."):
                    # 1. Executa a Procedure
                    sql = "CALL sp_atualizar_status_aluno(:id)"
                    success, msg = run_action(sql, {"id": id_matricula_final})
                    
                    if success:
                        # 2. Busca os dados atualizados para mostrar o resultado ao usuário
                        # Usamos a view completa que criamos antes para facilitar
                        dados_finais = run_query(f"""
                            SELECT Media_Final, Total_Aulas_Registradas, Total_Presencas, Situacao_Matricula 
                            FROM vw_boletim_completo 
                            WHERE id_matricula = {id_matricula_final}
                        """)
                        
                        if not dados_finais.empty:
                            res = dados_finais.iloc[0]
                            novo_status = res['Situacao_Matricula']
                            media_final = res['Media_Final']
                            
                            # Cálculo visual da frequência para explicar ao usuário
                            aulas = res['Total_Aulas_Registradas']
                            presencas = res['Total_Presencas']
                            freq_perc = (presencas / aulas * 100) if aulas > 0 else 100.0
                            
                            # Exibição do Resultado
                            st.markdown("### 📊 Resultado do Processamento")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Média Final", f"{media_final:.2f}")
                            col2.metric("Frequência", f"{freq_perc:.1f}%")
                            
                            # Feedback colorido dependendo do status
                            if novo_status == 'APROVADO':
                                st.success(f"✅ Sucesso! O aluno foi **{novo_status}**.")
                                st.balloons()
                            elif novo_status == 'REPROVADO POR FALTA':
                                st.error(f"🚫 O aluno foi **{novo_status}**.")
                                st.warning(f"A frequência de {freq_perc:.1f}% é inferior ao mínimo exigido (75%).")
                            elif novo_status == 'REPROVADO POR NOTA':
                                st.error(f"❌ O aluno foi **{novo_status}**.")
                                st.warning(f"A média {media_final:.2f} é inferior ao mínimo exigido (6.0).")
                            else:
                                st.info(f"Status atualizado para: {novo_status}")
                        else:
                            st.warning("Procedure executada, mas não foi possível ler os dados de retorno.")
                            
                    else:
                        st.error(f"Erro ao executar a procedure: {msg}")
        else:
            st.warning("Este aluno não está matriculado em nenhuma turma.")
    else:
        st.warning("Nenhum aluno cadastrado.")