import streamlit as st
from db.functions.db_config import obter_categorias
from db.functions.db_config import inserir_categoria, inserir_subcategoria, inserir_unidade

@st.dialog("Adicionar configuração")
def abrir_modal(tab):
    if (tab == "categoria"):
        categoria = st.text_input("Categoria")
        if st.button("Criar"):
            if categoria == "":
                st.write("Favor preencher todos os campos!")
            else:
                inserir_categoria(categoria)
                st.rerun()
    elif (tab == "subcategoria"):
        categoria = st.selectbox("Categoria", obter_categorias(), format_func=lambda x: x[1])
        subcategoria = st.text_input("Subcategoria")
        if st.button("Criar"):
            if categoria[0] == "" or subcategoria == "":
                st.write("Favor preencher todos os campos!")
            else:
                inserir_subcategoria(subcategoria, categoria[0])
                st.rerun()
    elif (tab == "unidade"):
        unidade = st.text_input("Unidade")
        if st.button("Criar"):
            if unidade == "":
                st.write("Favor preencher todos os campos!")
            else:
                inserir_unidade(unidade)
                st.rerun()