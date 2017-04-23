from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.EffectDAO import EffectDAO
from data.DAO.ItemDAO import ItemDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SpellDAO import SpellDAO
from data.DAO.interface.ISpellDAO import ISpellDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.character.Character import Character
from structure.enums.Alignment import Alignment
from structure.enums.Classes import Classes
from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon
from structure.spells.Spell import Spell
from data.DAO.DAO import DAO
from structure.tree.NodeObject import NodeObject


class CharacterDAO(DAO, ISpellDAO):
    DATABASE_TABLE = 'Character'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.CHARACTER


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, character: Character, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new spell in database
        :param character: Character object
        :return: id of autoincrement
        """
        if contextType is None:
            contextType = self.TYPE

        intValues = {
            'agility'      : character.agility,
            'charisma'     : character.charisma,
            'intelligence' : character.intelligence,
            'mobility'     : character.mobility,
            'strength'     : character.strength,
            'toughness'    : character.toughness,
            'age'          : character.age,
            'height'       : character.height,
            'weight'       : character.weight,
            'level'        : character.level,
            'xp'           : character.xp,
            'maxHealth'    : character.maxHealth,
            'maxMana'      : character.maxMana,
            'currentHealth': character.currentHealth,
            'currentMana'  : character.currentMana,
            'drdClass'     : character.drdClass.value if character.drdClass else None,
            'drdRace'      : character.drdRace.value if character.drdRace else None,
            'alignment'    : character.alignment.value if character.alignment else None,
        }

        strValues = {
            'name'       : character.name,
            'description': character.description
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        character.id = id

        self.database.insert_translate(strValues, character.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, character.name, nodeParentId, character)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for spell in character.spells:
            SpellDAO().create(spell, nodeId, contextType)

        for ability in character.abilities:
            AbilityDAO().create(ability, nodeId, contextType)

        for effect in character.effects:
            EffectDAO().create(effect, nodeId, contextType)

        if character.inventory is None:
            c = Container(None, None, 'Inventory', None, -1)
            inventoryId = ItemDAO().create(c, nodeId, contextType)
        else:
            character.inventory.parent_id = -1
            inventoryId = ItemDAO().create(character.inventory, nodeId, contextType)

        if character.ground is None:
            c = Container(None, None, 'Ground', None, -2)
            groundId = ItemDAO().create(c, nodeId, contextType)
        else:
            character.ground.parent_id = -2
            groundId = ItemDAO().create(character.ground, nodeId, contextType)

        self.database.update(self.DATABASE_TABLE, id, {'inventoryId': inventoryId, 'groundId': groundId})

        return id


    def update(self, character: Character):
        """
        Update spell in database
        :param character: Character object with new data
        """
        intValues = {
            'agility'      : character.agility,
            'charisma'     : character.charisma,
            'intelligence' : character.intelligence,
            'mobility'     : character.mobility,
            'strength'     : character.strength,
            'toughness'    : character.toughness,
            'age'          : character.age,
            'height'       : character.height,
            'weight'       : character.weight,
            'level'        : character.level,
            'xp'           : character.xp,
            'maxHealth'    : character.maxHealth,
            'maxMana'      : character.maxMana,
            'currentHealth': character.currentHealth,
            'currentMana'  : character.currentMana,
            'drdClass'     : character.drdClass.value if character.drdClass else None,
            'drdRace'      : character.drdRace.value if character.drdRace else None,
            'alignment'    : character.alignment.value if character.alignment else None,
        }

        strValues = {
            'name'       : character.name,
            'description': character.description
        }

        self.database.update(self.DATABASE_TABLE, character.id, intValues)
        self.database.update_translate(strValues, character.lang, character.id, self.TYPE)


    def delete(self, character_id: int):
        """
        Delete spell from database and all his translates
        :param character_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, character_id)
        self.database.delete_where('translates',
                                   {'target_id': character_id, 'type': ObjectType.CHARACTER})


    def get(self, character_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Character:
        """
        Get spell from database
        :param character_id: id of spell
        :param lang: lang of spell
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': character_id})[0])
        tr_data = self.database.select_translate(character_id, ObjectType.CHARACTER.value,
                                                 lang)

        drdClass = Classes(data.get('drdClass')) if data.get('drdClass') is not None else None
        drdRace = Races(data.get('drdRace')) if data.get('drdRace') is not None else None
        alignment = Alignment(data.get('alignment')) if data.get('alignment') is not None else None

        character = Character(data.get('ID'), lang, tr_data.get('name', ''),
                              tr_data.get('description', ''), data.get('agility', 0),
                              data.get('charisma', 0), data.get('intelligence', 0),
                              data.get('mobility', 0), data.get('strength', 0),
                              data.get('toughness', 0), data.get('age', 0), data.get('height', 0),
                              data.get('weight', 0), data.get('level', 0), data.get('xp', 0),
                              data.get('maxHealth', 0), data.get('maxMana', 0), drdClass, drdRace,
                              alignment, data.get('currentHealth', 0), data.get('currentMana', 0))

        if nodeId and contextType:
            children = self.treeDAO.get_children_objects(nodeId, contextType)
            abilities = []
            spells = []
            effects = []

            for child in children:
                if child.object.object_type is ObjectType.SPELL:
                    spell = SpellDAO().get(child.object.id, None, child.id, contextType)
                    spells.append(spell)
                elif child.object.object_type is ObjectType.ABILITY:
                    ability = AbilityDAO().get(child.object.id, None, child.id, contextType)
                    abilities.append(ability)
                elif child.object.object_type is ObjectType.EFFECT:
                    effect = EffectDAO().get(child.object.id, None, child.id, contextType)
                    effects.append(effect)
                elif child.object.object_type is ObjectType.ITEM and child.object.type is Items.CONTAINER and child.object.parent_id == -1:
                    inventory = ItemDAO().get(child.object.id, None, child.id, contextType)
                    character.inventory = inventory
                elif child.object.object_type is ObjectType.ITEM and child.object.type is Items.CONTAINER and child.object.parent_id == -2:
                    ground = ItemDAO().get(child.object.id, None, child.id, contextType)
                    character.ground = ground

            character.spells = spells
            character.abilities = abilities
            character.effects = effects

        return character


    def get_all(self, lang=None) -> list:
        """
        Get list of all spells from database, only one lang
        :param lang: lang code
        :return: list of Spells
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        characters = []
        for line in lines:
            character = self.get(line['ID'], lang)
            characters.append(character)
        return characters
