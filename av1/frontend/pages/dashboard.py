import streamlit as st
import pandas as pd
import db as db

st.set_page_config(
    layout='wide',
    page_title='Dashboard',
    page_icon=':bar_chart:',
    )

#CSS
st.markdown("""
<style>
            
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

db.sessionstate()

with st.sidebar:
    jogo = st.selectbox('jogo',st.session_state['games'],index=17535)
    #idioma = st.selectbox('idioma',st.session_state['language'])

st.markdown("<h1 style='text-align:center; color:white;'>DASHBOARD &#128202</h1>",unsafe_allow_html=True)
st.divider()


col1,col2,col3 = st.columns((1.5,5,2),gap='medium')
with col1:
    st.markdown('### REVIEWS')
    st.metric('total',db.format_number(db.get_reviews_count()))
    st.metric(str(jogo),db.format_number(db.get_reviews_game_count(jogo)))

with col2:
    #st.markdown('### MAPA')
    choropleth = db.choropleth_mapa()
    st.plotly_chart(choropleth,use_container_width=True,config={'displayModeBar':False})

with col3:
    st.markdown('### REVIEWS POR IDIOMA')
    st.dataframe(db.paises_com_mais_reviews(),use_container_width=True,hide_index=True)


