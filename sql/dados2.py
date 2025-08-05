import sqlite3

def popular_banco():
    """
    Função para conectar ao banco de dados e inserir uma vasta quantidade de dados
    para popular todas as tabelas e testar as consultas.
    """
    try:
        connect = sqlite3.connect('futebol.db')
        cursor = connect.cursor()
        print("Conectado ao banco de dados. Iniciando a inserção de dados...")

        # --- Inserção de Pessoas ---
        # CPFs de 1 a 10 são jogadores.
        # CPFs 11 a 13 são técnicos.
        # CPFs 14 a 16 são árbitros.
        # CPFs 17 a 19 são presidentes.
        # CPF '12345678901' é um caso especial para a subconsulta de linha.
        # Outras pessoas (20-22) não são jogadores para testar a junção externa.
        pessoas = [
            # Jogadores
            ('00000000001', 'Artur Friedenreich', '1892-07-18', 'Brasil', 'São Paulo'),
            ('00000000002', 'Zico', '1953-03-03', 'Brasil', 'Rio de Janeiro'),
            ('00000000003', 'Pelé', '1940-10-23', 'Brasil', 'Três Corações'),
            ('00000000004', 'Garrincha', '1933-10-28', 'Brasil', 'Magé'),
            ('00000000005', 'Sócrates', '1954-02-19', 'Brasil', 'Belém'),
            ('00000000006', 'Marta', '1986-02-19', 'Brasil', 'Dois Riachos'),
            ('00000000007', 'Lionel Messi', '1987-06-24', 'Argentina', 'Rosário'),
            ('00000000008', 'Cristiano Ronaldo', '1985-02-05', 'Portugal', 'Funchal'),
            ('00000000009', 'Diego Maradona', '1960-10-30', 'Argentina', 'Lanús'),
            ('00000000010', 'Johan Cruyff', '1947-04-25', 'Holanda', 'Amsterdã'),
            # Técnicos (com diferentes anos de experiência para a média)
            ('00000000011', 'Telê Santana', '1931-07-26', 'Brasil', 'Itabirito'),
            ('00000000012', 'Pep Guardiola', '1971-01-18', 'Espanha', 'Santpedor'),
            ('00000000013', 'Tite', '1961-05-25', 'Brasil', 'Caxias do Sul'),
            # Árbitros
            ('00000000014', 'Arnaldo Cézar Coelho', '1943-01-15', 'Brasil', 'Rio de Janeiro'),
            ('00000000015', 'Pierluigi Collina', '1960-02-13', 'Itália', 'Bolonha'),
            ('00000000016', 'Fernanda Colombo', '1991-04-24', 'Brasil', 'Criciúma'),
            # Presidentes
            ('00000000017', 'João Havelange', '1916-05-08', 'Brasil', 'Rio de Janeiro'),
            ('00000000018', 'Paulo Nobre', '1968-02-24', 'Brasil', 'São Paulo'),
            ('00000000019', 'Vicente Calderón', '1913-05-27', 'Espanha', 'Torrelavega'),
            # Pessoas que não são jogadores
            ('00000000020', 'Galvão Bueno', '1950-07-21', 'Brasil', 'Rio de Janeiro'),
            ('00000000021', 'Juca Kfouri', '1950-03-04', 'Brasil', 'São Paulo'),
            # Pessoa especial para subconsulta de linha
            ('12345678901', 'José da Silva', '1980-01-01', 'Portugal', 'Lisboa'),
            ('00000000022', 'Maria Pereira', '1982-05-10', 'Portugal', 'Lisboa'),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Pessoa (cpf, nome, nascimento, local_nacionalidade, local_naturalidade) VALUES (?, ?, ?, ?, ?)", pessoas)

        # --- Inserção de Clubes ---
        # Com datas antes de 1950, entre 1950 e 1970, e depois de 1970
        clubes = [
            (1, 'Flamengo', '1895-11-17'),
            (2, 'Vasco da Gama', '1898-08-21'),
            (3, 'Corinthians', '1910-09-01'),
            (4, 'Palmeiras', '1914-08-26'),
            (5, 'Santos', '1912-04-14'),
            (6, 'São Paulo', '1930-01-25'),
            (7, 'Real Madrid', '1902-03-06'),
            (8, 'Barcelona', '1899-11-29'),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Clube (id_clube, nome, data_fundacao) VALUES (?, ?, ?)", clubes)

        # --- Inserção de Presidentes ---
        presidentes = [
            ('00000000017', 1, '1958-01-01', '1971-01-01'), # Clube antes de 1950/1970
            ('00000000018', 4, '2013-01-21', '2016-12-15'), # Clube antes de 1950/1970
            ('00000000019', 7, '1964-06-17', '1980-03-12'), # Clube antes de 1950/1970
        ]
        cursor.executemany("INSERT OR IGNORE INTO Presidente (cpf_presidente, id_clube, data_inicio_mandato, data_fim_mandato) VALUES (?, ?, ?, ?)", presidentes)

        # --- Inserção de Técnicos ---
        tecnicos = [
            ('00000000011', 'PRO-A', 40), # Alta experiência
            ('00000000012', 'PRO-A', 15), # Média experiência
            ('00000000013', 'PRO-B', 10), # Baixa experiência (vai estar abaixo da média)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Tecnico (cpf_tecnico, licenca, anos_experiencia) VALUES (?, ?, ?)", tecnicos)

        # --- Inserção de Árbitros ---
        arbitros = [
            ('00000000014', True),
            ('00000000015', True),
            ('00000000016', False),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Arbitro (cpf_Arbitro, cart_fifa) VALUES (?, ?)", arbitros)

        # --- Inserção de Jogadores ---
        jogadores = [
            ('00000000002', 'Meia', 1),
            ('00000000003', 'Atacante', 5),
            ('00000000004', 'Ponta Direita', 2),
            ('00000000005', 'Meia', 3),
            ('00000000006', 'Atacante', 4),
            ('00000000007', 'Atacante', 8),
            ('00000000009', 'Meia', 2),
            ('00000000010', 'Atacante', 8),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Jogador (cpf_jogador, posicao, id_clube) VALUES (?, ?, ?)", jogadores)

        # --- Inserção de Campeonatos e Partidas ---
        campeonatos = [(1, 8, 'Campeonato Brasileiro'), (2, 4, 'Copa do Mundo')]
        cursor.executemany("INSERT OR IGNORE INTO Campeonato (id_campeonato, numero_times, nome) VALUES (?, ?, ?)", campeonatos)
        
        partidas = [
            (1, '2023-10-28', '3x1'),
            (2, '2023-11-04', '2x2'),
            (3, '2023-11-12', '0x1'),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Partida (id_partida, data, placar) VALUES (?, ?, ?)", partidas)

        # --- Relacionamentos ---
        
        # Participa (para junção interna e subconsulta)
        participacoes = [
            (1, 1, '2023-01-01', 1),
            (1, 2, '2023-01-01', 2),
            (1, 3, '2023-01-01', 3),
            (1, 4, '2023-01-01', 4),
            (2, 5, '2022-01-01', 1),
            (2, 7, '2022-01-01', 2),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Participa (id_campeonato, id_clube, data, colocacao) VALUES (?, ?, ?, ?)", participacoes)
        
        # Gols (lembrando, um por jogador por partida)
        gols = [
            ('00000000002', 1, 1), # Zico marcou na partida 1 pelo Flamengo
            ('00000000003', 1, 5), # Pelé marcou na partida 1 pelo Santos
            ('00000000007', 2, 8), # Messi marcou na partida 2 pelo Barcelona
            ('00000000009', 2, 2), # Maradona marcou na partida 2 pelo Vasco
            ('00000000002', 3, 1), # Zico marcou na partida 3 pelo Flamengo
        ]
        cursor.executemany("INSERT OR IGNORE INTO Gol (cpf_jogador, id_partida, id_clube) VALUES (?, ?, ?)", gols)
        
        connect.commit()
        print("Dados inseridos com sucesso!")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao popular o banco de dados: {e}")
    finally:
        if connect:
            connect.close()
            print("Conexão com o banco de dados fechada.")


popular_banco()