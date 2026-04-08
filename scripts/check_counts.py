import sqlite3
import os

BASE_DIR = os.getcwd()

def check_db(db_name):
    path = os.path.join(BASE_DIR, 'database', db_name)
    if not os.path.exists(path):
        print(f"{db_name} does not exist.")
        return
    
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nTables in {db_name}:")
    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} rows")
    conn.close()

check_db('blutdruck_input.db')
check_db('blutdruck_dwh.db')
