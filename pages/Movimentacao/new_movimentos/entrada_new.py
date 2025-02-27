import streamlit as st
import pandas as pd
from db.functions.db_config import obter_categorias, obter_unidades, obter_subcategorias_por_categoria
from db.functions.db_produtos import inserir_produto
from utils.modals.modal_select import abrir_selecao

def render():

    if "data" not in st.session_state:
        st.session_state.data = {"ID Produto": [], "Produto": [], "Quantidade": []}

    # Campos do formulário
    nome = st.text_input("Nome do Produto")
    categoria = st.selectbox("Categoria", obter_categorias(), format_func=lambda x: x[1])
    subcategoria = st.selectbox("Subcategoria", obter_subcategorias_por_categoria(categoria[0]), format_func=lambda x: x[1])
    estoque = st.number_input("Estoque Inicial", min_value=0, step=1)
    unidade = st.selectbox("Unidade", obter_unidades(), format_func=lambda x: x[1])
    descricao = st.text_area("Descrição")
    receita = st.checkbox("Este produto é uma receita!")

    resultado = None
    if st.button("Adicionar produto"):
        resultado = inserir_produto(nome, categoria[0], subcategoria[0], unidade[0], estoque, descricao, st.session_state.quant, st.session_state.data)
        st.rerun()
    if resultado == True:
        st.success("Produto adicionado com sucesso!")
    elif resultado is not None:
        st.write("Erro ao adicionar produto:", resultado)
        

    # Criar layout com duas colunas (3 para a tabela, 2 para o formulário)
    col_linha1, col_linha2, col_linha3 = st.columns([1, 1, 4])
    st.divider()
    col_tabela, col_form = st.columns([3, 2])
    st.divider()

    # Entrada para Quantidade Produzida
    with col_linha1:
        st.session_state.quant = st.number_input("Quantidade Produzida:", min_value=0.0, format="%.2f")

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
        dataframe_placeholder.dataframe(df, use_container_width=True, hide_index=True, height=200)

    with col_form:
        st.subheader("Adicionar Item")

        if "produto_selecionada" in st.session_state:
            st.write("Produto selecionado: " + str(st.session_state.produto_selecionada))
        else:
            st.write("Nenhum produto selecionado")

        if st.button("Selecionar produto", key="botao_pesquisa", use_container_width=True):
            abrir_selecao("produto")                   

        quantidade_sel_receita = st.number_input("Quantidade:", min_value=0.0, format="%.2f", step=1.0)

        if st.button("Adicionar item", use_container_width=True):
            if st.session_state.produto_selecionada and quantidade_sel_receita>0.0:
                # Adiciona item à sessão e atualiza DataFrame
                st.session_state.data["ID Produto"].append(len(st.session_state.data["ID Produto"]) + 1)
                st.session_state.data["Produto"].append(st.session_state.produto_selecionada)
                st.session_state.data["Quantidade"].append(quantidade_sel_receita)
                st.success("Item adicionado com sucesso!")

                # Atualiza tabela
                df = pd.DataFrame(st.session_state.data)
                dataframe_placeholder.dataframe(df, use_container_width=True, hide_index=True, height=300)
                st.session_state.produto_selecionada = None
                st.rerun()
            else:
                st.error("Selecione um produto e insira uma quantidade válida!")