from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import streamlit as st


def load():    
    try:
        client = MongoClient("mongodb://root:mongo@127.0.0.1:27017/", serverSelectionTimeoutMS=5000)
        client.server_info()  # Isso lançará uma exceção se não puder se conectar ao servidor.
        db = client['Steam']
        collection = db['Analise']
        return collection

    except ConnectionFailure:
        st.write("Falha na conexão ao servidor MongoDB")
