import streamlit as st
import pandas as pd
from database import run_query

def render():
    st.header("Dashboard Estratégico")
    st.markdown("Visão geral do desempenho acadêmico e operacional da escola.")
    kpi_data = run_query("""
        SELECT 
            (SELECT COUNT(*) FROM aluno WHERE matricula_ativa = 1) as alunos_ativos,
            (SELECT COUNT(*) FROM professor) as total_profs,
            (SELECT COUNT(*) FROM turma) as total_turmas,
            (SELECT COALESCE(AVG(valor), 0) FROM nota) as media_geral_escola
    """)
    freq_data = run_query("""
        SELECT 
            SUM(CASE WHEN presente = 1 THEN 1 ELSE 0 END) as presencas,
            COUNT(*) as total_aulas
        FROM frequencia
    """)

    if not kpi_data.empty:
        dados = kpi_data.iloc[0]
        
        presencas = freq_data.iloc[0]['presencas'] if not freq_data.empty else 0
        total_aulas = freq_data.iloc[0]['total_aulas'] if not freq_data.empty else 0
        taxa_freq = (presencas / total_aulas * 100) if total_aulas > 0 else 0
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Alunos Ativos", dados['alunos_ativos'], delta="Matriculados")
        c2.metric("Turmas Abertas", dados['total_turmas'], delta=f"{dados['total_profs']} Profs")

        media = float(dados['media_geral_escola'])
        delta_media = "Acima da meta (6.0)" if media >= 6 else "Abaixo da meta"
        c3.metric("Média Global (Notas)", f"{media:.2f}", delta=delta_media)
        delta_freq = "Boa" if taxa_freq >= 75 else "Crítica (<75%)"
        c4.metric("Frequência Global", f"{taxa_freq:.1f}%", delta=delta_freq)

    st.markdown("---")
    st.subheader("Radar de Risco (Alunos com Média Baixa)")
    df_risco = run_query("""
        SELECT a.nome AS Aluno, d.nome AS Disciplina, ROUND(AVG(n.valor), 2) AS Media_Atual
        FROM nota n
        JOIN matricula m ON n.id_matricula = m.id_matricula
        JOIN aluno a ON m.id_aluno = a.id_aluno
        JOIN turma t ON m.id_turma = t.id_turma
        JOIN disciplina d ON t.id_disciplina = d.id_disciplina
        GROUP BY a.id_aluno, d.id_disciplina
        HAVING Media_Atual < 6.0
        ORDER BY Media_Atual ASC
        LIMIT 5
    """)
    
    if not df_risco.empty:
        st.error("Atenção! Os seguintes alunos estão com desempenho crítico:")
        st.table(df_risco)
    else:
        st.success("Ótimo! Nenhum aluno com média abaixo de 6.0 detectado no momento.")