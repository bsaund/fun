import sqlite3 as sl
import pandas as pd

con = sl.connect('my-test.db')

with con:
    con.execute("""
    CREATE TABLE IF NOT EXISTS USER (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER
    );
    """)

sql = 'INSERT OR IGNORE INTO USER (id, name, age) values(?, ?, ?)'
data = [
    (1, 'Alice', 21),
    (2, 'Bob', 22),
    (3, 'Chris', 23)
]

with con:
    con.executemany(sql, data)

with con:
    data = con.execute("SELECT * FROM USER WHERE age <= 22")
    for row in data:
        print(row)

df = pd.read_sql('''
    SELECT u.id, u.name, u.age FROM User u''', con)


print(df)
