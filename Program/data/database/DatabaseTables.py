from data.database.Database import Database, Column, Foreign
from sqlite3 import OperationalError


class DatabaseTables:
    """
    Class that create all tables in database
    """


    def create_tables(self):
        """
        Try to create all tables in database
        :return:
        """
        database = Database('test.db')  # TODO

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
            Column('target_id', 'INTEGER', not_null=True),
            Column('lang', 'TEXT'),
            Column('type', 'INTEGER', not_null=True),
            Column('name', 'TEXT', not_null=True),
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
            Column('type', 'INTEGER', not_null=True),
            Column('price', 'INTEGER'),
            Column('weight', 'INTEGER'),
            Column('capacity', 'INTEGER'),
            Column('quality', 'INTEGER'),
            Column('size', 'INTEGER'),
            Column('copper', 'INTEGER'),
            Column('silver', 'INTEGER'),
            Column('gold', 'INTEGER'),
            Column('weightA', 'INTEGER'),
            Column('weightB', 'INTEGER'),
            Column('weightC', 'INTEGER'),
            Column('strength', 'INTEGER'),
            Column('rampancy', 'INTEGER'),
            Column('length', 'INTEGER'),
            Column('defence', 'INTEGER'),
            Column('initiative', 'INTEGER'),
            Column('rangeLow', 'INTEGER'),
            Column('rangeMedium', 'INTEGER'),
            Column('rangeHigh', 'INTEGER'),
            Column('weaponWeight', 'INTEGER'),
            Column('handling', 'INTEGER'),
        ]

        try:
            database.create_table('Item', item_columns)
        except OperationalError:
            pass

        # ///////////// Ability \\\\\\\\\\\\\\\\\\

        ability_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('drd_race', 'INTEGER'),
            Column('drd_class', 'INTEGER'),

        ]

        try:
            database.create_table('Ability', ability_columns)
        except OperationalError:
            pass

        # ///////////// Spell \\\\\\\\\\\\\\\\\\

        spell_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('cast_time', 'INTEGER'),
            Column('drd_class', 'INTEGER')
        ]

        try:
            database.create_table('Spell', spell_columns)
        except OperationalError:
            pass

        # ///////////// Modifier \\\\\\\\\\\\\\\\\\

        modifier_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('value', 'INTEGER'),
            Column('valueType', 'INTEGER'),
            Column('targetType', 'INTEGER'),
            Column('valueTargetAttribute', 'INTEGER')
        ]

        try:
            database.create_table('Modifier', modifier_columns)
        except OperationalError:
            pass

        # ///////////// Effect \\\\\\\\\\\\\\\\\\

        modifier_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('targetType', 'INTEGER'),
        ]

        try:
            database.create_table('Effect', modifier_columns)
        except OperationalError:
            pass

        # ///////////// Effect_modificators \\\\\\\\\\\\\\\\\\

        columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('effect_id', 'INTEGER', not_null=True),
            Column('modifier_id', 'INTEGER', not_null=True),
        ]

        foreign = [
            Foreign('effect_id', 'Effect', 'ID'),
            Foreign('modifier_id', 'Modifier', 'ID')
        ]

        try:
            database.create_table('Effect_modifiers', columns, foreign)
        except OperationalError:
            pass

        # ///////////// Player tree structure \\\\\\\\\\\\\\\\\\

        structure_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('target_id', 'INTEGER'),
            Column('target_type', 'INTEGER'),
            Column('parent_id', 'INTEGER'),
            Column('parent_type', 'INTEGER', not_null=True),
            Column('type', 'INTEGER', not_null=True),
            Column('name', 'TEXT')
        ]

        structure_foreigns = [
            Foreign('parent_id', 'player_tree_structure', 'ID', 'CASCADE')
        ]

        try:
            database.create_table('player_tree_structure', structure_columns, structure_foreigns)
        except OperationalError:
            pass
