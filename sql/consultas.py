import sqlite3

connect = sqlite3.connect('futebol.db')
cursor = connect.cursor()

# Group by/Having
# Exibir a quantidade de pessoas por nacionalidade
cursor.execute("""
    SELECT P.local_nacionalidade, COUNT(*) AS Quantidade
    FROM Pessoa P
    GROUP BY P.local_nacionalidade
    HAVING Quantidade > 0;
""")
print('Group by/Having:')
print(cursor.fetchall())




# Junção interna
# Exibir os nomes e data de fundação dos clubes que participam de campeonato
cursor.execute("""
    SELECT C.nome, C.data_fundacao 
    FROM Participa P INNER JOIN Clube C 
        ON P.id_clube = C.id_clube;
""")
print('\nJunção interna:')
print(cursor.fetchall())




# Junção externa
# Exibir o Cpf das pessoas que não são jogadores
cursor.execute("""
    SELECT P.cpf
    FROM Pessoa P LEFT OUTER JOIN Jogador J
    ON P.cpf = J.cpf_jogador
    WHERE J.cpf_jogador IS NULL;
""")
print('\nJunção externa:')
print(cursor.fetchall())




# Subconsulta escalar
# Exibir a quantidade de jogadores que nasceram a partir de 1995
cursor.execute("""
    SELECT (
        SELECT COUNT(*)
        FROM Jogador J
        INNER JOIN PESSOA p on J.cpf_jogador = p.cpf
        WHERE p.nascimento >= '1995-01-01'
    ) AS quantidade_jogadores;
""")
print('\nSubconsulta escalar:')
print(cursor.fetchone())




# Subconsulta em linha
# Obter nome e data de fundacao do clube mais antigo
cursor.execute("""
    SELECT nome, data_fundacao
    FROM Clube
    WHERE (nome, data_fundacao) = (
        SELECT nome, data_fundacao
        FROM Clube
        ORDER BY data_fundacao
        LIMIT 1
    );
""") 
print('\nSubconsulta em linha:')
print(cursor.fetchall())




# Operacao conjunto
# Mostrar o CPF das pessoas que sao técnicos OU árbitros
cursor.execute("""
    SELECT cpf_tecnico as cpf
    FROM Tecnico
    UNION
    SELECT cpf_arbitro
    FROM Arbitro;
""")
print('\nOperação conjunto:')
print(cursor.fetchall())

    # SEMI-JOIN
    # Exibe os CPFs dos presidentes cujos clubes foram fundados antes de 1970
    # -------------------------------------------------------------
cursor.execute("""
        SELECT DISTINCT pr.cpf_presidente
        FROM   Presidente pr
        WHERE  EXISTS (
               SELECT 1
               FROM   Clube c
               WHERE  c.id_clube       = pr.id_clube
                 AND  c.data_fundacao < '1970-01-01'
        );
    """)
print("\nOperação de Semi-Join:")
print(cursor.fetchall())

    # -------------------------------------------------------------
    # ANTI-JOIN
    # Exibe os CPFs dos presidentes cujos clubes foram fundados em 1950 ou depois
    # (ou seja, não existe clube vinculado fundado antes de 1950)
    # -------------------------------------------------------------
cursor.execute("""
        SELECT DISTINCT pr.cpf_presidente
        FROM   Presidente pr
        WHERE  NOT EXISTS (
               SELECT 1
               FROM   Clube c
               WHERE  c.id_clube       = pr.id_clube
                 AND  c.data_fundacao < '1950-01-01'
        );
    """)
print("\nOperação de Anti-Join:")
print(cursor.fetchall())

    # -------------------------------------------------------------
    # SUBCONSULTA-TABELA (derived table)
    # Exibe o CPF e o nome do clube dos jogadores que marcaram
    # três ou mais gols em uma única partida
    # -------------------------------------------------------------
cursor.execute("""
        SELECT t.cpf,
               c.nome AS clube
        FROM (
               SELECT g.cpf,
                      g.id_clube,
                      g.id_partida,
                      COUNT(*) AS qtd_gols
               FROM   Gol g
               GROUP  BY g.cpf, g.id_clube, g.id_partida
               HAVING COUNT(*) >= 3
             ) AS t
        JOIN Clube c ON c.id_clube = t.id_clube;
    """)
print("\nOperação de Subconsulta-Tabela:")
print(cursor.fetchall())








 

resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

connect.close()
