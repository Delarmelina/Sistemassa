import streamlit as st
from db.functions.db_produtos import obter_produtos, deletar_produto
from db.functions.db_movimentacao import obter_movimentacoes
from db.functions.db_config import obter_categorias, obter_subcategorias, obter_unidades, obter_subcategorias_por_categoria
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from pages.Cadastros.default_new.Produtos_new import render as Render_dados_produtos


#------------------------------------------------------------
# Funções, auxiliares e Popups

if 'linha_selecionada' not in st.session_state:
    st.session_state['linha_selecionada'] = True

st.title("Entradas de produtos")
st.write("Página para gerenciar entradas de produtos no estoque")

# Obter os entradas do banco de dados
entradas = obter_movimentacoes()
# Tratar os dados do dataframe de entradas
colunas = ["ID", "Tipo", "Data", "Restaurante", "Destino", "Fornecedor", "Observações"] # Set das colunas do dataframe
df_entradas = pd.DataFrame(entradas, columns=colunas) # Variavel do dataframe grado

gb = GridOptionsBuilder.from_dataframe(df_entradas)
gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
gb.configure_pagination(paginationAutoPageSize=True)  # Configura paginação
gb.configure_side_bar()  # Configura barra lateral
gb.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
gb.configure_default_column(resizable=True, flex=1)
grid_options = gb.build()

tab1, tab2 = st.tabs(["Entradas", 'Nova entrada'])

# Renderizando a tabela

with tab1:
    grid_response = AgGrid(
        df_entradas,
        gridOptions=grid_options,
        height=300,
        fit_columns_on_grid_load=True,
        width="100%",
        theme="streamlit",  # Temas: "streamlit", "dark", "light", etc.
    )

    linha_selecionada = grid_response["selected_rows"]

    # Botões das funções
    col2, col3, col4 = st.columns(3)
    if col2.button("Excluir Entrada", use_container_width=True, disabled=linha_selecionada is None):
        # resultado = deletar_entrada(linha_selecionada["ID"].iloc[0])
        resultado = True
        if resultado == True:
            st.rerun()
        elif resultado is not None:
            st.write("Erro ao excluir ebtrada:", resultado)
    if col3.button("Editar Entrada", use_container_width=True, disabled=linha_selecionada is None):
        print("Alterar entrada")
with tab2:
    Render_dados_produtos()