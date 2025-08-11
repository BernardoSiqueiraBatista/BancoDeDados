import pymongo
from datetime import datetime

cliente = pymongo.MongoClient(mongodblocalhost27017)
meu_banco = cliente['futebol']

def scenario1()
    meu_banco.datas.delete_many({})
    meu_banco.campeonato.delete_many({})

    d1 = {_id 1, data datetime(2024, 1, 1)}
    d2 = {_id 2, data datetime(2025, 1, 1)}
    meu_banco.datas.insert_many([d1, d2])

    meu_banco.campeonato.insert_many([
        {_id 10, nome Brasileirao, data_id 1},
        {_id 20, nome Libertadores, data_id 1},
        {_id 30, nome CopaDoBrasil, data_id 2},
    ])

def query_scenario_1()
    data_str = input(Data (YYYY-MM-DD) ).strip()
    data_x = datetime.fromisoformat(data_str)

    doc_data = meu_banco.datas.find_one({data data_x})
    if not doc_data
        print(Data não cadastrada. Portanto, nenhum campeonato esta rolando nessa data)
        return

    campeonatos = meu_banco.campeonato.find({data_id doc_data[_id]}, {_id 0, nome 1})
    
    print(fnCampeonatos na data {data_str})
    
    if not campeonatos
        print((nenhum))
    else
        for c in campeonatos
            print(f- {c['nome']})

# CENÁRIO 2 — Embutido simples campeonato EMBUTE a data


def scenario_2()
    meu_banco.datas.delete_many({})
    meu_banco.campeonato.delete_many({})

    meu_banco.campeonato.insert_many([
        {
            _id 10, 
            nome Brasileirao, 
            data {_id 1, valor datetime(2024, 1, 1)}
        },
        {
            _id 20, 
            nome Libertadores, 
            data {_id 2, valor datetime(2024, 1, 1)}
        },
        {
            _id 30, 
            nome CopaDoBrasil, 
            data {_id 3, valor datetime(2025, 1, 1)}
        },
    ])

def query2()
    data_str = input(Data (YYYY-MM-DD) ).strip()
    data_x = datetime.fromisoformat(data_str)

    campeonatos = list(meu_banco.campeonato.find({data.valor data_x}, {_id 0, nome 1}))
    
    print(fnCampeonatos na data {data_str})
    
    if not campeonatos
        print((nenhum))
    else
        for c in campeonatos
            print(f- {c['nome']})



def scenario_3()
    meu_banco.datas.delete_many({})
    meu_banco.campeonato.delete_many({})

    ids = meu_banco.campeonato.insert_many([
        {nome Brasileirao},
        {nome Libertadores},
    ]).inserted_ids

    ids2 = meu_banco.campeonato.insert_many([
        {nome CopaDoBrasil},
    ]).inserted_ids

    meu_banco.datas.insert_many([
        {_id 1, data datetime(2024, 1, 1), campeonatos_ids ids},
        {_id 2, data datetime(2025, 1, 1), campeonatos_ids ids2},
    ])

def query3()
    data_str = input(Data (YYYY-MM-DD) ).strip()
    data_x = datetime.fromisoformat(data_str)

    doc_data = meu_banco.datas.find_one({data data_x}, {campeonatos_ids 1})
    if not doc_data or not doc_data.get(campeonatos_ids)
        print(Nenhum campeonato encontrado nessa data.)
        return

    campeonatos = meu_banco.campeonato.find(
        {_id {$in doc_data[campeonatos_ids]}},
        {_id 0, nome 1}
    )
    
    print(fnCampeonatos na data {data_str})
    
    if not campeonatos
        print((nenhum))
    else
        for c in campeonatos
            print(f- {c['nome']})


def scenario_4()
    meu_banco.datas.delete_many({})
    meu_banco.campeonato.delete_many({})

    meu_banco.datas.insert_many([
        {
            _id 1,
            data datetime(2024, 1, 1),
            campeonatos [
                {nome Brasileirao},
                {nome Libertadores},
            ]
        },
        {
            _id 2,
            data datetime(2025, 1, 1),
            campeonatos [
                {nome CopaDoBrasil}
            ]
        }
    ])

def query4()
    data_str = input(Data (YYYY-MM-DD) ).strip()
    data_x = datetime.fromisoformat(data_str)

    doc = meu_banco.datas.find_one({data data_x}, {_id 0, campeonatos 1})
    if not doc or not doc.get(campeonatos)
        print(Nenhum campeonato encontrado nessa data.)
        return

    print(fnCampeonatos na data {data_str})
    for c in doc[campeonatos]
        print(f- {c['nome']})



def main()
    opcoes_insert = {
        1 scenario1,
        2 scenario_2,
        3 scenario_3,
        4 scenario_4,
    }

    opcoes_query = {
        1 query_scenario_1,
        2 query2,
        3 query3,
        4 query4,
    }

    opcao = -1
    while opcao

        meu_banco.jogador.drop()
        meu_banco.clube.drop()

        meu_banco['jogador']
        meu_banco['clube']


        print(==============================================================================)
        print(1. Cenário 1)
        print(2. Cenário 2)
        print(3. Cenário 3)
        print(4. Cenário 4)
        print(0. Sair)


        try
            opcao = int(input(Escolha ))
            if opcao == 0
                print(Fim...)
            elif opcao in opcoes_insert
                print(==============================================================================)
                opcoes_insert[opcao]()
                opcoes_query[opcao]()
            else
                print(Opção inválida, tente novamente.)
        except
            print(Por favor, digite um número válido.)

main()
