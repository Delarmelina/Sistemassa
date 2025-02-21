import streamlit as st
from db.functions.db_login import inserir_usuario

def render():

    # Campos do formulário
    nome = st.text_input("Nome do Usuário")
    senha = st.text_input("Senha", type="password")

    resultado = None
    if st.button("Adicionar usuario"):
        resultado = inserir_usuario(nome, senha)
        st.rerun()
    if resultado == True:
        st.success("usuario adicionado com sucesso!")
    elif resultado is not None:
        st.write("Erro ao adicionar usuario:", resultado)