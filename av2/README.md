PROPOSTA:
    A análise de sentimentos em reviews de usuários é uma ferramenta poderosa para entender a percepção e a satisfação dos consumidores em relação a produtos e serviços. No contexto dos jogos na Steam, essas análises podem fornecer insights valiosos para desenvolvedores e empresas de jogos. Esta proposta descreve uma solução de big data que coleta reviews da Steam, armazena-os no MongoDB e utiliza uma IA generativa para classificar os sentimentos dos reviews. A interface do usuário será desenvolvida utilizando o Streamlit, proporcionando uma visualização intuitiva e interativa dos dados.

DESCRICAO DA ARQUITETURA:
    Armazenamento em MongoDB: Os reviews coletados serão armazenados em um banco de dados NoSQL MongoDB, escolhendo esta tecnologia pela sua capacidade de lidar com grandes volumes de dados de forma eficiente e flexível.

    Classificação de Sentimentos: Implementação de um modelo de IA generativa, para analisar o texto dos reviews e atribuir um sentimento (positivo, negativo ou neutro) a cada um.

    Desenvolvimento da Interface: Criação de uma interface interativa usando Streamlit, onde os usuários poderão visualizar as análises de sentimentos dos reviews.

COMO TESTAR:
    1.Suba o docker:
        docker compose up -d

    2.Importar o arquivo csv com os reviews da steam:
        docker exec -it mongo_service mongoimport --db Steam --collection Analise  --type csv --file datasets/all_reviews.csv --headerline --ignoreBlanks --username root --password mongo --authenticationDatabase admin

    3.Crie os indices da coluna game e language:
        docker exec -it mongo_service bash
        mongo -u root -p mongo
        use Steam
        db.Analise.createIndex({game:1})
        db.Analise.createIndex({language:1})

    4.instale os requirements
        pip install -r requirements.txt

    5.acesse a interface streamlit
        cd frontend
        streamlit run app.py
        acesse localhost:8051
