import streamlit as st
from db.functions.db_produtos import obter_produtos
from db.functions.db_config import obter_categorias, obter_subcategorias, obter_unidades, obter_subcategorias_por_categoria
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.modals.modal_select import abrir_selecao


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
            # Configuração inicial da aba de Receita
            st.title("Aba de Receita")

            # Entrada para Quantidade Produzida
            col1, col2 = st.columns([2, 2])

            with col1:
                quantidade_produzida = st.number_input("Quantidade Produzida:", min_value=0.0, format="%.2f")

            with col2:
                unidade_var = st.text_input("Unidade", unidade[1], disabled=True)  # Valor padrão: "kg"

            # Dados simulados para exibição na tabela
            if "data" not in st.session_state:
                st.session_state.data = {"ID Produto": [], "Produto": [], "Quantidade": []}
            # Criar DataFrame para exibir como tabela
            df = pd.DataFrame(st.session_state.data)

            # Criar espaço reservado para o DataFrame
            dataframe_placeholder = st.empty()

            with st.expander("Adicionar item na receita"):
                formcol1, formcol2 = st.columns(2)
                with formcol1:
                    produto_sel_receita = st.text_input("Produto:")
                    quantidade_sel_receita = st.number_input("Quantidade:", min_value=0.0, format="%.2f", step=1.0)
                with formcol2:
                    if st.button("SP"):
                        unidade_selecionada = abrir_selecao("unidade")
                        st.write(unidade_selecionada)
                if st.button("Adicionar item", use_container_width=True):
                    if produto_sel_receita:
                        # Adicionar dados ao DataFrame no estado da sessão
                        st.session_state.data["ID Produto"].append(123)
                        st.session_state.data["Produto"].append(produto_sel_receita)
                        st.session_state.data["Quantidade"].append(quantidade_sel_receita)
                        st.success("Item adicionado com sucesso!")
                        df = pd.DataFrame(st.session_state.data)
                        dataframe_placeholder.dataframe(df, use_container_width=True)
            dataframe_placeholder.dataframe(df, use_container_width=True)