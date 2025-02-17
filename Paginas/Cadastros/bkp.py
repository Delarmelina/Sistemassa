import streamlit as st
from db.functions.db_produtos import obter_produtos
from db.functions.db_config import obter_categorias, obter_subcategorias, obter_unidades, obter_subcategorias_por_categoria
import pandas as pd

#------------------------------------------------------------
# Funções, auxiliares e Popups

# Popup de cadastro de novo produto
@st.dialog("Cadastrar novo Produto")
def novo_produto():
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
        st.rerun()


#-------------------------------------------------------------
# Rederização da página

st.title("Produtos")
st.write("Página para gerenciar produtos")

col1, col2, col3, col4 = st.columns(4)
if col1.button("Novo Produto", use_container_width=True):
    novo_produto()
if col2.button("Excluir Produto", use_container_width=True):
    print("Receita")
if col3.button("Editar Produto", use_container_width=True):
    print("Receita")
if col4.button("Alterar Receita", use_container_width=True, type="primary", disabled=True):
    print("Receita")

# Obter os produtos do banco de dados
produtos = obter_produtos()
# Tratar os dados do dataframe de produtos
produtos = [produto[:8] + produto[9:] for produto in produtos] # Obter apenas os dados relevantes
colunas = ["ID", "Nome", "Categoria", "Subcategoria", "Estoque", "Unidade", "Descrição", "Receita"] # Set das colunas do dataframe
df_produtos = pd.DataFrame(produtos, columns=colunas) # Variavel do dataframe grado
df_produtos['Receita'] = df_produtos['Receita'].apply(lambda x: "✅" if x > 0 else "⬜") # Setando o icone de receita baseado na quant. de produção

# Renderizar o dataframe na tela
st.dataframe(df_produtos, use_container_width=True, hide_index=True)
