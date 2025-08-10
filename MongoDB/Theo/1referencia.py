import pymongo
from datetime import datetime

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["futebol_db"]

# criando colecao para os clubes
print ("\nCriando a coleção de Clubes...")
colecao_clubes = db['clubes']
colecao_clubes.delete_many({}) # para executar repetidamente

lista_clubes = [
    {"nome": "Flamengo", "data_fundacao": datetime(1895,11,17)},
    {"nome": "Palmeiras", "data_fundacao": datetime(1914,8,26)},
    {"nome": "Corinthians", "data_fundacao": datetime(1910,9,1)},
]

lc = colecao_clubes.insert_many(lista_clubes)

print("\n --- Clubes --- ")
for clube in colecao_clubes.find():
    print(clube)

id_do_flamengo = colecao_clubes.find_one({"nome": "Flamengo"})["_id"]
id_do_palmeiras = colecao_clubes.find_one({"nome": "Palmeiras"})["_id"]
id_do_corinthians = colecao_clubes.find_one({"nome": "Corinthians"})["_id"]


# criando colecao para os jogadores
print ("\nCriando a coleção de Jogadores...")
colecao_jogadores = db['jogadores']
colecao_jogadores.delete_many({}) # para exercutar repetidamente

lista_jogadores = [
    {"cpf": "12345678901", "nome": "Gabriel Barbosa", "posicao": "Atacante", "clube_id": id_do_flamengo},
    {"cpf": "00000000001", "nome": "Giorgian de Arrascaeta", "posicao": "Meia", "clube_id": id_do_flamengo},
    {"cpf": "23456789001", "nome": "Vitor Roque", "posicao": "Atacante", "clube_id": id_do_palmeiras},
    {"cpf": "34567890001", "nome": "Hugo", "posicao": "Goleiro", "clube_id": id_do_corinthians},
]

lj = colecao_jogadores.insert_many(lista_jogadores)

print("\n --- Jogadores --- ")
for jogador in colecao_jogadores.find():
    print(jogador)



# ---------------------------------------------------------------------------------------------------------------



print("\n --------- Consulta ----------- ")
clube = "Flamengo"
print(f"\nQual os nomes dos jogadores que jogam no {clube}?")

clube_para_encontrar = colecao_clubes.find_one({"nome": clube})

if clube_para_encontrar:
    id_clube = clube_para_encontrar["_id"]

    jogadores_encontrados = colecao_jogadores.find(
        {"clube_id": id_clube}
    )

    nome_jogadores_encontrados = []
    for jogador in jogadores_encontrados:
        nome_jogadores_encontrados.append(jogador['nome'])

    if nome_jogadores_encontrados:
        for jogador in nome_jogadores_encontrados:
            print(jogador)
    else:
        print("Nenhum jogador encontrado para este clube.")
else:
    print(f"\nNão há clube {clube} no banco de dados")

cliente.close()