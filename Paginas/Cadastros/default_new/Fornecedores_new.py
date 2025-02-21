import streamlit as st
import pandas as pd
from db.functions.db_fornecedores import inserir_fornecedor

def render():
    # Campos do formulário
    nome = st.text_input("Nome do fornecedor")
    cnpj = st.text_input("CNPJ")
    contato = st.text_input("Contato")
    email = st.text_input("Email")

    resultado = None
    if st.button("Adicionar fornecedor"):
        resultado = inserir_fornecedor(nome, cnpj, contato, email)
        st.rerun()
    if resultado == True:
        st.success("fornecedor adicionado com sucesso!")
    elif resultado is not None:
        st.write("Erro ao adicionar fornecedor:", resultado)