import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from db.functions.db_config import obter_unidades
from db.functions.db_produtos import obter_produtos
from db.functions.db_restaurantes import obter_restaurantes_by_user
from utils.get_globals import set_restaurante

@st.dialog("Selecionar opção", width="large")
def abrir_selecao(tab):
    if tab == "unidade":
        unidades = obter_unidades()
        df = pd.DataFrame(unidades, columns=["ID", "Unidade"])

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
        grid_options = gb.build()

        # Criar a grade interativa
        grid_response = AgGrid(df, gridOptions=grid_options, height=300, width="100%", theme="streamlit")

        # Obtém a linha selecionada corretamente
        linha_selecionada = grid_response["selected_rows"]

        # Verifica se há uma linha selecionada e se o botão foi pressionado
        if st.button("Adicionar") and linha_selecionada["ID"].iloc[0] is not None:
            # Gravar no session state
            st.session_state.unidade_selecionada = linha_selecionada["Unidade"].iloc[0]
            st.rerun()
    elif tab == "produto":
        produtos = obter_produtos()
        produtos = [produto[:4] + produto[5:7] + produto[8:] for produto in produtos]  # Obter apenas os dados relevantes
        df = pd.DataFrame(produtos, columns=["ID", "Produto", "Categoria", "Subcategoria", "Unidade", "Descrição"])

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
        gb.configure_pagination(paginationAutoPageSize=True)  # Configura paginação
        grid_options = gb.build()

        # Criar a grade interativa
        grid_response = AgGrid(df, gridOptions=grid_options, height=300, width="100%", theme="streamlit")

        # Obtém a linha selecionada corretamente
        linha_selecionada = grid_response["selected_rows"]

        # Verifica se há uma linha selecionada e se o botão foi pressionado
        if st.button("Adicionar") and linha_selecionada["ID"].iloc[0] is not None:
            # Gravar no session state
            st.session_state.produto_selecionada = linha_selecionada["Produto"].iloc[0]
            st.rerun()
    elif tab == "restaurante_selecao":
        restaurantes = obter_restaurantes_by_user()
        df = pd.DataFrame(restaurantes, columns=["ID", "Restaurante"])

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
        gb.configure_pagination(paginationAutoPageSize=True)  # Configura paginação
        grid_options = gb.build()

        # Criar a grade interativa
        grid_response = AgGrid(df, gridOptions=grid_options, height=300, width="100%", theme="streamlit")

        # Obtém a linha selecionada corretamente
        linha_selecionada = grid_response["selected_rows"]

        if st.button("Selecionar") and linha_selecionada["ID"].iloc[0] is not None:
            set_restaurante(linha_selecionada["ID"].iloc[0])
            st.switch_page("pages/Home/Home.py")
    return None  # Retorna None caso nada seja selecionado


            