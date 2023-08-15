import sqlite3

connection = sqlite3.connect('database.retail')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO products (code, name, category) VALUES (?, ?, ?)",
            ('PRD0001', 'Parachute hair oil 250ML', 'Beauty & Hair care')
            )

cur.execute("INSERT INTO products (code, name, category) VALUES (?, ?, ?)",
            ('PRD0002', 'DM Almond Choc 200MG', "Confectionary")
            )

connection.commit()
connection.close()

