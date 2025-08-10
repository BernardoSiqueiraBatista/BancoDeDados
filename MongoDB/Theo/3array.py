import pymongo
from datetime import datetime

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente['futebol_db']


# colecao de jogadores
colecao_jogadores_ref = db['jogadores_referenciados']
colecao_jogadores_ref.delete_many({})

jogadores_inserir = [
    {"cpf": "1111111111", "nome": "Gabriel Barbosa", "posicao": "Atacante"},
    {"cpf": "2222222222", "nome": "Vitor Roque", "posicao": "Atacante"},
    {"cpf": "3333333333", "nome": "Giorgian de Arrascaeta", "posicao": "Meia"},

]

colecao_jogadores_ref.insert_many(jogadores_inserir)

# pegando todos os ids de jogadores do flamengo
jogadores_flamengo  = colecao_jogadores_ref.find(
    {"nome": {"$in": ["Gabriel Barbosa", "Giorgian de Arrascaeta"]}}
)

ids_jogadores_flamengo = []
for jogador in jogadores_flamengo:
    ids_jogadores_flamengo.append(jogador["_id"])

#------------------

# colecao de clubes 
colecao_clubes_ref = db['clubes_referenciados']
colecao_clubes_ref.delete_many({})

clube_flamengo = {
    "nome": "Flamengo",
    "data_fundacao": datetime(1895,11,17),
    "jogadores_ids": ids_jogadores_flamengo # array de referencias
}

colecao_clubes_ref.insert_one(clube_flamengo)



# ----------------------------------------------------------------------------------



print("\n -------------- Consulta --------------")
clube = "Flamengo"
print(f"\nQuais os nomes dos jogadores que jogam no {clube}?")

doc_clube = colecao_clubes_ref.find_one({"nome": clube})

if doc_clube:
    lista_id_jogadores = doc_clube.get("jogadores_ids", [])
    
    if lista_id_jogadores:
        jogadores_encontrados = colecao_jogadores_ref.find(
            {"_id": {"$in": lista_id_jogadores}},
        )

        lista_nome = []
        for jogador in jogadores_encontrados:
            lista_nome.append(jogador['nome'])

        if lista_nome:
            for nome in lista_nome:
                print(nome)
        else:
            print("Nenhum jogador encontrado para os ids fornecidos")
    else:
        print("O clube não possui jogadores associados")
else:
    print(f"Clube '{clube}' não encontrado")


cliente.close()

