import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def check_card(card):
    query = """SELECT count(number) FROM card WHERE number = ?"""
    data_tuple = (card,)
    cur.execute(query, data_tuple)
    rows = cur.fetchone()
    return rows[0] == 1

print(check_card(3000003972196503))



