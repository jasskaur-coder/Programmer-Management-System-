import sqlite3


conn = sqlite3.connect("programmers.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS programmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    salary REAL NOT NULL,
    pin INTEGER UNIQUE NOT NULL,
    experience INTEGER NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("\n✅ Database setup complete!")
