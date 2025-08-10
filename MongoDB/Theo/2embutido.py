import pymongo
from datetime import datetime

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["futebol_db"]

#criando colecao para os jogadores
print("\nCriando a coleção de Jogadores...")
colecao_jogadores2 = db["jogadores_com_clube_embutido"]
colecao_jogadores2.delete_many({})

lista_jogadores_clube_embutido = [
    {"cpf": "12345678901", "nome": "Gabriel Barbosa", "posicao": "Atacante", 
     "clube": {
        "nome": "Flamengo",
        "data_fundacao": datetime(1985,11,17),
    }},
    {"cpf": "32456789001", "nome": "Vitor Roque", "posicao": "Atacante",
     "clube": {
        "nome": "Palmeiras",
        "data_fundacao": datetime(1914,8,26),
    }},
    {"cpf": "34567890001", "nome": "Hugo Souza", "posicao": "Goleiro",
     "clube": {
        "nome": "Corinthians",
        "data_fundacao": datetime(1910,9,1),     
    }},
]

colecao_jogadores2.insert_many(lista_jogadores_clube_embutido)

print("\n --- Dados --- ")
for jogador in colecao_jogadores2.find():
    print(jogador)



# ---------------------------------------------------------------------------------



print("\n ------------ Consulta ------------- ")
clube = "Flamengo"
print(f"\nQuais os nomes dos jogadores que jogam no {clube}?")

jogadores_encontrados = colecao_jogadores2.find(
    {"clube.nome": clube},
)

lista_nomes = []
for jogador in jogadores_encontrados:
    lista_nomes.append(jogador['nome'])

if lista_nomes:
    for nome in lista_nomes:
        print(nome)
else:
    print(f"\nNão existe jogador vinculado ao {clube}")

cliente.close()