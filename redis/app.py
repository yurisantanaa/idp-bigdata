from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def hello_world():
    app.logger.info("Rodando o hello world")

    app.logger.info(f'Escrevendo chave no redis ...')
    r.set("alguma_chave", "algum_valor")

    valor = r.get("alguma_chave")
    app.logger.info(f'Valor obtido do Redis: {valor}')
    
    return 'Olá, mundo!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6000)