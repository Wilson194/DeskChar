from Database import *
from sqlite3 import OperationalError


class DatabaseTables:
    def create_tables(self):
        database = Database('test.db')

        # ///////////// Languages \\\\\\\\\\\\\\\\\\

        languages_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('name', 'TEXT', False, False, False, True),
            Column('code', 'TEXT', False, True, False, True),
        ]

        try:
            database.create_table('languages', languages_columns)
        except OperationalError:
            pass

        # ///////////// Translate \\\\\\\\\\\\\\\\\\

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

        # ///////////// Items \\\\\\\\\\\\\\\\\\

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

        # ///////////// Ability \\\\\\\\\\\\\\\\\\

        ability_columns = [
            Column('ID', 'INTEGER', True, False, True),
        ]

        try:
            database.create_table('Ability', ability_columns)
        except OperationalError:
            pass

        # ///////////// Spell \\\\\\\\\\\\\\\\\\

        spell_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('cast_time', 'INTEGER')
        ]

        try:
            database.create_table('Spell', spell_columns)
        except OperationalError:
            pass

        # ///////////// Player tree structure \\\\\\\\\\\\\\\\\\

        structure_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('target_id', 'INTEGER'),
            Column('target_type', 'INTEGER'),
            Column('parent_id', 'INTEGER'),
            Column('type', 'INTEGER', False, False, False, True),
            Column('name', 'TEXT')
        ]

        structure_foreigns = [
            Foreign('parent_id','player_tree_structure', 'ID', 'CASCADE')
        ]

        try:
            database.create_table('player_tree_structure', structure_columns, structure_foreigns)
        except OperationalError:
            pass
