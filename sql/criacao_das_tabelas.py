import sqlite3 

connect = sqlite3.connect('futebol.db')
cursor = connect.cursor()



# CAMPEONATO (ID, Nºtimes, Nome)
cursor.execute("""
    CREATE TABLE Campeonato (
        id_campeonato INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        numero_times INTEGER NOT NULL CHECK (numero_times > 1),
        nome TEXT NOT NULL          
    );
""")



# PATROCINADOR (ID, Setor, Nome)
cursor.execute("""
    CREATE TABLE Patrocinador (
        id_patrocinador INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        setor TEXT NOT NULL,
        nome TEXT NOT NULL
    );
""")



# PARTIDA (ID, Data, Placar)
cursor.execute("""
    CREATE TABLE Partida (
        id_partida INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        placar TEXT NOT NULL 
    );
""")



# CLUBE (ID, Nome, Data_Fundacao)
cursor.execute("""
    CREATE TABLE Clube (
        id_clube INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_fundacao DATE NOT NULL
    );
""")



# SÚMULA (ID, Cartão, Substituições)

cursor.execute("""
    CREATE TABLE Sumula (
        id_partida INTEGER NOT NULL PRIMARY KEY,
        quantidade_cartoes INTEGER,
        substituicoes INTEGER,
        
        CONSTRAINT fk_partida FOREIGN KEY (id_partida) REFERENCES Partida (id_partida)
    );
""")



# PESSOA (CPF, Nome, Nascimento, local_Nacionalidade, local_Naturalidade)
# Pessoa é uma macroentidade. Dela, várias outras herdam informações.
cursor.execute("""
    CREATE TABLE Pessoa (
        cpf VARCHAR(11) NOT NULL PRIMARY KEY,
        nome TEXT NOT NULL,
        nascimento DATE NOT NULL,
        local_nacionalidade TEXT NOT NULL,
        local_naturalidade TEXT NOT NULL
    );
""")



# PRESIDENTE (CPF, [ID_CLUBE]!, data_incio, data_fim)
#    CPF -> PESSOA (CPF)
cursor.execute("""
    CREATE TABLE Presidente (
        cpf_presidente VARCHAR(11),
        id_clube INTEGER NOT NULL UNIQUE,
        data_inicio_mandato DATE NOT NULL,
        data_fim_mandato DATE NOT NULL,
        
        PRIMARY KEY (cpf_presidente),
        FOREIGN KEY (id_clube) REFERENCES Clube (id_clube),  
        FOREIGN KEY (cpf_presidente) REFERENCES Pessoa(cpf)
    );
""")



# ÁRBITRO (CPF, cart_fifa)
#     CPF -> PESSOA (CPF)
cursor.execute("""
    CREATE TABLE Arbitro (
        cpf_Arbitro VARCHAR(11) PRIMARY KEY,
        cart_fifa BOOL NOT NULL,

        CONSTRAINT fk_pessoa_arbitro FOREIGN KEY (cpf_Arbitro) REFERENCES Pessoa(cpf)
    );
""")


# TÉCNICO (CPF, LICENÇA, ANOS DE EXPERIÊNCIA)
#   CPF -> PESSOA (CPF)
cursor.execute("""
    CREATE TABLE Tecnico (
        cpf_tecnico VARCHAR(11) PRIMARY KEY,
        licenca TEXT NOT NULL,
        anos_experiencia INTEGER NOT NULL,

        CONSTRAINT fk_pessoa_tecnico FOREIGN KEY (cpf_tecnico) REFERENCES Pessoa (cpf)
    );
""")



# JOGADOR (CPF, Posição, ID_Clube!)
# 	CPF -> PESSOA (CPF)
# 	ID_Clube -> CLUBE (ID)

cursor.execute("""
    CREATE TABLE Jogador (
        cpf_jogador VARCHAR(11) PRIMARY KEY,
        posicao TEXT NOT NULL,
        id_clube INTEGER NOT NULL,
        
        CONSTRAINT fk_pessoa_jogador FOREIGN KEY (cpf_jogador) REFERENCES Pessoa(cpf),
        CONSTRAINT fk_clube_jogador FOREIGN KEY (id_clube) REFERENCES Clube (id_clube)
    );
""")



