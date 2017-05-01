import unittest
from data.database.Database import *
from data.database.ObjectDatabase import ObjectDatabase


class TestDatabase(unittest.TestCase):
    """
    Testing basic operations with database
    """


    @classmethod
    def setUpClass(cls):
        cls.database = ObjectDatabase(':memory:')
        cls.database.drop_table('Character')
        cls.database.drop_table('Translate')

        columns = [
            Column('ID', 'INTEGER', True),
            Column('Name', 'TEXT', False, True),
            Column('Age', 'INTEGER'),
            Column('Agility', 'INTEGER')
        ]

        cls.database.create_table('Character', columns)


    @classmethod
    def tearDownClass(cls):
        database = Database('unitTests.db')
        ObjectDatabase(':memory:').drop_table('Character')


    def test_insert(self):
        """
        Test insert to database
        :return: 
        """
        values = {
            'Name'   : 'Wilson',
            'Age'    : 25,
            'Agility': 50
        }
        self.database.insert('Character', values)

        values = {
            'Name'   : 'John',
            'Age'    : 26,
            'Agility': 40
        }
        self.database.insert('Character', values)

        data = self.database.select_all('Character')
        self.assertEqual(len(data), 2, 'Database insert fail')

        self.database.truncate_table('Character')


    def test_delete(self):
        """
        Test delete data from database
        :return: 
        """
        values = {
            'Name'   : 'Wilson',
            'Age'    : 25,
            'Agility': 50
        }
        self.database.insert('Character', values)

        values = {
            'Name'   : 'John',
            'Age'    : 26,
            'Agility': 40
        }
        self.database.insert('Character', values)

        self.database.delete('Character', 1)
        data = self.database.select_all('Character')
        self.assertEqual(len(data), 1)

        self.database.truncate_table('Character')


    def test_select(self):
        """
        Test select data from database
        :return: 
        """
        values = {
            'Name'   : 'Wilson',
            'Age'    : 25,
            'Agility': 50
        }
        self.database.insert('Character', values)

        values = {
            'Name'   : 'John',
            'Age'    : 26,
            'Agility': 40
        }
        self.database.insert('Character', values)

        data = self.database.select('Character', {'Name': 'Wilson'})
        self.assertEqual(len(data), 1)

        self.database.truncate_table('Character')


    def test_foreign_key(self):
        """
        Test foreign key in database
        :return: 
        """
        columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('Name', 'TEXT', False, True),
            Column('Value', 'INTEGER'),
            Column('Target', 'INTEGER'),
        ]

        foreigns = [
            Foreign('Target', 'Character', 'ID')
        ]

        self.database.create_table('Translate', columns, foreigns)


    def test_invalid_column_type(self):
        """
        Test creating invalid Column in database
        :return: 
        """
        with self.assertRaises(ValueError):
            Column('Jmeno', 'VARCHAR')

        with self.assertRaises(ValueError):
            Column('Jmeno', 'TEXTIK')


# if __name__ == '__main__':
#     unittest.main()
