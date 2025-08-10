import pymongo
from bson.objectid import ObjectId
import datetime

# Conexão com o servidor
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
meu_banco = cliente['futebol']

meu_banco['clube'].delete_many({})
meu_banco['pessoa'].delete_many({})
meu_banco['partida'].delete_many({})
meu_banco['gol'].delete_many({})

print("Coleções limpas. Iniciando a inserção de dados de base...")

# --- Funções de Inserção por Cenário ---

def insert_scenario_1(gols_master_list):
    meu_banco['gol'].delete_many({})
    print("\nExecutando Inserção - Cenário 1 (Referência Simples)...")
    gols = []
    for gol in gols_master_list:
        gols.append({
            "partida_id": gol["partida_id"],
            "clube_id": gol["clube_id"],
            "jogador_cpf": gol["autor"]["_id"],
            "minuto_do_gol": gol["minuto"]
        })
    meu_banco['gol'].insert_many(gols)
    print("Gols do Cenário 1 inseridos.")

def query_scenario_1():
    nome_clube = input("Nome do Clube: ").strip()
    clube_doc = meu_banco['clube'].find_one({"nome": nome_clube})
    
    if clube_doc:
        clube_id = clube_doc['_id']
        gols_do_clube = meu_banco['gol'].find({"clube_id": clube_id, "jogador_cpf": {"$exists": True}})
        cpfs_jogadores = [gol['jogador_cpf'] for gol in gols_do_clube]
        
        if cpfs_jogadores:
            jogadores = meu_banco['pessoa'].find({"_id": {"$in": cpfs_jogadores}})
            print(f"\nJogadores que fizeram gol pelo {nome_clube}:")
            for jogador in jogadores:
                print(f"- {jogador['nome']}")
        else:
            print(f"Nenhum gol encontrado para o {nome_clube} neste formato de dados.")

def insert_scenario_2(gols_master_list):
    meu_banco['gol'].delete_many({})
    print("\nExecutando Inserção - Cenário 2 (Embutido Simples)...")
    gols = []
    for gol in gols_master_list:
        posicao_jogador = gol["autor"].get("posicao", "Não especificada")
        gols.append({
            "partida_id": gol["partida_id"],
            "clube_id": gol["clube_id"],
            "jogador": {
                "cpf": gol["autor"]["_id"],
                "nome": gol["autor"]["nome"],
                "posicao": posicao_jogador
            },
            "minuto_do_gol": gol["minuto"]
        })
    meu_banco['gol'].insert_many(gols)
    print("Gols do Cenário 2 inseridos.")

def query_scenario_2():
    nome_clube = input("Nome do Clube: ").strip()
    clube_doc = meu_banco['clube'].find_one({"nome": nome_clube})

    if clube_doc:
        clube_id = clube_doc['_id']
        jogadores = meu_banco['gol'].find({"clube_id": clube_id, "jogador": {"$exists": True}}, {"jogador.nome": 1, "_id": 0})
        
        print(f"\nJogadores que marcaram gol para o {nome_clube}:")
        for jogador in jogadores:
            print(f"- {jogador['jogador']['nome']}")

def insert_scenario_3(gols_master_list):
    meu_banco['gol'].delete_many({})
    print("\nExecutando Inserção - Cenário 3 (Array de Referências)...")
    gols = []
    for gol in gols_master_list:
        jogadores_cpfs = [gol["autor"]["_id"]]
        if gol["assistente"]:
            jogadores_cpfs.append(gol["assistente"]["_id"])
        
        gols.append({
            "partida_id": gol["partida_id"],
            "clube_id": gol["clube_id"],
            "jogadores_envolvidos_cpfs": jogadores_cpfs,
            "minuto_do_gol": gol["minuto"]
        })
    meu_banco['gol'].insert_many(gols)
    print("Gols do Cenário 3 inseridos.")

