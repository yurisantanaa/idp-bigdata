import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from db import load


def main():
    genai.configure(api_key='AIzaSyAYdoNtq0TaXnplBTF1638cKIUFqam7xHo')
    model = genai.GenerativeModel('gemini-1.5-flash')
    collection = load()
    menu(collection)

def showreviews(collection,jogo):
    myquery = collection.find({'game': jogo,'language':'english'},{'review':1,'_id':0})
    #reviews = [doc['review'] for doc in myquery[:10]] #ta lento
    reviews = ['jogo bom']
    return reviews

def menu(collection):
    result=None
    st.title('Reviews da Steam :video_game:', anchor=False)
    st.caption('Aluno Yuri Santana')
    col1, col2= st.columns([3,1])
    #myquery = collection.distinct('game')   #lento
    myquery = {'cs2','hollow'}
    with col1:
        jogo = st.selectbox('games',myquery,index = 1,label_visibility="collapsed")
    with col2:
        if st.button('enviar'):
            result = showreviews(collection,jogo)
    if result != None:
        st.dataframe(result,column_config={'value':'review'},use_container_width = True)


main()



        #response = model.generate_content(pergunta)
        #for chunk in response:
        #    st.write(chunk.text)