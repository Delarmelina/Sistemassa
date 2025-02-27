import streamlit as st
from utils.get_globals import set_restaurante, set_usuario_id, get_usuario_id
from db.functions.db_login import verificar_login

if get_usuario_id() is not None:
    set_restaurante(None)
    set_usuario_id(None)
    st.rerun()
else:
    print(get_usuario_id())
    st.switch_page("pages/Home/Home.py")