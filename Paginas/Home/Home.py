import streamlit as st
from utils.get_globals import get_restaurante, get_usuario_id
from db.functions.db_restaurantes import obter_restaurante_pelo_id
from db.functions.db_login import obter_usuario_by_id

st.title("Home PAGE")
st.write("Página principal do sistema!")

restaurante = get_restaurante()
usuario = get_usuario_id()

if usuario is not None:
    st.write("Usuário logado: " + obter_usuario_by_id(usuario)[1])
else:
    st.write("Usuário não logado")

if restaurante is not None:
    st.write("Restaurante logado: " +  obter_restaurante_pelo_id(restaurante)[1])
else:
    st.write("Restaurante não selecionado")