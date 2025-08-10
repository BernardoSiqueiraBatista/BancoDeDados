import pymongo
from datetime import datetime

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente['futebol']



# Query : Nome dos Jogadores que jogam no clube "..."



# Documento referenciando apenas um documento
def scenario_1():
    
    dados_clube1 = {"_id": 1, "nome": "Sport", "data_fundacao": datetime(1905, 5, 13)}
    dados_clube2 = {"_id": 2, "nome": "Nautico", "data_fundacao": datetime(1902, 4, 7)}
    dados_clube3 = {"_id": 3, "nome": "Santa", "data_fundacao": datetime(1914, 2, 3)}
    
    db.clube.insert_many([dados_clube1, dados_clube2, dados_clube3])

    dados_jogador1 = {"_id": 1, "nome": "Diego Souza", "posicao": "Atacante", "id_clube": 1}
    dados_jogador2 = {"_id": 2, "nome": "Magrão", "posicao": "Goleiro", "id_clube": 1}
    dados_jogador3 = {"_id": 3, "nome": "Carlinhos Bala", "posicao": "Atacante", "id_clube": 1}
    dados_jogador4 = {"_id": 4, "nome": "Kiesa", "posicao": "Atacante", "id_clube": 2}
    dados_jogador5 = {"_id": 5, "nome": "Tiago Garlhardo", "posicao": "Atacante", "id_clube": 3}
    
    db.jogador.insert_many([dados_jogador1, dados_jogador2, dados_jogador3, dados_jogador4, dados_jogador5])

def query_scenario_1():
    nome = input("Nome do Clube: ").strip()
    id_clube = db.clube.find_one({"nome": nome})
    
    if(id_clube):
        jogadores = db.jogador.find({"id_clube": id_clube["_id"]})

        for i in jogadores:
            print(i)



# Documento embutindo apenas um documento
def scenario_2():
    dados_jogador1 = {
        "_id": 1,
        "nome": "Diego Souza",
        "posicao": "Atacante",
        
        "clube" : {
            "nome": "Sport",
            "data_fundacao": datetime (1905, 5, 13),
        }
    }
    dados_jogador2 = {
        "_id": 2,
        "nome": "Magrão",
        "posicao": "Goleiro",
        
        "clube" : {
            "nome": "Sport",
            "data_fundacao": datetime (1905, 5, 13),
        }
    }
    dados_jogador3 = {
        "_id": 3,
        "nome": "Carlinhos Bala",
        "posicao": "Atacante",
        
        "clube" : {
            "nome": "Sport",
            "data_fundacao": datetime (1905, 5, 13),
        }
    }
    dados_jogador4 = {
        "_id": 4,
        "nome": "Kiesa",
        "posicao": "Atacante",
        
        "clube" : {
            "nome": "Nautico",
            "data_fundacao": datetime (1902, 4, 7),
        }
    }
    dados_jogador5 = {
        "_id": 5,
        "nome": "Tiago Galhardo",
        "posicao": "Atacante",
        
        "clube" : {
            "nome": "Santa",
            "data_fundacao": datetime (1914, 2, 3)
        }
    }

    db.jogador.insert_many([dados_jogador1, dados_jogador2, dados_jogador3, dados_jogador4, dados_jogador5])

def query_scenario_2():
    nome = input("Nome do Clube: ").strip()
    query = {"clube.nome": nome}
    jogadores = db.jogador.find(query)

    for i in jogadores:
        print(i)



# Documento com um array de referências para documentos
def scenario_3():
    dados_jogador_1 = {"_id": 1, "nome": "Diego Souza", "posicao": "Atacante"}
    dados_jogador_2 = {"_id": 2, "nome": "Magrão", "posicao": "Goleiro"}
    dados_jogador_3 = {"_id": 3, "nome": "Carlinhos Bala", "posicao": "Atacante"}
    dados_jogador_4 = {"_id": 4, "nome": "Kiesa", "posicao": "Atacante"}
    dados_jogador_5 = {"_id": 5, "nome": "Tiago Galhardo", "posicao": "Atacante"}
    
    db.jogador.insert_many([dados_jogador_1, dados_jogador_2, dados_jogador_3, dados_jogador_4, dados_jogador_5])


    dadosClube1 = {
        "_id": 1,
        "nome": "Sport",
        "data_fundacao": datetime (1905, 5, 13),
        "id_jogadores": [dados_jogador_1["_id"], dados_jogador_2["_id"], dados_jogador_3["_id"]]
    }
    dadosClube2 = {
        "_id": 2,
        "nome": "Nautico",
        "data_fundacao": datetime (1902, 4, 7),
        "id_jogadores": [dados_jogador_4["_id"]]
    }
    dadosClube3 = {
        "_id": 3,
        "nome": "Santa",
        "data_fundacao": datetime (1914, 2 , 3),
        "id_jogadores": [dados_jogador_5["_id"]]
    }

    db.clube.insert_many([dadosClube1, dadosClube2, dadosClube3])

def query_scenario_3():
    nome = input("Nome do Clube: ").strip()
    query = {"nome": nome}
    clube = db.clube.find_one(query)

    if clube:
        jogadores = db.jogador.find({"_id": {"$in" : clube["id_jogadores"]}})
        
        for i in jogadores:
            print(i)



# Documento embutindo vários documentos
def scenario_4():
    dados_clube1 = {
        "_id": 1,
        "nome": "Sport",
        "data_fundacao": datetime (1905, 5, 13),
        "jogadores": [
            {"nome": "Diego Souza", "posicao": "Atacante"},
            {"nome": "Magrão", "posicao": "Goleiro"},
            {"nome": "Carlinhos Bala", "posicao": "Atacante"}
        ]
    }
    dados_clube2 = {
        "_id": 2,
        "nome": "Nautico",
        "data_fundacao": datetime (1902, 4, 7),
        "jogadores": [
            {"nome": "Kiesa", "posicao": "Atacante"}
        ]
    }
    dados_clube3 = {
        "_id": 3,
        "nome": "Santa",
        "data_fundacao": datetime (1914, 2, 3),
        "jogadores": [
            {"nome": "Tiago Galhardo", "posicao": "Atacante"}
        ]
    }

    db.clube.insert_many([dados_clube1, dados_clube2, dados_clube3])

def query_scenario_4():
    nome = input("Nome do Clube: ").strip()
    clube = db.clube.find_one({"nome": nome})

    if clube:
        for i in clube["jogadores"]:
            print(i)



def main():
    opcoes_insert = {
        1: scenario_1,
        2: scenario_2,
        3: scenario_3,
        4: scenario_4,
    }

    opcoes_query = {
        1: query_scenario_1,
        2: query_scenario_2,
        3: query_scenario_3,
        4: query_scenario_4,
    }

    opcao = -1
    while opcao:

        db.jogador.drop()
        db.clube.drop()

        db['jogador']
        db['clube']


        print("==============================================================================")
        print("1. Cenário 1")
        print("2. Cenário 2")
        print("3. Cenário 3")
        print("4. Cenário 4")
        print("0. Sair")


        try:
            opcao = int(input("Escolha: "))
            if opcao == 0:
                print("Fim...")
            elif opcao in opcoes_insert:
                print("==============================================================================")
                opcoes_insert[opcao]()
                opcoes_query[opcao]()
            else:
                print("Opção inválida, tente novamente.")
        except:
            print("Por favor, digite um número válido.")

main()