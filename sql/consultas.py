import sqlite3

connect = sqlite3.connect('futebol.db')
cursor = connect.cursor()

# Group by/Having
# Exibir a quantidade de pessoas por nacionalidade
def group_by():
    cursor.execute("""
        SELECT P.local_nacionalidade, COUNT(*) AS Quantidade
        FROM Pessoa P
        GROUP BY P.local_nacionalidade
        HAVING Quantidade > 0;
    """)
    
    print('\nGroup by/Having:')
    for i in cursor.fetchall():
        print(i)


# Junção interna
# Exibir os nomes e data de fundação dos clubes que participam de campeonato
def juncao_interna():
    cursor.execute("""
        SELECT C.nome, C.data_fundacao 
        FROM Participa P INNER JOIN Clube C 
            ON P.id_clube = C.id_clube;
    """)
  
    print('\nJunção interna:')
    for i in cursor.fetchall():
        print(i)



# Junção externa
# Exibir o Cpf das pessoas que não são jogadores
def juncao_externa(): 
    cursor.execute("""
        SELECT P.cpf
        FROM Pessoa P LEFT OUTER JOIN Jogador J
            ON P.cpf = J.cpf_jogador
        WHERE J.cpf_jogador IS NULL;
    """)

    print('\nJunção externa:')
    for i in cursor.fetchall():
        print(i)



# SEMI-JOIN
# Exibe os CPFs dos presidentes cujo clube foi fundado antes de 1970
def semi_join():
    cursor.execute("""
            SELECT P.cpf_presidente
            FROM Presidente P
            WHERE EXISTS (
                SELECT 1
                FROM Clube C
                WHERE C.id_clube = P.id_clube
                    AND  
                      C.data_fundacao < '1970-01-01'
            );
        """)
    
    print("\nOperação de Semi-Join:")
    for i in cursor.fetchall():
        print(i)




# ANTI-JOIN
# Exibe os CPFs dos presidentes cujos clubes foram fundados em 1950 ou depois
def anti_join():
    cursor.execute("""
            SELECT P.cpf_presidente
            FROM Presidente P
            WHERE NOT EXISTS (
                SELECT 1
                FROM Clube C
                WHERE C.id_clube = P.id_clube
                    AND  
                      C.data_fundacao < '1950-01-01'
            );
        """)
    
    print("\nOperação de Anti-Join:")
    for i in cursor.fetchall():
        print(i)



# Subconsulta escalar
# Exibir o cpf dos técnicos que tem mais tempo de experiência que a média
def subconsulta_escalar():
    cursor.execute("""
        SELECT T.cpf_tecnico
        FROM Tecnico T
        WHERE anos_experiencia >
                   (SELECT AVG(anos_experiencia)
                    FROM Tecnico);
    """)

    print('\nSubconsulta escalar:')
    for i in cursor.fetchall():
        print(i)




# Subconsulta em linha
# Exibir o Nome das pessoas que tem nacionalidade e naturalidade igual ao da pessoa com cpf = 12345678901
def subconsulta_em_linha():
    cursor.execute("""
        SELECT P1.nome
        FROM Pessoa P1
        WHERE (local_nacionalidade, local_naturalidade) =
                (SELECT P2.local_nacionalidade, P2.local_naturalidade
                FROM Pessoa P2
                WHERE CPF = "12345678901");
    """)
    print('\nSubconsulta em linha:')
    for i in cursor.fetchall():
        print(i)



# Subconsulta em tabela
# Exibir o Nome dos clubes que participam de campeonato
def subconsulta_tabela():
    cursor.execute("""
        SELECT C.nome
        FROM Clube C
        WHERE C.id_clube IN
            (SELECT P.id_clube
            FROM PARTICIPA P);    
    """)
    
    print("\nOperação de Subconsulta-Tabela:")
    for i in cursor.fetchall():
        print(i)



# Operacao conjunto
# Mostrar o CPF das pessoas que sao técnicos OU árbitros
def operacao_conjunto():
    cursor.execute("""
        SELECT cpf_tecnico
        FROM Tecnico
        UNION
        SELECT cpf_arbitro
        FROM Arbitro;
    """)
    print('\nOperação conjunto:')
    for i in cursor.fetchall():
        print(i)



def main():    
    escolha = 1
    opcoes = {    
        1: group_by,
        2: juncao_interna,
        3: juncao_externa,
        4: semi_join,
        5: anti_join,
        6: subconsulta_escalar,
        7: subconsulta_em_linha,
        8: subconsulta_tabela,
        9: operacao_conjunto,
    }


    while (escolha != 0):

        # cursor.execute("""
        #     SELECT * FROM Pessoa;
        # """)

        # for i in cursor.fetchall():
        #     print(i)

        print("0. Sair")
        print("1. Group by/Having")
        print("2. Junção interna")
        print("3. Junção externa")
        print("4. Semi-join")
        print("5. Anti-join")
        print("6. Subconsulta escalar")
        print("7. Subconsulta linha")
        print("8. Subcosulta tabela")
        print("9. Operacao conjunto")

        try:
            escolha = int(input("Escolha: "))
            if escolha == 0:
                print("Saindo...")
            elif escolha in opcoes:
                print("\n======================")
                opcoes[escolha]() 
                print("\n======================\n")
            else:
                print("\n========================")
                print("Opção inválida.")
                print("========================\n")
        except ValueError:
            print("Por favor, digite um número válido.")
            print("\n========================")
            print("Opção inválida.")
            print("========================\n")

    connect.close()

main()