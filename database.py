import sqlite3

def init_db():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        pocket_id TEXT,
        verified INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        pocket_id TEXT PRIMARY KEY
    )
    """)

    conn.commit()
    conn.close()

def add_user(telegram_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    conn.commit()
    conn.close()

def set_pocket_id(telegram_id, pocket_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET pocket_id=? WHERE telegram_id=?", (pocket_id, telegram_id))
    conn.commit()
    conn.close()

def verify_user(telegram_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET verified=1 WHERE telegram_id=?", (telegram_id,))
    conn.commit()
    conn.close()

def is_verified(telegram_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT verified FROM users WHERE telegram_id=?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()

    return result and result[0] == 1

def get_user(telegram_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT pocket_id, verified FROM users WHERE telegram_id=?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()

    return result

def check_registration(pocket_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations WHERE pocket_id=?", (pocket_id,))
    result = cursor.fetchone()
    conn.close()

    return result is not None

def add_registration(pocket_id):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO registrations (pocket_id) VALUES (?)", (pocket_id,))
    conn.commit()
    conn.close()
