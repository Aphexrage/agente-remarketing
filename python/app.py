import streamlit as st
import base64

# Definições do streamlit:
st.set_page_config(
    layout= "wide",
    page_icon= "icone2.png"
)

# Função para carregar as imagens no navegador
def imagemRestaurada(imagem):
    try: 
        with open(imagem, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error("O arquivo da imagem não foi encontrado!")
        return None
    
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