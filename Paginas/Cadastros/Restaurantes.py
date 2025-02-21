import streamlit as st
from db.functions.db_restaurantes import obter_restaurantes, excluir_restaurante
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from Paginas.Cadastros.default_new.Restaurantes_new import render as Render_dados_restaurantes


#------------------------------------------------------------
# Funções, auxiliares e Popups

if 'linha_selecionada' not in st.session_state:
    st.session_state['linha_selecionada'] = True

st.title("Restaurantes")
st.write("Página para gerenciar todos os restaurantes cadastrados no sistema.")

# Obter os restaurantes do banco de dados
restaurantes = obter_restaurantes()
# Tratar os dados do dataframe de restaurantes
colunas = ["ID", "Nome"] # Set das colunas do dataframe
df_restaurantes = pd.DataFrame(restaurantes, columns=colunas) # Variavel do dataframe grado

gb = GridOptionsBuilder.from_dataframe(df_restaurantes)
gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
gb.configure_pagination(paginationAutoPageSize=True)  # Configura paginação
gb.configure_side_bar()  # Configura barra lateral
gb.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
gb.configure_default_column(resizable=True, flex=1)
grid_options = gb.build()

tab1, tab2 = st.tabs(["Restaurantes", 'Novo Restaurante'])

# Renderizando a tabela

with tab1:
    grid_response = AgGrid(
        df_restaurantes,
        gridOptions=grid_options,
        height=300,
        fit_columns_on_grid_load=True,
        width="100%",
        theme="streamlit",  # Temas: "streamlit", "dark", "light", etc.
    )

    linha_selecionada = grid_response["selected_rows"]

    # Botões das funções
    col2, col3  = st.columns(2)
    if col2.button("Excluir restaurante", use_container_width=True, disabled=linha_selecionada is None):
        resultado = excluir_restaurante(linha_selecionada["ID"].iloc[0])
        if resultado == True:
            st.rerun()
        elif resultado is not None:
            st.write("Erro ao excluir restaurante:", resultado)
    if col3.button("Editar restaurante", use_container_width=True, disabled=linha_selecionada is None):
        print("Receita")
with tab2:
    Render_dados_restaurantes()