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
            Column('amount', 'INTEGER'),
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

        # ///////////// Ability context \\\\\\\\\\\\\\\\\\

        ability_context_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('value', 'INTEGER'),
            Column('valueType', 'INTEGER'),
            Column('targetAttribute', 'INTEGER'),
        ]

        try:
            database.create_table('AbilityContext', ability_context_columns)
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
            Column('characterTargetAttribute', 'INTEGER'),
            Column('itemTargetAttribute', 'INTEGER')

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

        # ///////////// Character \\\\\\\\\\\\\\\\\\

        character_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('age', 'INTEGER'),
            Column('agility', 'INTEGER'),
            Column('charisma', 'INTEGER'),
            Column('height', 'INTEGER'),
            Column('intelligence', 'INTEGER'),
            Column('level', 'INTEGER'),
            Column('mobility', 'INTEGER'),
            Column('strength', 'INTEGER'),
            Column('toughness', 'INTEGER'),
            Column('weight', 'INTEGER'),
            Column('xp', 'INTEGER'),
            Column('maxHealth', 'INTEGER'),
            Column('maxMana', 'INTEGER'),
            Column('drdRace', 'INTEGER'),
            Column('drdClass', 'INTEGER'),
            Column('alignment', 'INTEGER'),
            Column('currentMana', 'INTEGER'),
            Column('currentHealth', 'INTEGER'),

        ]

        try:
            database.create_table('Character', character_columns)
        except OperationalError:
            pass

        # ///////////// Party character \\\\\\\\\\\\\\\\\\

        party_character_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('deviceName', 'TEXT'),
            Column('MACAddress', 'TEXT'),
            Column('character_id', 'INTEGER')
        ]

        try:
            database.create_table('PartyCharacter', party_character_columns)
        except OperationalError:
            pass

        # ///////////// Monster \\\\\\\\\\\\\\\\\\

        monster_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('viability', 'INTEGER'),
            Column('defense', 'INTEGER'),
            Column('endurance', 'INTEGER'),
            Column('rampancy', 'INTEGER'),
            Column('mobility', 'INTEGER'),
            Column('perseverance', 'INTEGER'),
            Column('intelligence', 'INTEGER'),
            Column('charisma', 'INTEGER'),
            Column('alignment', 'INTEGER'),
            Column('experience', 'INTEGER'),
            Column('hp', 'INTEGER'),
            Column('monsterRace', 'INTEGER'),
            Column('size', 'INTEGER'),
        ]

        try:
            database.create_table('Monster', monster_columns)
        except OperationalError:
            pass

        # ///////////// Scenario \\\\\\\\\\\\\\\\\\

        scenario_columns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('date', 'INTEGER'),
        ]

        try:
            database.create_table('Scenario', scenario_columns)
        except OperationalError:
            pass

        # ///////////// Location \\\\\\\\\\\\\\\\\\

        location_columns = [
            Column('ID', 'INTEGER', True, False, True),

        ]

        try:
            database.create_table('Location', location_columns)
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

        # ///////////// Effect modifiers \\\\\\\\\\\\\\\\\\

        effectModifierColumns = [
            Column('effect_id', 'INTEGER', not_null=True),
            Column('modifier_id', 'INTEGER', not_null=True),
        ]

        effectModifierForeigns = [
            Foreign('effect_id', 'Effect', 'ID', 'CASCADE'),
            Foreign('modifier_id', 'Modifier', 'ID', 'CASCADE'),
        ]

        try:
            database.create_table('Effect_modifier', effectModifierColumns, effectModifierForeigns)
        except OperationalError:
            pass

        # ///////////// Ability context \\\\\\\\\\\\\\\\\\

        abilityContextColumns = [
            Column('ability_id', 'INTEGER', not_null=True),
            Column('context_id', 'INTEGER', not_null=True),
        ]

        abilityContextForeigns = [
            Foreign('ability_id', 'Ability', 'ID', 'CASCADE'),
            Foreign('context_id', 'AbilityContext', 'ID', 'CASCADE'),
        ]

        try:
            database.create_table('Ability_context', abilityContextColumns,
                                  abilityContextForeigns)
        except OperationalError:
            pass

        # ///////////// Items effects \\\\\\\\\\\\\\\\\\

        itemEffectColumns = [
            Column('effect_id', 'INTEGER', not_null=True),
            Column('item_id', 'INTEGER', not_null=True),
            Column('item_type', 'INTEGER', not_null=True),

        ]

        itemEffectForeigns = [
            Foreign('effect_id', 'Effect', 'ID', 'CASCADE'),
        ]

        try:
            database.create_table('Item_effect', itemEffectColumns, itemEffectForeigns)
        except OperationalError:
            pass

        # ///////////// MapItem \\\\\\\\\\\\\\\\\\\

        mapColumns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('name', 'TEXT'),
            Column('description', 'TEXT'),
            Column('map_file', 'TEXT'),
        ]

        try:
            database.create_table('Map', mapColumns)
        except OperationalError:
            pass

        # ///////////// MapItem \\\\\\\\\\\\\\\\\\\

        mapItemColumns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('name', 'TEXT'),
            Column('description', 'TEXT'),
            Column('positionX', 'REAL'),
            Column('positionY', 'REAL'),
            Column('scale', 'INTEGER'),
            Column('object_type', 'INTEGER'),
            Column('object_id', 'INTEGER'),
            Column('name', 'INTEGER'),
            Column('map_id', 'INTEGER')
        ]

        mapItemForeigns = [
            Foreign('map_id', 'Map', 'ID', 'CASCADE')
        ]

        try:
            database.create_table('Map_item', mapItemColumns, mapItemForeigns)
        except OperationalError:
            pass

        # ///////////// Settings \\\\\\\\\\\\\\\\\\

        settingsColumns = [
            Column('ID', 'INTEGER', True, False, True),
            Column('name', 'TEXT', not_null=True),
            Column('int_value', 'INTEGER'),
            Column('str_value', 'TEXT'),

        ]

        try:
            database.create_table('Settings', settingsColumns)
        except OperationalError:
            pass

        # ///////////// Initialize Languages \\\\\\\\\\\\\\\\\\
        data = database.select('languages', {'code': 'cs'})
        if len(data) == 0:
            database.insert('languages', {'name': 'Čeština', 'code': 'cs'})
            database.insert('languages', {'name': 'Angličtina', 'code': 'en'})
