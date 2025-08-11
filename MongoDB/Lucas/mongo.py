import pymongo
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

def limpar_colecoes(db):
  """
  Apaga a coleção 'clube' para garantir um teste limpo e isolado.
  """
  db.clube.delete_many({})


def cenario_1_referencia_unica(db):
  """
  Cenário 1: Referência Simples (Adaptado para 1-para-1).
  Caso de uso: Um clube tem um "Principal Rival".
  O documento do clube armazena o ID do seu maior rival.
  """
  print("\nExecutando: Cenário 1 (Referência de 'Principal Rival')")

  #Inserção dos clubes
  db.clube.insert_many([
    {"_id": "SPT", "nome": "Sport Club do Recife", "data_fundacao": datetime(1905, 5, 13)},
    {"_id": "NAU", "nome": "Clube Náutico Capibaribe", "data_fundacao": datetime(1901, 4, 7)}
  ])
  #Adiciona a referência de rival no Sport
  db.clube.update_one(
    {"_id": "SPT"}, 
    {"$set": {"principal_rival_ref": "NAU"}}
  )

  #Consulta: Qual o nome do principal rival do Sport?
  sport = db.clube.find_one({"_id": "SPT"})
  rival = db.clube.find_one({"_id": sport['principal_rival_ref']})

  pp.pprint(rival)


def cenario_2_embutido_unico(db):
  """
  Cenário 2: Documento Embutido (Adaptado para 1-para-1).
  Caso de uso: Um clube tem um "Principal Rival", e seus dados básicos
  são embutidos para otimizar a leitura.
  """
  print("\nExecutando: Cenário 2 (Embutindo 'Principal Rival')")

  #Inserção do clube com o rival embutido
  db.clube.insert_one({
    "_id": "SPT",
    "nome": "Sport Club do Recife",
    "data_fundacao": datetime(1905, 5, 13),
    "principal_rival": {
      "id_clube": "NAU",
      "nome": "Clube Náutico Capibaribe"
    }
  })

  #Consulta: Qual o nome do principal rival do Sport?
  sport = db.clube.find_one({"_id": "SPT"})

  pp.pprint(sport['principal_rival'])


def cenario_3_array_referencias(db):
  """
  Cenário 3: Array de Referências (N-para-N).
  O modelo mais fiel ao relacional para N:N, onde um clube
  armazena uma lista de IDs de seus rivais.
  """
  print("\nExecutando: Cenário 3 (Array de Referências de Rivais)")

  #Inserção dos clubes
  db.clube.insert_many([
    {"_id": "SPT", "nome": "Sport Club do Recife"},
    {"_id": "NAU", "nome": "Clube Náutico Capibaribe"},
    {"_id": "STC", "nome": "Santa Cruz Futebol Clube"}
  ])
  #Adiciona a lista de referências de rivais no Sport
  db.clube.update_one(
    {"_id": "SPT"},
    {"$set": {"rivais_refs": ["NAU", "STC"]}}
  )

  #Consulta: Quais os nomes dos rivais do Sport?
  sport = db.clube.find_one({"_id": "SPT"})
  ids_rivais = sport['rivais_refs']

  rivais = list(db.clube.find({"_id": {"$in": ids_rivais}}))

  pp.pprint(rivais)


def cenario_4_array_embutido(db):
  """
  Cenário 4: Array de Documentos Embutidos (N-para-N).
  Abordagem NoSQL clássica para N:N, otimizada para leitura.
  O clube armazena uma lista com os dados básicos de seus rivais.
  """
  print("\nExecutando: Cenário 4 (Array Embutido de Rivais)")

  #Inserção do clube com a lista de rivais embutida
  db.clube.insert_one({
    "_id": "SPT",
    "nome": "Sport Club do Recife",
    "rivais": [
      {"id_clube": "NAU", "nome": "Clube Náutico Capibaribe"},
      {"id_clube": "STC", "nome": "Santa Cruz Futebol Clube"}
    ]
  })

  #Consulta: Quais os nomes dos rivais do Sport?
  sport = db.clube.find_one({"_id": "SPT"})

  pp.pprint(sport['rivais'])


def main():
  """
  Função principal com o menu de interação.
  """
  client = pymongo.MongoClient("mongodb://localhost:27017/")
  db = client['futebol']

  cenarios = {
    1: cenario_1_referencia_unica,
    2: cenario_2_embutido_unico,
    3: cenario_3_array_referencias,
    4: cenario_4_array_embutido
  }

  while True:
    print("\n----------------------------------")
    print("Relacionamento Rival (Clube-Clube)")
    print("1: Cenário de Referência Única (Principal Rival)")
    print("2: Cenário Embutido Único (Principal Rival)")
    print("3: Cenário com Array de Referências (Rivais)")
    print("4: Cenário com Array Embutido (Rivais)")
    print("0: Sair")

    try:
      escolha = int(input("Escolha o cenário a executar: "))

      if escolha == 0:
        print("Encerrando...")
        break

      if escolha in cenarios:
        limpar_colecoes(db)
        cenarios[escolha](db)
      else:
        print("Opção inválida. Tente novamente.")

    except ValueError:
      print("Entrada inválida. Por favor, digite um número.")
    except Exception as e:
      print(f"Ocorreu um erro inesperado: {e}")

  client.close()

if __name__ == "__main__":
  main()
