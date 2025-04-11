
import sqlite3
import os

os.makedirs('./db', exist_ok=True)

conn = sqlite3.connect('./db/database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_type TEXT NOT NULL,
    code TEXT NOT NULL,
    timestamp TIMESTAMP,
    description TEXT,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Database and table created.")
