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


def menu():
    print("1 - Adicionar nova senha")
    print("2 - Buscar senha")
    print("3 - Atualizar senha")
    print("4 - Remover senha")
    print("5 - Encerrar programa")


def add():
    site = input('Informe o nome do site: ')
    username = input('Informe o nome de usuário: ')
    password = input('Informe a senha: ')
    add_passwords(site, username, password)
    print('Senha cadastrada com sucesso!')


def search():
    site = input('Informe o nome do site que deseja buscar a senha: ')
    result = search_passwords(site)
    if result:
        print(result['Username'])
        print(result['password'])
    else:
        print('Senha não encontrada')


def update():
    site = input('Informe o site que deseja atualizar a senha: ')
    username = input('Informe o nome de usuário: ')
    password = input('Informe a nova senha:')
    update_password(site, username, password)


def remove():
    site = input('Informe o site que deseja remover:')
    remove_password(site)
    print('Senha removida com sucesso!')

options = {
    1: add,
    2: search,
    3: update,
    4: remove
}

while True:
    menu()
    choice = input('Informe a opção desejada: ')
    try:
        choice = int(choice)
    except:
        print('Opção precisa ser um número inteiro.')

    if choice == 5:
        print('Encerrando programa.')
        break
    elif choice in options:
        options[choice]()
    else:
        print('Escolha uma opção válida.')
