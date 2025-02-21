import streamlit as st
from db.functions.db_login import obter_usuarios, excluir_usuario
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from Paginas.Cadastros.default_new.Usuarios_new import render as Render_dados_usuarios
from utils.modals.modal_permissions import abrir_modal_perm


#------------------------------------------------------------
# Funções, auxiliares e Popups

if 'linha_selecionada' not in st.session_state:
    st.session_state['linha_selecionada'] = True

st.title("Usuários")
st.write("Página para gerenciar todos os usuários do sistema.")

# Obter os usuarios do banco de dados
usuarios = obter_usuarios()
colunas = ["ID", "Login"] # Set das colunas do dataframe
df_usuarios = pd.DataFrame(usuarios, columns=colunas) # Variavel do dataframe grado

gb = GridOptionsBuilder.from_dataframe(df_usuarios)
gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
gb.configure_pagination(paginationAutoPageSize=True)  # Configura paginação
gb.configure_side_bar()  # Configura barra lateral
gb.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
gb.configure_default_column(resizable=True, flex=1)
grid_options = gb.build()

tab1, tab2 = st.tabs(["Usuários", 'Novo Usuário'])

# Renderizando a tabela

with tab1:
    grid_response = AgGrid(
        df_usuarios,
        gridOptions=grid_options,
        height=300,
        fit_columns_on_grid_load=True,
        width="100%",
        theme="streamlit",  # Temas: "streamlit", "dark", "light", etc.
    )

    linha_selecionada = grid_response["selected_rows"]

    # Botões das funções
    col2, col3, col4  = st.columns(3)
    if col2.button("Excluir usuario", use_container_width=True, disabled=linha_selecionada is None):
        resultado = excluir_usuario(linha_selecionada["ID"].iloc[0])
        if resultado == True:
            st.rerun()
        elif resultado is not None:
            st.write("Erro ao excluir usuario:", resultado)
    if col3.button("Editar usuario", use_container_width=True, disabled=linha_selecionada is None):
        print("Receita")
    if col4.button("Permissões", use_container_width=True, disabled=linha_selecionada is None):
        abrir_modal_perm(linha_selecionada["ID"].iloc[0], linha_selecionada["Login"].iloc[0])
with tab2:
    Render_dados_usuarios()