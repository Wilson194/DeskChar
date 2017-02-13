from Database import *


class DatabaseTables:
    def create_tables(self):
        database = Database(':memory:')

        languages_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('name', 'TEXT', False, False, False, True),
            Column('code', 'TEXT', False, True, False, True),
        ]

        database.create_table('languages', languages_columns)

        translate_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('target_id', 'INTEGER', False, False, False, True),
            Column('language_code', 'TEXT'),
            Column('type', 'TEXT'),
            Column('name', 'TEXT'),
            Column('value', 'TEXT')
        ]

        translate_foreign = [
            Foreign('language_code', 'languages', 'code')
        ]

        database.create_table('translates', translate_columns,
                              translate_foreign)

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

        database.create_table('Item', item_columns)
