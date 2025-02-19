import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from db.functions.db_config import obter_unidades
from db.functions.db_produtos import obter_produtos

@st.dialog("Selecionar opção")
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
        df = pd.DataFrame(produtos, columns=["ID", "produto"])

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
            st.session_state.produto_selecionada = linha_selecionada["produto"].iloc[0]
            st.rerun()

    return None  # Retorna None caso nada seja selecionado


            