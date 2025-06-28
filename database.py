import sqlite3
import uuid


local_db = "database.db"

def init_db():
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS login (
            id TEXT PRIMARY KEY,
            code TEXT)''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            website TEXT,
            email TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()
    
    return cursor

def fetch_login(code):
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    cursor.execute('SELECT code FROM login WHERE code=?', (code,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def get_all_accounts():
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    conn.close()
    return accounts


def insert_account(id, website, email, password):
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO accounts (id, website, email, password)
        VALUES (?, ?, ?, ?)
    ''', (id, website, email, password))

    conn.commit()
    conn.close()
    


def update_account(id, website, email, password):
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Accounts
        SET Website = ?, Mail = ?, Password = ?
        WHERE id = ?
    ''', (website, email, password, id))

    conn.commit()
    conn.close()



#============================= Test Functions =============================

def insert_login_code():
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    id = str(uuid.uuid4())  # Generate a unique id
    code = "hello"
    cursor.execute('INSERT INTO login (id, code) VALUES (?, ?)', (id, code))
    conn.commit()
    conn.close()
    
    print("Login code inserted successfully.")
# insert_login_code()

