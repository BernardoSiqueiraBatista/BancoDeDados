import sqlite3 as sql

conn = sql.connect('futebol.db')
cursor = conn.cursor()

#CAMPEONATO (ID, Nºtimes, Nome)
# cursor.execute("""
# CREATE TABLE Campeonato (
#     id_campeonato INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#     Numero_times INTEGER NOT NULL CHECK (Numero_times > 1),
#     Nome TEXT NOT NULL          
# );""")

# PATROCINADOR (ID, Setor, Nome)
# cursor.execute("""
# CREATE TABLE Patrocinador (
#     id_patrocinador INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#     Setor TEXT NOT NULL,
#     Nome TEXT NOT NULL
# );""")

# PARTIDA (ID, Data, Placar)
# A coluna Placar foi definida como texto por uma questão de semântica. No placar, armazenamos um inteiro
# que representa o total de gols do time mandante e outro inteiro para o total de gols do time visitante,
# mas precisamos de um separador para entender qual time está sendo referenciado por cada inteiro, e ele é 
# um caracter. Logo, iremos armazenar essa expressão 'int x int' como texto.
# cursor.execute("""
# CREATE TABLE Partida (
#     id_partida INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#     Data DATE NOT NULL,
#     Placar TEXT NOT NULL 
# );""")

# CLUBE (ID, Nome, Data_Fundacao)
# cursor.execute("""
# CREATE TABLE Clube (
#     id_clube INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#     Nome TEXT NOT NULL,
#     Data_fundação DATE NOT NULL
# );""")



# SÚMULA (ID, Cartão, Substituições)
# Súmula é uma entidade fraca de partica. Logo, o id é uma chave que vem da tabela Partida
# cursor.execute("""
# CREATE TABLE Súmula (
#     id_sumula INTEGER NOT NULL PRIMARY KEY,
#     Cartão TEXT,
#     Substituições INTEGER,
#     CONSTRAINT fk_partida FOREIGN KEY (id_sumula) REFERENCES Partida(id_partida)
# );""")



# PESSOA (CPF, Nome, Nascimento, local_Nacionalidade, local_Naturalidade)
# Pessoa é uma macroentidade. Dela, várias outras herdam informações.
# cursor.execute("""
# CREATE TABLE Pessoa (
#     Cpf VARCHAR(11) NOT NULL PRIMARY KEY,
#     Nome TEXT NOT NULL,
#     Nascimento DATE NOT NULL,
#     local_Nacionalidade TEXT NOT NULL,
#     local_Naturalidade TEXT NOT NULL
# );""")


conn.commit()
conn.close()
