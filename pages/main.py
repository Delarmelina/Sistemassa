import streamlit as st
from utils.get_globals import get_restaurante, get_usuario_id

def render():

    # Páginas da Home
    home_page = st.Page("pages/Home/Home.py", title="Home", icon=":material/home:")
    sel_rest_page = st.Page("pages/Home/Selecionar_rest.py", title="Alterar Restaurante", icon=":material/storefront:")
    logout_page = st.Page("pages/Home/Logout.py", title="Logout", icon=":material/storefront:")

    #Páginas de Cadastro
    usuarios_page = st.Page("pages/Cadastros/Usuarios.py", title="Usuarios", icon=":material/group:")
    fornecedores_page = st.Page("pages/Cadastros/Fornecedores.py", title="Fornecedores", icon=":material/local_shipping:")
    restaurantes_page = st.Page("pages/Cadastros/Restaurantes.py", title="Restaurantes", icon=":material/restaurant:")
    produtos_page = st.Page("pages/Cadastros/Produtos.py", title="Produtos", icon=":material/inventory_2:")

    # Páginas da Movimentação
    producao_produtos_page = st.Page("pages/Movimentacao/Producao_produtos.py", title="Produção de Produtos", icon=":material/production_quantity_limits:")
    entrada_produtos_page = st.Page("pages/Movimentacao/Entrada_produtos.py", title="Entrada de Produtos", icon=":material/inbox:")
    saida_produtos_page = st.Page("pages/Movimentacao/Saida_produtos.py", title="Saída de Produtos", icon=":material/outbox:")
    transferencia_produtos_page = st.Page("pages/Movimentacao/Transferencia_produtos.py", title="Transferência de Produtos", icon=":material/transfer_within_a_station:")

    # Páginas de Configuração
    configuracao_page = st.Page("pages/Config/Configuracao.py", title="Configuração", icon=":material/manufacturing:")

    pages = {
        "Home": [home_page, sel_rest_page, logout_page],
        "Cadastros": [usuarios_page, fornecedores_page, restaurantes_page, produtos_page],
        "Movimentação": [producao_produtos_page, entrada_produtos_page, saida_produtos_page, transferencia_produtos_page],
        "Configuração": [configuracao_page],
    }

    if get_usuario_id() is not None:
        pg = st.navigation(pages=pages)
    else:
        pg = st.navigation(pages=[home_page, logout_page], position="hidden")

    # Testar execução
    try:
        pg.run()
    except Exception as e:
        st.error(f"Erro ao executar: {e}")