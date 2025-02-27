import streamlit as st
from db.functions.db_config import obter_subcategorias
from utils.modals.modal_config import abrir_modal  # Substitua pelo módulo correto, se necessário

def render_tab():
    st.header("Subcategorias")
    subcategorias = obter_subcategorias()
    st.dataframe(subcategorias, use_container_width=True)

    if st.button("Criar Subcategoria"):
        abrir_modal("subcategoria")