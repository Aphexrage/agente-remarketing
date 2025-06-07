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
        return st.toast("O arquivo da imagem não foi encontrado") 
    
def imagemFundo(image_path):
    try:
        with open(image_path, "rb") as f:
            encodedImagem = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return st.toast("O arquivo da imagem de fundo não foi encontrado")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encodedImagem}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
def titulo(texto, cor):
    st.markdown(
        f"""
        <h3 style = 'text-align: center; color: {cor}'>
        {texto}</h3>
        """,
        unsafe_allow_html=True
    )
    
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
    
#esconderHeader()
    
iconeFuncional = imagemRestaurada("./assets/icone.png")

fundo = imagemFundo("./assets/fundo.png")

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
    
# Funcao para fazer query
# Coloque seu codigo SQL
# Retorna um dataframe para pandas da query
# Quando faz a query, usa os dados de conexao()

def fazerQuery(sql):
    conexaoParaQuery = conexao()
    df = pd.read_sql(sql, conexaoParaQuery)
    conexaoParaQuery.close()
    return df

df_clientes = fazerQuery("SELECT * FROM clientes")

df_produto = fazerQuery("SELECT * FROM produto")

df_vendas = fazerQuery("SELECT * FROM vendas") 

df_itens = fazerQuery("SELECT * FROM itens_por_venda")

# Quero criar uma tabela mostrando compras por clientes

df_comprasPorCliente = df_vendas.groupby('id_cliente').size().reset_index(name="total")

df_dadosCompletos = df_comprasPorCliente.merge(
    df_clientes,
    on='id_cliente'
)

df_dadosCompletos = df_dadosCompletos[[
    "id_cliente", "nome", "sobrenome", "cpf", "email", "total"
]]

st.dataframe(
    df_dadosCompletos,
    use_container_width=True,
    hide_index=True,
    )

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
    st.write("Clientes")
    st.dataframe(
        df_clientes,
        use_container_width=True,
        hide_index=True,
    )
with col2:
    st.write("Produtos")
    st.dataframe(
        df_produto,
        use_container_width=True,
        hide_index=True
        )