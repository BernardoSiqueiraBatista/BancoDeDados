import sqlite3

connect = sqlite3.connect('futebol.db')
cursor = connect.cursor()

# -Group by/Having
# Exibir a quantidade de pessoas por nacionalidade
cursor.execute("""
    SELECT P.local_nacionalidade, COUNT(*) AS Quantidade
    FROM Pessoa P
    GROUP BY P.local_nacionalidade
    HAVING Quantidade > 0;
""")



# -Junção interna
# Exibir os nomes e data de fundação dos clubes que participam de campeonato
cursor.execute("""
    SELECT C.nome, C.data_fundacao 
    FROM Participa P INNER JOIN Clube C 
        ON P.id_clube = C.id_clube;
""")

connect.close()