import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, ?)
""", ("Test User", "test@gmail.com", "123456", "patient"))

conn.commit()
conn.close()

print("✅ Test user inserted")