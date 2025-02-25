import streamlit as st
from utils.get_globals import set_restaurante, set_usuario_id, get_usuario_id
from db.functions.db_login import verificar_login

# if get_usuario_id() is None:
#     login = st.text_input("Login")
#     senha = st.text_input("Senha", type="password")

#     if st.button("Entrar"):
#         st.switch_page("Paginas/Home/Home.py")
#     else:
#         st.write("Usuário ou senha incorretos!")

if get_usuario_id() is not None:
    set_restaurante(None)
    set_usuario_id(None)

st.switch_page("Paginas/Home/Home.py")
st.rerun()