import streamlit as st
from db.functions.db_config import obter_categorias, obter_subcategorias, obter_unidades
from db.functions.db_config import inserir_categoria, inserir_subcategoria, inserir_unidade
from Paginas.Config.tab_unidade import render_tab as Render_Unidades
from Paginas.Config.tab_categoria import render_tab as Render_Categorias
from Paginas.Config.tab_subcategoria import render_tab as Render_Subcategorias

tab1, tab2, tab3 = st.tabs(["Categorias", "Subcategorias", "Unidades"])

with tab1:
    Render_Categorias()
with tab2:
    Render_Subcategorias()
with tab3:
    Render_Unidades()

