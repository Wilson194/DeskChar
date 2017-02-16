from Database import *
from sqlite3 import OperationalError


class DatabaseTables:
    def create_tables(self):
        database = Database('test.db')

        languages_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('name', 'TEXT', False, False, False, True),
            Column('code', 'TEXT', False, True, False, True),
        ]

        try:
            database.create_table('languages', languages_columns)
        except OperationalError:
            pass

        translate_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('target_id', 'INTEGER', False, False, False, True),
            Column('lang', 'TEXT'),
            Column('type', 'TEXT'),
            Column('name', 'TEXT'),
            Column('value', 'TEXT')
        ]

        translate_foreign = [
            Foreign('lang', 'languages', 'code')
        ]

        try:
            database.create_table('translates', translate_columns,
                                  translate_foreign)
        except OperationalError:
            pass

        item_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('parent_id', 'INTEGER'),
            Column('type', 'INTEGER', False, False, False, True),
            Column('price', 'INTEGER'),
            Column('weight', 'INTEGER'),
            Column('amount', 'INTEGER'),
            Column('capacity', 'INTEGER'),
            Column('quality', 'INTEGER'),
            Column('armor_size', 'INTEGER'),
            Column('copper', 'INTEGER'),
            Column('silver', 'INTEGER'),
            Column('gold', 'INTEGER')
        ]

        try:
            database.create_table('Item', item_columns)
        except OperationalError:
            pass

        ability_columns = [
            Column('ID', 'INTEGER', True, False, True),
        ]

        try:
            database.create_table('Ability', ability_columns)
        except OperationalError:
            pass

        spell_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('cast_time', 'INTEGER')
        ]

        try:
            database.create_table('Spell', spell_columns)
        except OperationalError:
            pass
