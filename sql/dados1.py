import sqlite3

conn = sqlite3.connect('futebol.db')
cursor = conn.cursor()

# Inserir Pessoas (cpf, nome, nascimento, nacionalidade, naturalidade)
pessoas = [
    ('12345678901', 'Neymar da Silva Santos Júnior', '1992-02-05', 'Brasil', 'Mogi das Cruzes'),
    ('23456789012', 'Gabriel Barbosa Almeida', '1996-08-30', 'Brasil', 'São Bernardo do Campo'),
    ('34567890123', 'Alisson Ramses Becker', '1992-10-02', 'Brasil', 'Novo Hamburgo'),
    ('45678901234', 'Casemiro', '1993-02-23', 'Brasil', 'São José dos Campos'),
    ('56789012345', 'Roberto Firmino', '1991-10-02', 'Brasil', 'Maceió'),
    ('67890123456', 'Thiago Silva', '1984-09-22', 'Brasil', 'Rio de Janeiro'),
    ('78901234567', 'Tite', '1961-05-25', 'Brasil', 'Caxias do Sul'),
    ('89012345678', 'Anderson Daronco', '1991-07-12', 'Brasil', 'Posadas'),
]

cursor.executemany("""
    INSERT INTO Pessoa (cpf, nome, nascimento, local_nacionalidade, local_naturalidade)
    VALUES (?, ?, ?, ?, ?);
""", pessoas)



# Inserir Clubes (id_clube, nome, data_fundacao)
clubes = [
    (1, 'Flamengo', '1895-11-17'),
    (2, 'Palmeiras', '1914-08-26'),
    (3, 'Grêmio', '1903-09-15'),
    (4, 'Corinthians', '1910-09-01'),
]

cursor.executemany("""
    INSERT INTO Clube (id_clube, nome, data_fundacao)
    VALUES (?, ?, ?);
""", clubes)



# Inserir jogadores (cpf_jogador, posicao, id_clube)
jogadores = [
    ('12345678901', 'Atacante', 1),  
    ('23456789012', 'Atacante', 2),
    ('34567890123', 'Goleiro', 3), 
    ('45678901234', 'Volante', 2), 
    ('56789012345', 'Atacante', 1),
    ('67890123456', 'Zagueiro', 4),
]

cursor.executemany("""
    INSERT INTO Jogador (cpf_jogador, posicao, id_clube)
    VALUES (?, ?, ?);
""", jogadores)


# Inserir Clubes_anteriores (CPF, Clube_anterior)
Clubes_anteriores = [
    ('12345678901', 'Sport'),
    ('12345678901', 'Atlético-MG'),
    ('12345678901', 'Botafogo'),  
    ('23456789012', 'Nautico'),
    ('23456789012', 'Avaí'),
    ('23456789012', 'Vitória'),
    ('34567890123', 'Santa Cruz'), 
    ('34567890123', 'Sport'), 
    ('45678901234', 'Palmeiras'), 
    ('56789012345', 'CSA'),
    ('67890123456', 'CRB'),
]

cursor.executemany("""
    INSERT INTO Clubes_anteriores (cpf_jogador, Clube_anterior)
    VALUES (?, ?);
""", Clubes_anteriores)


# Inserir técnicos (cpf_tecnico, licenca, anos_experiencia)
tecnicos = [
    ('78901234567', 'Licença A', 20)
]

cursor.executemany("""
    INSERT INTO Tecnico (cpf_tecnico, licenca, anos_experiencia)
    VALUES (?, ?, ?);
""", tecnicos)




# Inserir árbitros (cpf_Arbitro, cart_fifa)
arbitros = [
    ('89012345678', 1),
]

cursor.executemany("""
    INSERT INTO Arbitro (cpf_Arbitro, cart_fifa)
    VALUES (?, ?);
""", arbitros)




# Inserir campeonatos (id_campeonato, numero_times, nome)
campeonatos = [
    (1, 20, 'Campeonato Brasileiro Série A'),
    (2, 16, 'Copa do Brasil'),
]

cursor.executemany("""
    INSERT INTO Campeonato (id_campeonato, numero_times, nome)
    VALUES (?, ?, ?);
""", campeonatos)




# Tabela participa (id_campeonato, id_clube, data, colocacao)
participa = [
    (1, 1, '2023-01-01', 1),
    (1, 2, '2023-01-01', 2),
    (1, 3, '2023-01-01', 5),
    (2, 1, '2023-01-01', 1),
    (2, 4, '2023-01-01', 3),
]

cursor.executemany("""
    INSERT INTO Participa (id_campeonato, id_clube, data, colocacao)
    VALUES (?, ?, ?, ?);
""", participa)




conn.commit()
conn.close()
