import streamlit as st
from db.functions.db_config import obter_categorias
from utils.modals.modal_config import abrir_modal  # Substitua pelo módulo correto, se necessário

def render_tab():
    st.header("Categorias")
    categorias = obter_categorias()
    st.dataframe(categorias, use_container_width=True)

    if st.button("Criar Categoria"):
        abrir_modal("categoria")
