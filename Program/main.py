from data.database.Database import *


database = Database(':memory:')

columns = [
    Column('ID', 'INTEGER', True),
    Column('Name', 'TEXT', False, False),
    Column('Age', 'INTEGER')
]

database.create_table('Vek', columns)

database.add_column('Vek', Column('Height', 'INTEGER'))

columns = [
    Column('ID', 'INTEGER', True, False, True),
    Column('Target', 'INTEGER'),
]

foreigns = [
    Foreign('Target', 'Vek', 'ID')
]

database.create_table('Translate', columns, foreigns)

database.insert('Vek', {
    'Name': 'Honza',
    'Age': 25,
    'Height': 180
})

database.insert('Vek', {
    'Name': 'Petr',
    'Age': 28,
    'Height': 175
})

for i in database.select('Vek', {'Name': 'Honza'}):
    print(i['ID'], i['Name'])

database.drop_table('Vek')
