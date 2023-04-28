import sqlite3
import tkinter as tk

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


def add_new_pass():
    add_pass_window = tk.Toplevel(root)
    site_var = tk.StringVar()
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    tk.Label(add_pass_window, text="Site").pack()
    site_entry = tk.Entry(add_pass_window, textvariable=site_var)
    site_entry.pack()
    tk.Label(add_pass_window, text="Username").pack()
    username_entry = tk.Entry(
        add_pass_window, textvariable=username_var)
    username_entry.pack()
    tk.Label(add_pass_window, text="Senha").pack()
    password_entry = tk.Entry(
        add_pass_window, show='*', textvariable=password_var)
    password_entry.pack()

    def save_pass_output():
        site = site_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        add_passwords(site, username, password)
        result_label.config(text="Senha salva!")
    tk.Button(add_pass_window, text="Salvar", command=save_pass_output).pack()
    result_label = tk.Label(add_pass_window, text="")
    result_label.pack()


def search_in_db():
    search_pass_db = tk.Toplevel(root)
    search_var = tk.StringVar()

    tk.Label(search_pass_db,
             text="Informe o nome do site que deseja buscar a senha").pack()
    search_entry = tk.Entry(search_pass_db, textvariable=search_var)
    search_entry.pack()

    def show_password():
        site = search_entry.get()
        result = search_passwords(site)
        if result:
            output_label.config(
                text=f"Site: {result['Site']}\nUsername: {result['Username']}\nPassword: {result['password']}")
        else:
            output_label.config(text='Senha não encontrada')
    tk.Button(search_pass_db, text='Search', command=show_password).pack()
    output_label = tk.Label(search_pass_db, text='')
    output_label.pack()

def search_one_pass(site):
    cursor.execute("SELECT * FROM passwords WHERE site=?", (site,))
    rows = cursor.fetchone()
    return rows
    
def update_password_gui():
    update_password_window = tk.Toplevel(root)

    tk.Label(update_password_window, text="Site").grid(row=0, column=0)
    site_entry = tk.Entry(update_password_window)
    site_entry.grid(row=0, column=1)

    tk.Label(update_password_window, text="Username").grid(row=1, column=0)
    username_entry = tk.Entry(update_password_window)
    username_entry.grid(row=1, column=1)

    tk.Label(update_password_window, text="Password").grid(row=2, column=0)
    password_entry = tk.Entry(update_password_window, show='*')
    password_entry.grid(row=2, column=1)
    
    def update_password_command():
        site = site_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        result = search_one_pass(site)
        if result is None: 
             output_label.config(text='Site não encontrado', fg='red')
        else:      
            update_password(site, username, password)
            output_label.config(text='Site atualizado', fg='green')
    tk.Button(update_password_window, text='Update password', command=update_password_command).grid(row=3, column=0, columnspan=2)
    output_label = tk.Label(update_password_window, text='')
    output_label.grid(row=4, column=0, columnspan=2)


root = tk.Tk()

menubar = tk.Menu(root)
root.config(menu=menubar)


label = tk.Label(root, text="Gerenciador de senhas", font='Verdana, 24')
label.pack()

arquivo_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="O que deseja fazer?", menu=arquivo_menu)
arquivo_menu.add_command(label="Adicionar nova senha", command=add_new_pass)
arquivo_menu.add_command(label="Buscar senha", command=search_in_db)
arquivo_menu.add_command(label="Atualizar senha", command=update_password_gui)
arquivo_menu.add_command(label="Remover senha")

arquivo_menu.add_separator()
arquivo_menu.add_command(label="Sair", command=root.quit)


root.mainloop()
