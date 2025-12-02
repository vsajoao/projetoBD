import streamlit as st
from telas import dashboard, alunos, matriculas, notas, boletim, fechamento, frequencia, disciplinas, salas, avaliacoes, turmas

st.set_page_config(page_title="Sistema Escolar", layout="wide")

st.title("Sistema de Gestão Escolar")
st.markdown("---")

MENU_STRUCTURE = {
    "Início": {
        "Dashboard Geral": dashboard
    },
    "Secretaria": {
        "Gerenciar Salas": salas,
        "Gerenciar Disciplinas": disciplinas,
        "Gerenciar Turmas": turmas,
        "Gerenciar Alunos": alunos,
        "Nova Matrícula": matriculas
    },
    "Área do Professor": {
        "Frequência (Chamada)": frequencia,
        "Avaliações": avaliacoes,
        "Lançar Notas": notas
    },
    "Relatórios & Fechamento": {
        "Boletim": boletim,
        "Fechar Semestre": fechamento
    }
}

st.sidebar.title("Navegação")

categoria_selecionada = st.sidebar.selectbox(
    "Selecione o Módulo:",
    list(MENU_STRUCTURE.keys())
)

st.sidebar.markdown("---")

pagina_selecionada_nome = st.sidebar.radio(
    "Funcionalidade:",
    list(MENU_STRUCTURE[categoria_selecionada].keys())
)

modulo_pagina = MENU_STRUCTURE[categoria_selecionada][pagina_selecionada_nome]
modulo_pagina.render()

st.sidebar.markdown("---")
st.sidebar.caption("Projeto BD 2025.2")