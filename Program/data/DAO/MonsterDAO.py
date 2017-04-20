from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.ItemDAO import ItemDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SpellDAO import SpellDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.Alignment import Alignment
from structure.enums.MonsterRace import MonsterRace
from structure.enums.ObjectType import ObjectType
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon
from structure.monster.Monster import Monster

from data.DAO.DAO import DAO
from structure.tree.NodeObject import NodeObject


class MonsterDAO(DAO):
    DATABASE_TABLE = 'Monster'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.MONSTER


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, monster: Monster, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new spell in database
        :param monster: Spell object
        :return: id of autoincrement
        """

        if not contextType:
            contextType = self.TYPE

        intValues = {
            'viability'   : monster.viability,
            'defense'     : monster.defense,
            'endurance'   : monster.endurance,
            'rampancy'    : monster.rampancy,
            'mobility'    : monster.mobility,
            'perseverance': monster.perseverance,
            'intelligence': monster.intelligence,
            'charisma'    : monster.charisma,
            'experience'  : monster.experience,
            'hp'          : monster.hp,
            'alignment'   : monster.alignment.value if monster.alignment else None,
            'monsterRace' : monster.monsterRace.value if monster.monsterRace else None,
            'size'        : monster.size.value if monster.size else None,
        }

        strValues = {
            'name'       : monster.name,
            'description': monster.description,
            'offense'    : monster.offense,
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        monster.id = id

        self.database.insert_translate(strValues, monster.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, monster.name, nodeParentId, monster)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for one in monster.containers + monster.armors + monster.moneyList + monster.meleeWeapons + monster.rangedWeapons + monster.throwableWeapons + monster.items:
            ItemDAO().create(one, nodeId, contextType)

        for spell in monster.spells:
            SpellDAO().create(spell, nodeId, contextType)

        for ability in monster.abilities:
            AbilityDAO().create(ability, nodeId, contextType)

        return id


    def update(self, monster: Monster):
        """
        Update spell in database
        :param spell: Spell object with new data
        """
        intValues = {
            'viability'   : monster.viability,
            'defense'     : monster.defense,
            'endurance'   : monster.endurance,
            'rampancy'    : monster.rampancy,
            'mobility'    : monster.mobility,
            'perseverance': monster.perseverance,
            'intelligence': monster.intelligence,
            'charisma'    : monster.charisma,
            'experience'  : monster.experience,
            'hp'          : monster.hp,
            'alignment'   : monster.alignment.value if monster.alignment else None,
            'monsterRace' : monster.monsterRace.value if monster.monsterRace else None,
            'size'        : monster.size.value if monster.size else None,
        }

        strValues = {
            'name'       : monster.name,
            'description': monster.description,
            'offense'    : monster.offense,
        }

        self.database.update(self.DATABASE_TABLE, monster.id, intValues)

        self.database.update_translate(strValues, monster.lang, monster.id, self.TYPE)


    def delete(self, monster_id: int):
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, monster_id)
        self.database.delete_where('translates',
                                   {'target_id': monster_id, 'type': ObjectType.SPELL})


    def get(self, monster_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Monster:
        """
        Get spell from database
        :param monster_id: id of spell
        :param lang: lang of spell
        :return: Monster object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': monster_id})[0])
        tr_data = self.database.select_translate(monster_id, ObjectType.MONSTER.value,
                                                 lang)

        monsterRace = MonsterRace(data['monsterRace']) if data['monsterRace'] else None
        monsterSize = MonsterRace(data['size']) if data['size'] else None
        alignment = Alignment(data['alignment']) if data['alignment'] else None
        monster = Monster(data['ID'], lang, tr_data.get('name', ''), tr_data.get('description', ''),
                          data.get('viability', 0), tr_data.get('offense', ''),
                          data.get('defense', 0),
                          data.get('endurance', 0), data.get('rampancy', 0),
                          data.get('mobility', 0), data.get('perseverance', 0),
                          data.get('intelligence', 0), data.get('charisma', 0),
                          alignment, data.get('experience', 0), data.get('hp', 0),
                          monsterRace, monsterSize)

        if nodeId and contextType:
            children = self.treeDAO.get_children_objects(nodeId, contextType)
            abilities = []
            spells = []
            items = []
            armors = []
            moneys = []
            containers = []
            meleeWeapons = []
            rangedWeapons = []
            throwableWeapons = []

            for child in children:
                if child.object.object_type is ObjectType.SPELL:
                    spell = SpellDAO().get(child.object.id, None, child.id, contextType)
                    spells.append(spell)
                elif child.object.object_type is ObjectType.ABILITY:
                    ability = AbilityDAO().get(child.object.id, None, child.id, contextType)
                    abilities.append(ability)
                elif child.object.object_type is ObjectType.ITEM:
                    childItem = ItemDAO().get(child.object.id, None, child.id, contextType)
                    if isinstance(childItem, Armor):
                        armors.append(childItem)
                    elif isinstance(childItem, Container):
                        containers.append(childItem)
                    elif isinstance(childItem, Money):
                        moneys.append(childItem)
                    elif isinstance(childItem, MeleeWeapon):
                        meleeWeapons.append(childItem)
                    elif isinstance(childItem, RangeWeapon):
                        rangedWeapons.append(childItem)
                    elif isinstance(childItem, ThrowableWeapon):
                        throwableWeapons.append(childItem)
                    else:
                        items.append(childItem)

            monster.abilities = abilities
            monster.spells = spells
            monster.items = items
            monster.armors = armors
            monster.moneyList = moneys
            monster.containers = containers
            monster.meleeWeapons = meleeWeapons
            monster.rangedWeapons = rangedWeapons
            monster.throwableWeapons = throwableWeapons

        return monster


    def get_all(self, lang=None) -> list:
        """
        Get list of all spells from database, only one lang
        :param lang: lang code
        :return: list of Spells
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
