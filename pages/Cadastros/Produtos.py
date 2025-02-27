import streamlit as st
from db.functions.db_produtos import obter_produtos, deletar_produto
from db.functions.db_config import obter_categorias, obter_subcategorias, obter_unidades, obter_subcategorias_por_categoria
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from pages.Cadastros.default_new.Produtos_new import render as Render_dados_produtos


#------------------------------------------------------------
# Funções, auxiliares e Popups

if 'linha_selecionada' not in st.session_state:
    st.session_state['linha_selecionada'] = True

st.title("Produtos")
st.write("Página para gerenciar produtos")

# Obter os produtos do banco de dados
produtos = obter_produtos()
# Tratar os dados do dataframe de produtos
produtos = [produto[:8] + produto[9:] for produto in produtos] # Obter apenas os dados relevantes
colunas = ["ID", "Nome", "Categoria", "Subcategoria", "Estoque", "Unidade", "Descrição", "Receita"] # Set das colunas do dataframe
df_produtos = pd.DataFrame(produtos, columns=colunas) # Variavel do dataframe grado
df_produtos['Receita'] = df_produtos['Receita'].apply(lambda x: "✅" if x > 0 else "⬜") # Setando o icone de receita baseado na quant. de produção

gb = GridOptionsBuilder.from_dataframe(df_produtos)
gb.configure_selection("single", use_checkbox=True)  # Configura seleção de uma única linha
gb.configure_pagination(paginationAutoPageSize=True)  # Configura paginação
gb.configure_side_bar()  # Configura barra lateral
gb.configure_grid_options(domLayout='autoHeight', autoSizeColumns=True)
gb.configure_default_column(resizable=True, flex=1)
grid_options = gb.build()

tab1, tab2 = st.tabs(["Produtos", 'Novo Produto'])

# Renderizando a tabela

with tab1:
    grid_response = AgGrid(
        df_produtos,
        gridOptions=grid_options,
        height=300,
        fit_columns_on_grid_load=True,
        width="100%",
        theme="streamlit",  # Temas: "streamlit", "dark", "light", etc.
    )

    linha_selecionada = grid_response["selected_rows"]

    # Botões das funções
    col2, col3, col4 = st.columns(3)
    if col2.button("Excluir Produto", use_container_width=True, disabled=linha_selecionada is None):
        resultado = deletar_produto(linha_selecionada["ID"].iloc[0])
        if resultado == True:
            st.rerun()
        elif resultado is not None:
            st.write("Erro ao excluir produto:", resultado)
    if col3.button("Editar Produto", use_container_width=True, disabled=linha_selecionada is None):
        print("Receita")
    if col4.button("Alterar Receita", use_container_width=True, disabled=not(linha_selecionada is not None and linha_selecionada["Receita"].iloc[0] == '✅')):
        print(st.session_state.linha_selecionada)
with tab2:
    Render_dados_produtos()