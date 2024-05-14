import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )

    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS `filmesvideo`;")

    cursor.execute("CREATE DATABASE `filmesvideo`;")

    cursor.execute("USE `filmesvideo`;")

    # criando tabelas
    TABLES = {}
    TABLES['Filmes'] = ('''
          CREATE TABLE `filmes` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `nome` varchar(50) NOT NULL,
          `categoria` varchar(40) NOT NULL,
          `streaming` varchar(20) NOT NULL,
          PRIMARY KEY (`id`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    TABLES['Usuarios'] = ('''
          CREATE TABLE `usuarios` (
          `nome` varchar(20) NOT NULL,
          `nickname` varchar(8) NOT NULL,
          `senha` varchar(100) NOT NULL,
          PRIMARY KEY (`nickname`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    for tabela_nome in TABLES:
        tabela_sql = TABLES[tabela_nome]
        try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Já existe')
            else:
                print(err.msg)
        else:
            print('OK')

    # inserindo usuarios
    usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
    usuarios = [
        ("Davi", "davilm2", generate_password_hash("12345").decode('utf-8')),
        ("Clara", "cla", generate_password_hash("1903").decode('utf-8')),
        ("Maria", "cla2", generate_password_hash("2202").decode('utf-8'))
    ]
    cursor.executemany(usuario_sql, usuarios)

    cursor.execute('select * from filmesvideo.usuarios')
    print(' -------------  Usuários:  -------------')
    for user in cursor.fetchall():
        print(user[1])

    # inserindo filmes
    filmes_sql = 'INSERT INTO filmes (nome, categoria, streaming) VALUES (%s, %s, %s)'
    filmes = [
        ('Lost in Translation', 'Drama', 'Netflix'),
        ('Poderoso Chefão: parte 1', 'Drama', 'HBO Max'),
        ('Paris,Texas', 'Drama', 'Mubi'),
        ('Frances Ha', 'Drama', 'Mubi'),
        ('Trainspotting', 'Drama/Comédia', 'HBO Max'),
        ('Yi Yi', 'Drama', 'nenhum'),
    ]
    cursor.executemany(filmes_sql, filmes)

    cursor.execute('select * from filmesvideo.filmes')
    print(' -------------  Filmes:  -------------')
    for filme in cursor.fetchall():
        print(filme[1])

    # commitando se não nada tem efeito
    conn.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

finally:
    if 'conn' in locals() or 'conn' in globals():
        cursor.close()
        conn.close()
