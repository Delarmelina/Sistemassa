import streamlit as st
from db.database_structure import criar_banco

# Configurar o layout para abrir sempre em wide mode
st.set_page_config(
    page_title="Gerenciamento de Produtos",
    layout="wide"  # Define o layout como "wide"
)

# Inicialização do banco de dados
#criar_banco()

# Páginas da Home
home_page = st.Page("Paginas/Home/Home.py", title="Home", icon=":material/home:")

#Páginas de Cadastro
fornecedores_page = st.Page("Paginas/Cadastros/Fornecedores.py", title="Fornecedores", icon=":material/local_shipping:")
restaurantes_page = st.Page("Paginas/Cadastros/Restaurantes.py", title="Restaurantes", icon=":material/restaurant:")
produtos_page = st.Page("Paginas/Cadastros/Produtos.py", title="Produtos", icon=":material/inventory_2:")

# Páginas da Movimentação
producao_produtos_page = st.Page("Paginas/Movimentacao/Producao_produtos.py", title="Produção de Produtos", icon=":material/production_quantity_limits:")
entrada_produtos_page = st.Page("Paginas/Movimentacao/Entrada_produtos.py", title="Entrada de Produtos", icon=":material/inbox:")
saida_produtos_page = st.Page("Paginas/Movimentacao/Saida_produtos.py", title="Saída de Produtos", icon=":material/outbox:")
transferencia_produtos_page = st.Page("Paginas/Movimentacao/Transferencia_produtos.py", title="Transferência de Produtos", icon=":material/transfer_within_a_station:")

# Páginas de Configuração
configuracao_page = st.Page("Paginas/Config/Configuracao.py", title="Configuração", icon=":material/manufacturing:")

# Páginas auxiliares
new_produtos_page = st.Page("Paginas/Cadastros/Produtos_new.py", title="Novo Produto", icon=":material/inventory_2:")

pages = {
        "Home": [home_page],
        "Cadastros": [fornecedores_page, restaurantes_page, produtos_page],
        "Movimentação": [producao_produtos_page, entrada_produtos_page, saida_produtos_page, transferencia_produtos_page],
        "Configuração": [configuracao_page],
        }   

pg = st.navigation(pages=pages)

# Testar execução
try:
    pg.run()
except Exception as e:
    st.error(f"Erro ao executar: {e}")