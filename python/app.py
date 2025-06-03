import streamlit as st
import base64
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# Para testes de conexao:
from mysql.connector import connect, Error

# Definições do streamlit:
st.set_page_config(
    layout= "wide",
    page_icon= "./assets/icone2.png",
    page_title="Dashboard Solus",
)

# Função para carregar as imagens no navegador
def imagemRestaurada(imagem):
    try: 
        with open(imagem, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.toast("O arquivo da imagem não foi encontrado!")
        return None
    
# Função para apagar o header padrao do streamlit:
def esconderHeader():
    hide_st_syle = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_syle, unsafe_allow_html=True)
    
esconderHeader()
    
iconeFuncional = imagemRestaurada("./assets/icone.png")

if iconeFuncional:
    st.sidebar.markdown(
        f"""
        <div style= "margin-top: -90px;">
            <img src = 'data:image/png;base64, {iconeFuncional}' style= 'height: 200px; margin-right:10px;'/>
        </div>    
        """,
        unsafe_allow_html= True
    )

# Botao para ativar o agente
with st.sidebar:
    if st.button("Mandar e-mail para clientes"):
        st.toast("Teste de botao")
        
with st.sidebar:
    st.header('Ordenação')
    ordem = st.radio(
        "Ordernar clientes por:",
        ("Mais compras", "Menos compras"),
        index= 0
    )
    st.markdown("---")
    st.write("Filtros:")
    clientes1compra = st.checkbox("Mostrar clientes com uma venda", False)

# Configurando a conexao com o banco

def conexao():
    return mysql.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )
    
def query(sql):
    conexaoQuery = conexao()
    df = pd.read_sql(sql, conexaoQuery)
    conexaoQuery.close()
    return df

clientes = "SELECT * FROM clientes"
df_clientes = query(clientes)
st.write("Linhas:", df_clientes.shape[0])

produtos = "SELECT * FROM produto"
df_produto = query(produtos)
st.write("Linhas:", df_produto.shape[0])

# Testando a conexao:
if __name__ == "__main__":
    try:
        teste = conexao()
        if teste.is_connected():
            st.toast("Banco de dados conectado!")
        teste.close()
    except Error as e:
        st.toast("Ouve algum problema na conexão!")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(df_clientes)
with col2:
    st.dataframe(df_produto)