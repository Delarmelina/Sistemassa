import streamlit as st
from db.functions.db_config import obter_unidades
from utils.modals.modal_config import abrir_modal  # Substitua pelo módulo correto, se necessário

def render_tab():
    st.header("Unidades")
    unidades = obter_unidades()
    st.dataframe(unidades, use_container_width=True)

    if st.button("Criar Unidade"):
        abrir_modal("unidade")
