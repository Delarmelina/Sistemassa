import streamlit as st
from db.functions.db_produtos import obter_produtos
from db.functions.db_config import obter_categorias, obter_subcategorias, obter_unidades, obter_subcategorias_por_categoria
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.modals.modal_select import abrir_selecao

# Estilo CSS para alinhar o botão de lupa ao lado esquerdo do input
st.markdown("""
    <style>
        .input-container {
            display: flex;
            align-items: center;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
            width: 100%;
            background-color: white;
        }
        .input-container input {
            border: none;
            outline: none;
            flex-grow: 1;
            font-size: 16px;
            padding-left: 5px;
        }
        .search-button {
            background: none;
            border: none;
            cursor: pointer;
            padding: 5px;
        }
    </style>
""", unsafe_allow_html=True)

def render():
    tab1, tab2 = st.tabs(["Produto", "Receita"])
    with tab1:
        # Campos do formulário
        nome = st.text_input("Nome do Produto")
        categoria = st.selectbox("Categoria", obter_categorias(), format_func=lambda x: x[1])
        subcategoria = st.selectbox("Subcategoria", obter_subcategorias_por_categoria(categoria[0]), format_func=lambda x: x[1])
        estoque = st.number_input("Estoque Inicial", min_value=0, step=1)
        unidade = st.selectbox("Unidade", obter_unidades(), format_func=lambda x: x[1])
        descricao = st.text_area("Descrição")
        receita = st.checkbox("Este produto é uma receita!")

        if st.button("Teste"):
            st.write("Produto adicionado com sucesso!")
            print(str(nome) + " - " + str(categoria) + " - " + str(subcategoria) + " - " + str(estoque) + " - " + str(unidade) + " - " + str(descricao) + " - " + str(receita) )
            st.rerun()
    with tab2:
        if not(receita):
            st.write("Esse produto não possui uma receita!")
        else:
            # Criar layout com duas colunas (3 para a tabela, 2 para o formulário)
            col_linha1, col_linha2, col_linha3 = st.columns([1, 1, 4])
            st.divider()
            col_tabela, col_form = st.columns([3, 2])
            st.divider()

            # Entrada para Quantidade Produzida
            with col_linha1:
                quantidade_produzida = st.number_input("Quantidade Produzida:", min_value=0.0, format="%.2f")

            with col_linha2:
                st.text_input("Unidade", unidade[1], disabled=True)  # Valor padrão: "kg"

            # Inicializa dados na sessão
            if "data" not in st.session_state:
                st.session_state.data = {"ID Produto": [], "Produto": [], "Quantidade": []}

            # Criar DataFrame
            df = pd.DataFrame(st.session_state.data)

            # Layout dividido: Tabela à esquerda, Formulário à direita
            with col_tabela:
                st.subheader("Receita")
                dataframe_placeholder = st.empty()
                dataframe_placeholder.dataframe(df, use_container_width=True)

            with col_form:
                st.subheader("Adicionar Item")

                # Criar input estilizado
                produto_sel_receita = st.text_input("Produto:", key="produto", label_visibility="collapsed")

                # Botão de busca embutido
                col1, col2 = st.columns([0.1, 0.9])  # Define a largura do botão e do campo de entrada
                with col1:
                    if st.button("🔍", key="botao_pesquisa"):
                        abrir_selecao("unidade")
                with col2:
                    st.text_input("Produto:", key="produto2", value=produto_sel_receita, label_visibility="collapsed")

                quantidade_sel_receita = st.number_input("Quantidade:", min_value=0.0, format="%.2f", step=1.0)

                if st.button("Adicionar item", use_container_width=True):
                    if produto_sel_receita:
                        # Adiciona item à sessão e atualiza DataFrame
                        st.session_state.data["ID Produto"].append(len(st.session_state.data["ID Produto"]) + 1)
                        st.session_state.data["Produto"].append(produto_sel_receita)
                        st.session_state.data["Quantidade"].append(quantidade_sel_receita)
                        st.success("Item adicionado com sucesso!")

                        # Atualiza tabela
                        df = pd.DataFrame(st.session_state.data)
                        dataframe_placeholder.dataframe(df, use_container_width=True)