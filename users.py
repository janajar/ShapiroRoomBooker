import sqlite3
import bcrypt

def create_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def update_password(username, password):
    conn = sqlite3.connect('users.db')
    curs = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    curs.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()

def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def in_database(username, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    else:
        return False