def query_scenario_3():
    nome_clube = input("Nome do Clube: ").strip()
    clube_doc = meu_banco['clube'].find_one({"nome": nome_clube})

    if clube_doc:
        clube_id = clube_doc['_id']
        gols_do_clube = meu_banco['gol'].find({"clube_id": clube_id, "jogadores_envolvidos_cpfs": {"$exists": True}})

        cpfs_jogadores = []
        for gol in gols_do_clube:
            cpfs_jogadores.extend(gol['jogadores_envolvidos_cpfs'])

        cpfs_unicos = list(set(cpfs_jogadores))

        if cpfs_unicos:
            jogadores_encontrados = meu_banco['pessoa'].find({"_id": {"$in": cpfs_unicos}})
            
            print(f"\nJogadores envolvidos em gols do {nome_clube}:")
            for jogador in jogadores_encontrados:
                print(f"- {jogador['nome']}")
        else:
            print(f"Nenhum gol encontrado para o {nome_clube} neste formato de dados.")

def insert_scenario_4(gols_master_list):
    meu_banco['gol'].delete_many({})
    print("\nExecutando Inserção - Cenário 4 (Embutindo Vários Documentos)...")
    gols = []
    for gol in gols_master_list:
        detalhes = {
            "autor": {
                "cpf": gol["autor"]["_id"],
                "nome": gol["autor"]["nome"]
            }
        }
        if gol["assistente"]:
            detalhes["assistente"] = {
                "cpf": gol["assistente"]["_id"],
                "nome": gol["assistente"]["nome"]
            }

        gols.append({
            "partida_id": gol["partida_id"],
            "clube_id": gol["clube_id"],
            "detalhes_gol": detalhes,
            "minuto_do_gol": gol["minuto"]
        })
    meu_banco['gol'].insert_many(gols)
    print("Gols do Cenário 4 inseridos.")

def query_scenario_4():
    nome_clube = input("Nome do Clube: ").strip()
    clube_doc = meu_banco['clube'].find_one({"nome": nome_clube})

    if clube_doc:
        clube_id = clube_doc['_id']
        gols_do_clube = meu_banco['gol'].find({"clube_id": clube_id, "detalhes_gol": {"$exists": True}})

        print(f"\nJogadores que participaram de gols do {nome_clube}:")
        nomes_imprimidos = set()
        for gol in gols_do_clube:
            detalhes = gol['detalhes_gol']
            autor_nome = detalhes.get('autor', {}).get('nome')

            if autor_nome and autor_nome not in nomes_imprimidos:
                print(f"- {autor_nome} (Autor)")
                nomes_imprimidos.add(autor_nome)

            assistente_nome = detalhes.get('assistente', {}).get('nome')
            if assistente_nome and assistente_nome not in nomes_imprimidos:
                print(f"- {assistente_nome} (Assistente)")
                nomes_imprimidos.add(assistente_nome)

