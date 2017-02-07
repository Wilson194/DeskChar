import unittest
from data.database.Database import *


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = Database(':memory:')

        columns = [
            Column('ID', 'INTEGER', True),
            Column('Name', 'TEXT', False, True),
            Column('Age', 'INTEGER'),
            Column('Agility', 'INTEGER')
        ]

        cls.database.create_table('Character', columns)


    def test_insert(self):
        values = {
            'Name': 'Wilson',
            'Age': 25,
            'Agility': 50
        }
        self.database.insert('Character', values)

        values = {
            'Name': 'John',
            'Age': 26,
            'Agility': 40
        }
        self.database.insert('Character', values)

        data = self.database.select_all('Character')
        self.assertEqual(len(data), 2, 'Database insert fail')

        self.database.truncate_table('Character')


    def test_delete(self):
        values = {
            'Name': 'Wilson',
            'Age': 25,
            'Agility': 50
        }
        self.database.insert('Character', values)

        values = {
            'Name': 'John',
            'Age': 26,
            'Agility': 40
        }
        self.database.insert('Character', values)

        self.database.delete('Character', 1)
        data = self.database.select_all('Character')
        self.assertEqual(len(data), 1)

        self.database.truncate_table('Character')


    def test_select(self):
        values = {
            'Name': 'Wilson',
            'Age': 25,
            'Agility': 50
        }
        self.database.insert('Character', values)

        values = {
            'Name': 'John',
            'Age': 26,
            'Agility': 40
        }
        self.database.insert('Character', values)

        data = self.database.select('Character', {'Name': 'Wilson'})
        self.assertEqual(len(data), 1)

        self.database.truncate_table('Character')


    def test_foreign_key(self):
        columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('Name', 'TEXT', False, True),
            Column('Value', 'INTEGER'),
            Column('Target', 'INTEGER'),
        ]

        foreigns = [
            Foreign('Target', 'Character', 'ID')
        ]

        self.database.create_table('Translate', columns,foreigns)


    def test_invalid_column_type(self):
        with self.assertRaises(ValueError):
            Column('Jmeno', 'VARCHAR')

        with self.assertRaises(ValueError):
            Column('Jmeno', 'TEXTIK')


# if __name__ == '__main__':
#     unittest.main()