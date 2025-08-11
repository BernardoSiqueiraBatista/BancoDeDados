import pymongo
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

def limpa_banco(db):
  db.pessoa.delete_many({})
  db.arbitro.delete_many({})
  db.partida.delete_many({})


def cenario_1_referencia(db):
  """Emula a estrutura relacional: Partida -> Arbitro -> Pessoa."""
  print("Executando: Cenário 1 (Referência)")

  #Inserção de dados
  db.pessoa.insert_one({
    "_id": "111", 
    "nome": "Raphael Claus",
    "nascimento": datetime(1979, 8, 6)
  })
  db.arbitro.insert_one({
    "_id": "111", #Mesmo ID de pessoa
    "cartao_fifa": True,
    "pessoa_ref": "111" #FK para pessoa
  })
  db.partida.insert_one({
    "descricao": "Final do Campeonato",
    "arbitro_ref": "111" #FK para arbitro
  })

  partida = db.partida.find_one({"descricao": "Final do Campeonato"})
  arbitro = db.arbitro.find_one({"_id": partida['arbitro_ref']})
  pessoa_arbitro = db.pessoa.find_one({"_id": arbitro['pessoa_ref']})

  pp.pprint(pessoa_arbitro)

def cenario_2_embutido(db):
  """Modelo NoSQL: Partida com os dados do árbitro embutidos."""
  print("Executando: Cenário 2 (Embutido)")

  #1 Inserção de dados
  db.partida.insert_one({
    "descricao": "Final do Campeonato",
    "arbitro": {
      "cpf": "111",
      "nome": "Raphael Claus",
      "cartao_fifa": True
    }
  })

  #2 Consulta direta
  partida = db.partida.find_one({"descricao": "Final do Campeonato"})

  pp.pprint(partida['arbitro'])

def cenario_3_array_referencias(db):
  """Emula a estrutura relacional: Partida -> N Arbitros."""
  print("Executando: Cenário 3 (Array de Referências)")

  #1 Insere as pessoas/árbitros
  db.pessoa.insert_many([
    {"_id": "111", "nome": "Raphael Claus"},
    {"_id": "222", "nome": "Wilton Pereira Sampaio"},
    {"_id": "333", "nome": "Anderson Daronco"}
  ])

  #2 Insere a partida com a lista de IDs
  db.partida.insert_one({
    "descricao": "Jogo Noturno",
    "equipe_arbitragem_refs": ["111", "222", "333"]
  })

  #3 Consulta com o operador $in
  partida = db.partida.find_one({"descricao": "Jogo Noturno"})
  ids_arbitros = partida['equipe_arbitragem_refs']

  #find() retorna um cursor, então precisamos iterar
  arbitros_encontrados = list(db.pessoa.find({"_id": {"$in": ids_arbitros}}))

  pp.pprint(arbitros_encontrados)

def cenario_4_array_embutido(db):
  """Modelo NoSQL: Partida com a equipe de arbitragem embutida."""
  print("Executando: Cenário 4 (Array Embutido)")

  #1 Insere a partida com a lista de documentos
  db.partida.insert_one({
    "descricao": "Jogo Decisivo",
    "equipe_arbitragem": [
      {"cpf": "111", "nome": "Raphael Claus", "funcao": "Principal"},
      {"cpf": "222", "nome": "Wilton Pereira Sampaio", "funcao": "Assistente"},
      {"cpf": "333", "nome": "Anderson Daronco", "funcao": "VAR"}
    ]
  })

  #2 Consulta direta
  partida = db.partida.find_one({"descricao": "Jogo Decisivo"})

  pp.pprint(partida['equipe_arbitragem'])

def main():
  """Função principal com o menu de interação."""
  client = pymongo.MongoClient("mongodb://localhost:27017/")
  db = client['futebol']

  cenarios = {
    1: cenario_1_referencia,
    2: cenario_2_embutido,
    3: cenario_3_array_referencias,
    4: cenario_4_array_embutido
  }

  while True:
    print("\n----------------------------------")
    print("1: Cenário de Referência (1-1)")
    print("2: Cenário Embutido (1-1)")
    print("3: Cenário com Array de Referências (1-N)")
    print("4: Cenário com Array Embutido (1-N)")
    print("0: Sair")

    try:
      escolha = int(input("Escolha o cenário: "))
      if escolha == 0:
        print("Saindo...")
        break

      if escolha in cenarios:
        limpa_banco(db)
        cenarios[escolha](db)
      else:
        print("Opção inválida.")
        
    except ValueError:
      print("Por favor, digite um número.")
    except Exception as e:
      print(f"Ocorreu um erro: {e}")

  client.close()

if __name__ == "__main__":
  main()