def main():
    opcoes_insert = {
        1: insert_scenario_1,
        2: insert_scenario_2,
        3: insert_scenario_3,
        4: insert_scenario_4,
    }

    opcoes_query = {
        1: query_scenario_1,
        2: query_scenario_2,
        3: query_scenario_3,
        4: query_scenario_4,
    }

    opcao = -1
    while opcao:
        meu_banco['gol'].drop()        
        meu_banco['clube'].delete_many({})
        meu_banco['pessoa'].delete_many({})
        meu_banco['partida'].delete_many({})

        meu_banco['clube'].insert_many([
            {"nome": "São Paulo", "data_fundacao": datetime.datetime(1930, 1, 25)}, 
            {"nome": "Palmeiras", "data_fundacao": datetime.datetime(1914, 8, 26)}, 
            {"nome": "Corinthians", "data_fundacao": datetime.datetime(1910, 9, 1)}, 
            {"nome": "Flamengo", "data_fundacao": datetime.datetime(1895, 11, 17)}, 
            {"nome": "Cruzeiro", "data_fundacao": datetime.datetime(1921, 1, 2)
        }
        ])
        clubes_map = {doc['nome']: doc['_id'] for doc in meu_banco['clube'].find({})}
        
        jogadores_data = [
            {"_id": "00000000001", "nome": "Raphael Veiga", "clube_id": clubes_map['Palmeiras'], "posicao": "Meio-campo"},
            {"_id": "00000000002", "nome": "Vitor Roque", "clube_id": clubes_map['Palmeiras'], "posicao": "Atacante"},
            {"_id": "00000000003", "nome": "Arrascaeta", "clube_id": clubes_map['Flamengo'], "posicao": "Meio-campo"},
            {"_id": "00000000004", "nome": "Bruno Henrique", "clube_id": clubes_map['Flamengo'], "posicao": "Atacante"},
            {"_id": "00000000005", "nome": "Rodrigo Garro", "clube_id": clubes_map['Corinthians'], "posicao": "Meio-campo"},
            {"_id": "00000000006", "nome": "Memphis Depay", "clube_id": clubes_map['Corinthians'], "posicao": "Atacante"},
            {"_id": "00000000007", "nome": "Jonathan Calleri", "clube_id": clubes_map['São Paulo'], "posicao": "Atacante"},
            {"_id": "00000000008", "nome": "Lucas Moura", "clube_id": clubes_map['São Paulo'], "posicao": "Atacante"},
            {"_id": "00000000009", "nome": "Kaio Jorge", "clube_id": clubes_map['Cruzeiro'], "posicao": "Atacante"},
            {"_id": "00000000010", "nome": "Matheus Pereira", "clube_id": clubes_map['Cruzeiro'], "posicao": "Meio-campo"},
        ]
        meu_banco['pessoa'].insert_many(jogadores_data)
        jogadores_map = {doc['nome']: doc for doc in meu_banco['pessoa'].find({})}

        partidas_data = [
            {"_id": ObjectId(), "clube_casa_id": clubes_map['Palmeiras'], "clube_visitante_id": clubes_map['Corinthians']},
            {"_id": ObjectId(), "clube_casa_id": clubes_map['Flamengo'], "clube_visitante_id": clubes_map['São Paulo']},
            {"_id": ObjectId(), "clube_casa_id": clubes_map['Flamengo'], "clube_visitante_id": clubes_map['Cruzeiro']}
        ]
        meu_banco['partida'].insert_many(partidas_data)
        partida_ids = [p['_id'] for p in meu_banco['partida'].find()]

        gols_master_list = [
            {"partida_id": partida_ids[0], "clube_id": clubes_map['Palmeiras'], "autor": jogadores_map['Raphael Veiga'], "assistente": jogadores_map['Vitor Roque'], "minuto": 15},
            {"partida_id": partida_ids[0], "clube_id": clubes_map['Corinthians'], "autor": jogadores_map['Rodrigo Garro'], "assistente": None, "minuto": 40},
            {"partida_id": partida_ids[1], "clube_id": clubes_map['Flamengo'], "autor": jogadores_map['Arrascaeta'], "assistente": jogadores_map['Bruno Henrique'], "minuto": 50},
            {"partida_id": partida_ids[1], "clube_id": clubes_map['São Paulo'], "autor": jogadores_map['Jonathan Calleri'], "assistente": jogadores_map['Lucas Moura'], "minuto": 80},
            {"partida_id": partida_ids[2], "clube_id": clubes_map['Cruzeiro'], "autor": jogadores_map['Kaio Jorge'], "assistente": None, "minuto": 90},
            {"partida_id": partida_ids[2], "clube_id": clubes_map['Cruzeiro'], "autor": jogadores_map['Matheus Pereira'], "assistente": jogadores_map['Kaio Jorge'], "minuto": 93}
        ]

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
                break
            elif opcao in opcoes_insert:
                print("==============================================================================")
                opcoes_insert[opcao](gols_master_list)
                opcoes_query[opcao]()
            else:
                print("Opção inválida, tente novamente.")
        except:
            print("Por favor, digite um número válido.")

main()
