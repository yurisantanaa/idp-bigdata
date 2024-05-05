Objetivo:Usar o MongoDB juntamente com o Jupyter para analisar o dataset do top 1000 universidades do mundo


Como executar:
    1.execute os arquivos permissions.sh e wait-for-it.sh
        chmod +x permissions.sh
        chmod +x wait-for-it.sh
        ./wait-for-it.sh
        ./permissions.sh

    2.suba o container
        -docker compose up -d

    3.baixe o dataset
        -wget...

        -converta o arquivo para utf8:
            iconv -f ISO-8859-1 -t UTF-8 universitydatasets.csv > universitydatasets_utf8.csv

        -importe para o mongodb:
            docker exec -it mongo_service mongoimport --db analise --collection university_ranking --type csv --file /datasets/universitydatasets_utf8.csv --headerline --ignoreBlanks --username root --password mongo --authenticationDatabase admin

    4.conecte no jupyter(porta 8888) e rode os codigos