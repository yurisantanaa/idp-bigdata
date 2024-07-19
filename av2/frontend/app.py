import streamlit as st
from db import *

st.set_page_config(
    layout='wide',
    page_title='Reviews',
    page_icon=":trophy:"
)

sessionstate()

result = None
sentiment = None

st.markdown("<h1 style='text-align:center; color:white;'>REVIEWS DA STEAM &#127918</h1>",unsafe_allow_html=True)
st.caption('Aluno Yuri Santana')

col1, col2,col3 = st.columns([4,4,1])
placeholder = st.empty()

with col1:
    jogo = st.selectbox('games',st.session_state['games'],index = 17535,label_visibility="collapsed")
with col2:
    idioma = st.selectbox('idioma',st.session_state['language'],label_visibility='collapsed')
with col3:
    if st.button('enviar'):
        reviews = findreviews(connectMongo(),jogo,idioma)
        listareview = listareviews(reviews)
        listaid = listaids(reviews)

        sentiment = generatesentiment(listareview)
        result = return_dataframe(listareview,sentiment)
        updatetabela(listareview,listaid,sentiment,connectMongo())
        with placeholder.container():
            st.dataframe(result,use_container_width= True,hide_index=True)
