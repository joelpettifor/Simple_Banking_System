import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()

c.execute("SELECT * FROM card")
print(c.fetchall())