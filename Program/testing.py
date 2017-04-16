import sqlite3 as lite

con = lite.connect('test.db')

cur = con.cursor()

data = '\n'.join(con.iterdump())

with open('text.txt', 'w') as f:
    f.write(data)