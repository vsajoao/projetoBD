import streamlit as st
import pandas as pd
from database import run_query

def render():
    st.header("📄 Boletim Escolar Completo")
    
    # 1. Filtro: Selecionar Aluno
    alunos = run_query("SELECT id_aluno, nome FROM aluno ORDER BY nome")
    
    if alunos.empty:
        st.warning("Nenhum aluno cadastrado no sistema.")
        return

    # Cria o mapa Nome -> ID
    aluno_dict = {row['nome']: row['id_aluno'] for _, row in alunos.iterrows()}
    
    # Layout do filtro
    col_sel, col_vazio = st.columns([1, 2])
    with col_sel:
        nome_selecionado = st.selectbox("Selecione o Aluno:", list(aluno_dict.keys()))
        id_aluno = aluno_dict[nome_selecionado]
    
    # 2. Buscar dados na View
    sql = f"SELECT * FROM vw_boletim_completo WHERE id_aluno = {id_aluno}"
    df = run_query(sql)
    
    if df.empty:
        st.info(f"O aluno **{nome_selecionado}** não possui matrículas ou registros acadêmicos.")
        return

    st.markdown("---")

    # 3. Cabeçalho do Aluno (Foto + Resumo Global)
    col_perfil, col_resumo = st.columns([1, 4])
    
    with col_perfil:
        # Tenta pegar a foto da primeira linha
        foto_blob = df.iloc[0]['Aluno_Foto']
        if foto_blob:
            st.image(foto_blob, width=150, caption="Foto de Perfil")
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120, caption="Sem Foto")

    with col_resumo:
        st.subheader(f"Aluno: {df.iloc[0]['Aluno_Nome']}")
        st.write(f"📧 Email: {df.iloc[0]['Aluno_Email']}")
        
        # --- Cálculo de Métricas Gerais ---
        media_global = df['Media_Final'].mean()
        
        # Tratamento seguro para valores nulos/None vindo do banco
        df['Total_Aulas_Registradas'] = df['Total_Aulas_Registradas'].fillna(0)
        df['Total_Presencas'] = df['Total_Presencas'].fillna(0)
        
        total_aulas_geral = df['Total_Aulas_Registradas'].sum()
        total_presencas_geral = df['Total_Presencas'].sum()
        
        if total_aulas_geral > 0:
            freq_global = (total_presencas_geral / total_aulas_geral) * 100
        else:
            freq_global = 100.0 # Sem aulas = 100% de presença teórica
            
        m1, m2, m3 = st.columns(3)
        m1.metric("Média Geral", f"{media_global:.2f}")
        m2.metric("Frequência Global", f"{freq_global:.1f}%")
        m3.metric("Disciplinas", len(df))

    st.divider()

    # 4. Detalhes por Disciplina
    st.subheader("Desempenho por Disciplina")
    
    for index, row in df.iterrows():
        # Definição de cores e ícones baseados no status
        status = row['Situacao_Matricula']
        icone = "🔵" # Cursando
        if status == 'APROVADO': icone = "🟢"
        elif status == 'REPROVADO': icone = "🔴"
        
        # CORREÇÃO DO ERRO: Garantir que se for None, vira 0
        aulas_mat = row['Total_Aulas_Registradas'] if pd.notna(row['Total_Aulas_Registradas']) else 0
        presencas_mat = row['Total_Presencas'] if pd.notna(row['Total_Presencas']) else 0
        
        # Evita divisão por zero
        perc_freq = 0.0
        if aulas_mat > 0:
            perc_freq = (presencas_mat / aulas_mat) * 100
        else:
            perc_freq = 100.0

        # Título do Expander
        titulo_expander = f"{icone} **{row['Disciplina']}** | Média: **{row['Media_Final']}** | Status: **{status}**"
        
        with st.expander(titulo_expander):
            c1, c2, c3 = st.columns(3)
            
            # Coluna 1: Dados da Turma
            with c1:
                st.markdown("###### 🏫 Informações")
                st.write(f"**Professor:** {row['Professor']}")
                st.write(f"**Sala:** {row['Sala']}")
                st.write(f"**Período:** {row['Periodo']}")
            
            # Coluna 2: Detalhe das Notas
            with c2:
                st.markdown("###### 📝 Notas Parciais")
                if row['Detalhe_Notas']:
                    notas_lista = row['Detalhe_Notas'].split(' | ')
                    for nota_txt in notas_lista:
                        st.text(f"• {nota_txt}")
                else:
                    st.caption("Nenhuma nota lançada ainda.")
            
            # Coluna 3: Frequência Visual
            with c3:
                st.markdown("###### 📅 Frequência")
                st.progress(int(perc_freq) / 100, text=f"{perc_freq:.1f}% de Presença")
                # Aqui estava o erro: agora usamos as variáveis tratadas 'presencas_mat' e 'aulas_mat'
                st.caption(f"{int(presencas_mat)} presenças em {int(aulas_mat)} aulas registradas.")
                
                if perc_freq < 75 and aulas_mat > 0:
                    st.error("⚠️ Risco de Reprovação por Faltas (<75%)")