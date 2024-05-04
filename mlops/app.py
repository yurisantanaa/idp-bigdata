import os
from flask import Flask, request, jsonify
# Importar Biblioteca da Hugging Face
from transformers import pipeline

app = Flask(__name__)

# Carregar o modelo de classificação de sentimentos
sentiment_model = pipeline("sentiment-analysis")


@app.route('/analyze_sentiment',methods=['POST'])
def analyze_sentiment():
    # Receber dados JSON da requisição
    data = request.get_json()

    # Extrair os valores do JSON
    fixed_acidity = data['fixed acidity']
    volatile_acidity = data['volatile acidity']
    citric_acid = data['citric acid']
    residual_sugar = data['residual sugar']
    chlorides = data['chlorides']
    free_sulfur_dioxide = data['free sulfur dioxide']
    total_sulfur_dioxide = data['total sulfur dioxide']
    density = data['density']
    pH = data['pH']
    sulphates = data['sulphates']
    alcohol = data['alcohol']
    color = data['color']

    # Fazer a previsão usando o modelo
    predicao = modelo.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol, color]])

    # Mapear o resultado da previsão para uma resposta legível
    resultado = ['Vinho Ruim' if pred == 1 else 'Vinho Bom' for pred in predicao]

    # Retornar o resultado como JSON
    return jsonify(resultado)

    # Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)