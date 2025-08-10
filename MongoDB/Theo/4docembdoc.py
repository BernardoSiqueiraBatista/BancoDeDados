import pymongo
from datetime import datetime

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["futebol_db"]

# colecao de clubes
colecao_clubes_embutidos = db["clubes_com_jogadores_embutidos"]
colecao_clubes_embutidos.delete_many({})

clube_com_jogadores = {
    "nome": "Flamengo",
    "data_fundacao": datetime(1895,11,17),
    "jogadores": [
        {
            "cpf": "11111111111",
            "nome": "Gabriel Barbosa",
            "posicao": "Atacante"
        },
        {
            "cpf": "22222222222",
            "nome": "Giorgian de Arrascaeta",
            "posicao": "Meia"
        }
    ]
}

colecao_clubes_embutidos.insert_one(clube_com_jogadores)



# -----------------------------------------------------------------



print("\n ------------ CONSULTA ------------ ")
clube = "Flamengo"
print(f"\nQuais os nomes dos jogadores que jogam no {clube}?")

doc_clube = colecao_clubes_embutidos.find_one({"nome": clube})

if doc_clube:
    if "jogadores" in doc_clube:
        lista_nomes = []
        for jogador in doc_clube['jogadores']:
            lista_nomes.append(jogador['nome'])

        for nome in lista_nomes:
            print(nome)
    else:
        print("\nO clube não possui jogadores")
else:
    print(f"\nO clube {clube} não existe")

cliente.close()