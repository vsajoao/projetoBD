import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DatabaseError

def get_engine():
    return create_engine('mysql+mysqlconnector://root:root@localhost:3306/escola_db')

def run_query(query, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            return pd.read_sql(text(query), conn, params=params)
    except Exception as e:
        st.error(f"Erro na consulta: {e}")
        return pd.DataFrame()

def run_action(sql, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql), params)
        return True, "Sucesso"
    except DatabaseError as e:
        return False, str(e.orig)
    except Exception as e:
        return False, str(e)