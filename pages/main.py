import streamlit as st
from utils.get_globals import get_usuario_id, get_restaurante
import utils.navigation_config as nav

def render():

    if get_usuario_id() is not None: # Está logado?
        if get_restaurante() is not None: # Restaurante Selecionado       
            if get_usuario_id() == 4: # É admin?
                pg = st.navigation(pages=nav.admin())
            else: # Não é admin
                pg = st.navigation(pages=nav.rest_selecionado())
        if get_restaurante() is None: # Restaurante não selecionado
            if get_usuario_id() == 4: # É admin?
                pg = st.navigation(pages=nav.admin_sem_restaurante())
            else: # Não é admin
                pg = st.navigation(pages=nav.rest_nao_selecionado())
    else:
        pg = st.navigation(pages=nav.unloged(), position="hidden")

    # Testar execução
    try:
        pg.run()
    except Exception as e:
        st.error(f"Erro ao executar: {e}")