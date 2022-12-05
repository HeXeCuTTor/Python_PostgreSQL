import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(80) NOT NULL,
                surname VARCHAR(80) NOT NULL
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS email(
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                clients_id INTEGER NOT NULL REFERENCES clients(id)
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                number VARCHAR(15) NOT NULL,
                clients_id INTEGER NOT NULL REFERENCES clients(id)
            );
            """)
            conn.commit()

def add_client(conn,name,surname):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO clients(name, surname) VALUES(%s, %s);""", (name,surname))
        conn.commit()

def add_email(conn,clients_id,email):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO email(email, clients_id) VALUES(%s, %s);""", (email,clients_id))
        conn.commit()

def add_phone(conn,clients_id, number):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phone(number, clients_id) VALUES(%s, %s);""", (number,clients_id))
        conn.commit()

def change_data_client(conn,old_name,new_name,old_surname,new_surname):
    with conn.cursor() as cur:
        cur.execute("""SELECT id FROM clients WHERE name=%s AND surname=%s;""", (old_name,old_surname))
        clients_id = cur.fetchone()[0]
    if new_name != '0' and new_surname == '0':
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET name=%s WHERE id=%s;""", (new_name, clients_id))
            cur.execute("""SELECT * FROM clients;""")
            print(cur.fetchall())
            conn.commit()
    elif new_name == '0' and new_surname != '0':
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET surname=%s WHERE id=%s;""", (new_surname, clients_id))
            cur.execute("""SELECT * FROM clients;""")
            print(cur.fetchall()) 
            conn.commit() 
    else:
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET name=%s WHERE id=%s;""", (new_name, clients_id))
            cur.execute("""SELECT * FROM clients;""")
            print(cur.fetchall())               
            cur.execute("""UPDATE clients SET surname=%s WHERE id=%s;""", (new_surname, clients_id))
            cur.execute("""SELECT * FROM clients;""")
            print(cur.fetchall())
            conn.commit()

def change_client_number(conn,old_number, new_number):
    with conn.cursor() as cur:
        cur.execute("""SELECT id FROM phone WHERE number=%s;""", (old_number,))
        phone_id = cur.fetchone()[0]
        cur.execute("""UPDATE phone SET number=%s WHERE id=%s;""", (new_number, phone_id))
        cur.execute("""SELECT * FROM phone;""")
        print(cur.fetchall())
        conn.commit()

def change_client_email(conn,old_email, new_email):
    with conn.cursor() as cur:
        cur.execute("""SELECT id FROM email WHERE email=%s;""", (old_email,))
        email_id = cur.fetchone()[0]
        cur.execute("""UPDATE email SET email=%s WHERE id=%s;""", (new_email, email_id))
        cur.execute("""SELECT * FROM email;""")
        print(cur.fetchall())
        conn.commit()

def delete_number(conn,name,surname):
    with conn.cursor() as cur:
        cur.execute("""SELECT id FROM clients WHERE name=%s AND surname=%s;""", (name,surname))
        clients_id = cur.fetchone()[0]
        cur.execute("""DELETE FROM phone WHERE clients_id=%s;""", (clients_id,))
        cur.execute("""SELECT * FROM phone;""")
        print(cur.fetchall()) 

def delete_clients_data(conn,name,surname):
    with conn.cursor() as cur:
        cur.execute("""SELECT id FROM clients WHERE name=%s AND surname=%s;""", (name,surname))
        clients_id = cur.fetchone()[0]
        cur.execute("""DELETE FROM phone WHERE clients_id=%s;""", (clients_id,))
        cur.execute("""SELECT * FROM phone;""")
        print(cur.fetchall())
        cur.execute("""DELETE FROM email WHERE clients_id=%s;""", (clients_id,))
        cur.execute("""SELECT * FROM email;""")
        print(cur.fetchall())
        cur.execute("""DELETE FROM clients WHERE id=%s;""", (clients_id,))
        cur.execute("""SELECT * FROM clients;""")
        print(cur.fetchall())
        conn.commit()
def find_client_data(conn,name,surname,email,number):
    with conn.cursor() as cur:
        if email != '0':
            cur.execute("""SELECT clients_id FROM email WHERE email=%s;""", (email,))
            clients_id = cur.fetchone()[0]
            cur.execute("""SELECT * FROM phone WHERE clients_id=%s;""", (clients_id,))
            print(cur.fetchall())
            cur.execute("""SELECT * FROM clients WHERE id=%s;""", (clients_id,))
            print(cur.fetchone()[1:3])
            return
        elif number != '0':
            cur.execute("""SELECT clients_id FROM phone WHERE number=%s;""", (number,))
            clients_id = cur.fetchone()[0]
            cur.execute("""SELECT * FROM email WHERE clients_id=%s;""", (clients_id,))
            print(cur.fetchall())
            cur.execute("""SELECT * FROM phone WHERE clients_id=%s;""", (clients_id,))
            print(cur.fetchall())
            cur.execute("""SELECT * FROM clients WHERE id=%s;""", (clients_id,))
            print(cur.fetchone()[1:3])
            return
        else:
            cur.execute("""SELECT id FROM clients WHERE name=%s AND surname=%s;""", (name,surname))
            clients_id = cur.fetchone()[0]
            print(clients_id)
            cur.execute("""SELECT * FROM email WHERE clients_id=%s;""", (clients_id,))
            print(cur.fetchall())
            cur.execute("""SELECT * FROM phone WHERE clients_id=%s;""", (clients_id,))
            print(cur.fetchall())                        


n = 1
while n == 1:
    programm = input("Открыть базу данных? Y/N ")
    if programm == 'Y':
        conn = psycopg2.connect(database = 'netology_db', user = 'postgres', password = 'postgres')
        create_db(conn)
        start = input("Введите команду: 'A' - добавить клиента\n'B' - добавить телефон или email\n'C' - изменить данные клиента\n'R' - изменить телефон или email клиента\n'D' - удалить данные клиента\n'F' - найти данные\n ")
        if start == 'A':
            name = input("Введите имя клиента: ")
            surname = input("Введите фамилию клиента: ")
            add_client(conn,name,surname)
        elif start == 'B':
            data = input("Телефон или email? T/E")
            if data == 'T':
                clients_id = input('Введите id клиента: ')
                number = input('Введите номер: ')
                add_phone(conn, clients_id, number)
            elif data == 'E':
                clients_id = input('Введите id клиента: ')
                email = input('Введите email: ')
                add_email(conn, clients_id, email)
        elif start == 'C':
            old_name = input("Старое имя? ")
            new_name = input("Новое имя?(Если нет - введите 0) ")
            old_surname = input("Старая фамилия? ")
            new_surname = input("Новая фамилия? (Если нет - введите 0) ")
            change_data_client(conn,old_name,new_name,old_surname,new_surname)
        elif start == 'R':
            data = input("Телефон или email? T/E")
            if data == 'T':
                old_number = input('Старый номер? ')
                new_number = input('Новый номер? ')
                change_client_number(conn,old_number, new_number)
            elif data == 'E':
                old_email = input('Старый email? ')
                new_email= input('Новый email? ')
                change_client_email(conn,old_email, new_email)            
        elif start == 'D':
            data = input("Удалить все данные или только телефон? A/T")
            if data == 'A':
                name = input("Введите имя: ")
                surname = input("Введите фамилию: ")
                delete_clients_data(conn,name,surname)
            elif data == 'T':
                name = input("Введите имя: ")
                surname = input("Введите фамилию: ")
                delete_clients_data(conn,name,surname)
        elif start == 'F':
            number = input("Телефон? (Если нет - введите 0) ")
            email = input("Email? (Если нет - введите 0) ")
            name = input("Имя? (Если нет - введите 0) ")
            surname = input("Фамилия? (Если нет - введите 0) ")
            if number == '0' and email == '0' and name == '0' and surname == '0':
                print('Not found')
            else:
               find_client_data(conn,name,surname,email,number)
        conn.close()                            
    elif programm == 'N':
        break