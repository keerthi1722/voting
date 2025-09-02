import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect("voting.db")
cursor = conn.cursor()

# Create Voters Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        voter_id TEXT UNIQUE NOT NULL,
        has_voted INTEGER DEFAULT 0
    )
''')

# Create Candidates Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        votes INTEGER DEFAULT 0
    )
''')

# Insert Sample Candidates (Run only once)
cursor.execute("INSERT INTO candidates (name, votes) VALUES ('Alice', 0), ('Bob', 0)")

# Save and close
conn.commit()
conn.close()

print("Database setup complete. Tables created successfully!")
