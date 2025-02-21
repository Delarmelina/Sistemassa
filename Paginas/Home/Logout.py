import streamlit as st
from utils.get_globals import set_restaurante, set_usuario_id

set_restaurante(None)
set_usuario_id(None)
st.experimental_rerun()