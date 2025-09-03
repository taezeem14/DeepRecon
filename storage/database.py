import sqlite3

def init_db():
    conn = sqlite3.connect("storage/deeprecon.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        url TEXT,
        emails TEXT,
        btc TEXT,
        pgp TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_result(url, emails, btc, pgp):
    conn = sqlite3.connect("storage/deeprecon.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (url, emails, btc, pgp) VALUES (?, ?, ?, ?)", 
                   (url, ",".join(emails), ",".join(btc), ",".join(pgp)))
    conn.commit()
    conn.close()
