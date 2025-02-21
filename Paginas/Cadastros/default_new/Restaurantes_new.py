import streamlit as st
import pandas as pd
from db.functions.db_config import obter_categorias, obter_unidades, obter_subcategorias_por_categoria
from db.functions.db_restaurantes import inserir_restaurante
from utils.modals.modal_select import abrir_selecao

def render():

    # Campos do formulário
    nome = st.text_input("Nome do restaurante")

    resultado = None
    if st.button("Adicionar restaurante"):
        resultado = inserir_restaurante(nome)
        st.rerun()
    if resultado == True:
        st.success("restaurante adicionado com sucesso!")
    elif resultado is not None:
        st.write("Erro ao adicionar restaurante:", resultado)