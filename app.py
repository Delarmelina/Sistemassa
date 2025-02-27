import streamlit as st
from db.database_structure import criar_banco
from utils.get_globals import get_restaurante, get_usuario_id
from db.functions.db_login import verificar_login
from pages.main import render as main_render

# Configurar o layout para abrir sempre em wide mode
st.set_page_config(
    page_title="Gerenciamento de Produtos",
    layout="wide"  # Define o layout como "wide"
)

# Inicialização do banco de dados
#criar_banco()

#Verificar se o Usuário está logado
if get_usuario_id() is None:
    login = st.text_input("Usuário", key="usuario")
    password = st.text_input("Senha", key="senha", type="password")
    if st.button("Entrar"):
        if (verificar_login(login, password) == True):
            st.success("Login efetuado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos!")
main_render()