# CLUBES ANTERIORES (CPF, Clube anterior)
# 	CPF -> PESSOA (CPF)
cursor.execute("""
    CREATE TABLE Clubes_anteriores (
        cpf_jogador VARCHAR(11),
        clube_anterior VARCHAR(50),
        
        CONSTRAINT fk_pessoa_jogador FOREIGN KEY (cpf_jogador) REFERENCES Pessoa(cpf),
        CONSTRAINT pk_clubes_anteriores PRIMARY KEY (cpf_jogador, clube_anterior)
    );
""")



# PARTICIPA (ID_Campeonato, ID_Clube, Colocação)
# 	ID_Camp -> CAMPEONATO (ID)
# 	ID_Clube -> CLUBE (ID)
cursor.execute("""
    CREATE TABLE Participa (
        id_campeonato INTEGER,
        id_clube INTEGER,
        data DATE,
        colocacao INTEGER,

        CONSTRAINT fk_campeonato_participa FOREIGN KEY (id_campeonato) REFERENCES Campeonato (id_campeonato),
        CONSTRAINT fk_clube_participa FOREIGN KEY (id_clube) REFERENCES Clube (id_clube),
        CONSTRAINT pk_participa PRIMARY KEY (id_campeonato, id_clube, data)
    );
""")



# PATROCINADO (ID_Clube, ID_Camp, ID_Patroc, Colocação)
# 	(ID_Clube, ID_Camp, Colocacao) → PARTICIPA (ID_Clube, ID_Camp, Colocacao)
# 	ID_Patroc -> PATROCINADOR (ID)

cursor.execute("""
    CREATE TABLE Patrocinado (
        id_campeonato INTEGER,
        id_clube INTEGER,
        id_patrocinador INTEGER,
        data DATE,
        
        CONSTRAINT fk_participa FOREIGN KEY (id_campeonato, id_clube, data) REFERENCES Participa (id_campeonato, id_clube, data),
        CONSTRAINT fk_patrocinador_patrocinado FOREIGN KEY (id_patrocinador) REFERENCES Patrocinador (id_patrocinador),

        CONSTRAINT pk_patrocinado PRIMARY KEY (id_campeonato, id_clube, id_patrocinador, data)
    );
""")



# É RIVAL (ID_Riv1, ID_Riv2) 
# 	ID_Riv1 -> CLUBE (ID)
# 	ID_Riv2 -> CLUBE (ID)
cursor.execute("""
    CREATE TABLE Rival (
        id_rival1 INTEGER,
        id_rival2 INTEGER,

        CONSTRAINT fk_clube1_Rival FOREIGN KEY (id_rival1) REFERENCES Clube (id_clube),
        CONSTRAINT fk_clube2_Rival FOREIGN KEY (id_rival2) REFERENCES Clube (id_clube),
               
        CONSTRAINT pk_rival PRIMARY KEY (id_rival1, id_rival2)
    );
""")



# GOL (CPF, ID_Partida, ID_Clube!)
# 	CPF -> PESSOA (CPF)
# 	ID_Partida -> PARTIDA (ID)
# 	ID_Clube -> CLUBE (ID)
cursor.execute("""
    CREATE TABLE Gol (
        cpf_jogador VARCHAR(11),
        id_partida INTEGER,
        id_clube INTEGER NOT NULL,

        CONSTRAINT fk_jogador_gol FOREIGN KEY (cpf_jogador) REFERENCES Pessoa (cpf),
        CONSTRAINT fk_partida FOREIGN KEY (id_partida) REFERENCES Partida (id_partida),
        CONSTRAINT fk_clube FOREIGN KEY (id_clube) REFERENCES Clube (id_clube),

        CONSTRAINT pk_gol PRIMARY KEY (cpf_jogador, id_partida)      
    );
""")


connect.commit()
connect.close()
