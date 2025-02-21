import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from db.functions.db_restaurantes import obter_restaurantes
from db.functions.db_login import obter_user_restaurante_by_id, alterar_permissoes

@st.dialog("Selecione os restaurantes permitidos")
def abrir_modal_perm(id, login):
    st.write("Permissões do usuário: " + login)
    user_restaurante = [item for sublista in obter_user_restaurante_by_id(int(id)) for item in sublista]   

    restaurantes = obter_restaurantes()
    df = pd.DataFrame(restaurantes, columns=["ID", "Restaurante"])

    # Encontra os índices dos restaurantes que o usuário já tem permissão
    selected_indices = df[df["ID"].isin(user_restaurante)].index.tolist()

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection("multiple", use_checkbox=True, pre_selected_rows=[selected_indices])  # Configura seleção de várias linhas
    grid_options = gb.build()

    # Criar a grade interativa
    grid_response = AgGrid(df, gridOptions=grid_options, height=300, width="100%", theme="streamlit")

    # Obtém a linha selecionada corretamente
    linha_selecionada = grid_response["selected_rows"]

    # Verifica se há uma linha selecionada e se o botão foi pressionado
    if st.button("Adicionar") and linha_selecionada["ID"].iloc[0] is not None:
        alterar_permissoes(id, linha_selecionada["ID"].tolist())
        st.rerun()