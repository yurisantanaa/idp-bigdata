from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import google.generativeai as genai
import streamlit as st
import pandas as pd
from bson.objectid import ObjectId
import plotly.express as px


def connectMongo():    
    try:
        client = MongoClient("mongodb://root:mongo@mongo_service/", serverSelectionTimeoutMS=5000)
        db = client['Steam']
        collection = db['Analise']
        return collection

    except ConnectionFailure:
        client.server_info()  # Isso lançará uma exceção se não puder se conectar ao servidor.
        st.write("Falha na conexão ao servidor MongoDB")


def get_reviews_count():
    reviews_count = connectMongo().estimated_document_count()
    return reviews_count

def get_reviews_game_count(jogo):
    if jogo is not None:
        myquery = list(connectMongo().aggregate([
        {
            '$match': {
                'game': jogo
            }
        }, {
            '$count': 'num_reviews'
        }
        ]))
        return myquery[0]['num_reviews']
    else:
        return 0

def findreviews(collection,jogo,idioma):
    myquery = list(collection.find({'game': jogo,'language':idioma,'sentiment':None},{'review':1,'_id':1}).limit(10))
    return myquery

def updatetabela(review,id,sentiment,collection):
    combined = list(zip(id,review,sentiment))
    for reviewtoupdate in combined:
        collection.update_one({'_id':ObjectId(reviewtoupdate[0])},{'$set':{'sentiment':reviewtoupdate[2]}})

def generatesentiment(review):
    lista = []
    genai.configure(api_key='AIzaSyAYdoNtq0TaXnplBTF1638cKIUFqam7xHo')
    model = genai.GenerativeModel('gemini-1.5-flash')

    safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

    for analyzereview in review:
        prompt = f"""
        Classifique esse review e retorne SOMENTE as palavras POSITIVO,NEGATIVO ou NEUTRO para o sentimento atrelado a este review
        SE o review estiver em branco ou nao for possivel identificar o sentimento retorne NEUTRO
        Using this JSON schema:
            review = {analyzereview}
        """
        response = model.generate_content(prompt,safety_settings=safe)
        #st.write(response)
        if response is not None:
            lista.append(response.text)
    if lista:   
        return lista
    
    else:
        return 1

def return_dataframe(review,sentiment):
    combined = list(zip(review, sentiment))
    result = pd.DataFrame(list(combined),columns=['review','sentimento'])
    return result


def listareviews(reviews):
    review = [doc['review'] for doc in reviews]
    return review

def listaids(reviews):
    id = [doc['_id'] for doc in reviews]
    return id


def sessionstate():
    st.session_state['games'] = connectMongo().distinct('game')
    st.session_state['language'] = connectMongo().distinct('language')

def paises_com_mais_reviews():
    myquery = list(connectMongo().aggregate([{'$group': {'_id': '$language', 'count': {'$sum': 1}}}]))
    df = pd.DataFrame(myquery)
    df.rename(columns={'_id' : 'idioma','count' : 'quantidade'},inplace=True)
    df.sort_values(by='quantidade',ascending=False,inplace=True)
    return df

def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    if num > 1000:
        if not num % 1000:
            return f'{num // 1000} K'
        return f'{round(num/1000,1)}K'
    return num

def choropleth_mapa():
    st.write()
    df = pd.read_csv('datasets/countries-languages.csv')

    language_color_map={
        'others': '#8A8A8A',
        'english': '#0012CB',
        'spanish': '#FF0202',
        'schinese': '#FFCD02',
        'brazilian': '#FF8000'
    }

    #st.write('teste')
    #f['color'] = df['Languages Spoken'].map(language_color_map)
    #st.write(df)
    #df['quantidade'] = df['language'].map(language_color_map)

    choropleth = px.choropleth(
        df,
        locations='Country',
        hover_name='Languages Spoken',
        projection='natural earth',
        locationmode='country names',
        color = 'Languages Spoken',
        color_discrete_map=language_color_map
        )

    choropleth.update_layout(
        template = 'plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=0,b=0),
        showlegend=False,
        height=350
    )
    return choropleth
