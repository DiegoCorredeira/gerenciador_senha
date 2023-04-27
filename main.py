import sqlite3

conn = sqlite3.connect('passwords.db')

cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS passwords
               (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT, username TEXT, password TEXT)
               ''')
conn.commit()


def add_passwords(site, username, password):
    cursor.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)",
                   (site, username, password))
    conn.commit()


def search_passwords(site):
    cursor.execute("SELECT * FROM passwords WHERE site=?", (site,))
    result = cursor.fetchone()
    if result:
        return {'Site': result[1], 'Username': result[2], 'password': result[3]}
    else:
        return ''


def update_password(site, username, password):
    cursor.execute("UPDATE passwords SET username=?, password=?, site=?",
                   (username, password, site))
    conn.commit()


def remove_password(site):
    cursor.execute("DELETE FROM passwords WHERE site=?", (site,))
    conn.commit()


flag = ''
while flag != 'sair':
    print("1 - Adicionar nova senha")
    print("2 - Buscar senha")
    print("3 - Atualizar senha")
    print("4 - Remover senha")
    print("5 - Encerrar programa")
    choice = input('Informe a opção desejada: ')
    try:
        choice = int(choice)
    except:
        print('Opção precisa ser um número inteiro.')

    if choice == 1:
        site = input('Informe o nome do site: ')
        username = input('Informe o nome de usuário: ')
        password = input('Informe a senha: ')

        add_passwords(site, username, password)
        print('Senha cadastrada com sucesso!')
    elif choice == 2:
        site = input('Informe o nome do site que deseja buscar a senha: ')
        result = search_passwords(site)
        if result:
            print(result['Username'])
            print(result['password'])
        else:
            print('Senha não encontrada')
    elif choice == 3: 
        site = input('Informe o site que deseja atualizar a senha: ')
        username = input('Informe o nome de usuário: ')
        password = input('Informe a nova senha:') 
        update_password(site, username, password)
    elif choice == 4: 
        site = input('Informe o site que deseja remover:')
        remove_password(site)
        print('Senha removida com sucesso!')
    elif choice == 5:
        flag = 'sair'
        print('Encerrando programa.')
    else: 
        print('Escolha uma opção válida.')