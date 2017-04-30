from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.ISpellDAO import ISpellDAO
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from structure.spells.Spell import Spell
from data.DAO.DAO import DAO
from structure.tree.NodeObject import NodeObject


class SpellDAO(DAO, ISpellDAO):
    DATABASE_TABLE = 'Spell'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.SPELL


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, spell: Spell, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Spell
        :param spell: Spell object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created Spell
        """

        if not contextType:
            contextType = self.TYPE

        intValues = {
            'cast_time': spell.cast_time if spell.cast_time else 0,
            'drd_class': spell.drd_class.value if spell.drd_class else None
        }

        strValues = {
            'name'               : spell.name,
            'description'        : spell.description,
            'mana_cost_initial'  : spell.mana_cost_initial,
            'mana_cost_continual': spell.mana_cost_continual,
            'range'              : spell.range,
            'scope'              : spell.scope,
            'duration'           : spell.duration
        }

        # Insert NON transable values
        id = self.database.insert(self.DATABASE_TABLE, intValues)

        # Insert transable values
        self.database.insert_translate(strValues, spell.lang, id, self.TYPE)

        spell.id = id

        # Create node for tree structure
        node = NodeObject(None, spell.name, nodeParentId, spell)
        self.treeDAO.insert_node(node, contextType)

        return id


    def update(self, spell: Spell):
        """
        Update spell in database
        :param spell: Spell object with new data
        """
        if spell.id is None:
            raise ValueError('Cant update object without ID')
        data = self.database.select(self.DATABASE_TABLE, {'ID': spell.id})

        if not data:
            raise ValueError('Cant update none existing object')

        intValues = {
            'cast_time': spell.cast_time,
            'drd_class': spell.drd_class.value if spell.drd_class else None
        }

        self.database.update(self.DATABASE_TABLE, spell.id, intValues)

        strValues = {
            'name'               : spell.name,
            'description'        : spell.description,
            'mana_cost_initial'  : spell.mana_cost_initial,
            'mana_cost_continual': spell.mana_cost_continual,
            'range'              : spell.range,
            'scope'              : spell.scope,
            'duration'           : spell.duration
        }

        self.database.update_translate(strValues, spell.lang, spell.id, self.TYPE)


    def delete(self, spell_id: int):
        """
        Delete spell from database and all his translates
        :param spell_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, spell_id)
        self.database.delete_where('translates',
                                   {'target_id': spell_id, 'type': ObjectType.SPELL})


    def get(self, spell_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Spell:
        """
        Get Spell , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param spell_id: id of Spell
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Spell object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'

        data = self.database.select(self.DATABASE_TABLE, {'ID': spell_id})
        if not data:
            return None
        else:
            data = dict(data[0])
        tr_data = self.database.select_translate(spell_id, ObjectType.SPELL.value,
                                                 lang)
        drdClassIndex = data.get('drd_class', None)
        drdClass = Classes(drdClassIndex) if drdClassIndex is not None else None
        spell = Spell(spell_id, lang, tr_data.get('name', ''),
                      tr_data.get('description', ''), tr_data.get('mana_cost_initial', ''),
                      tr_data.get('mana_cost_continual', ''), tr_data.get('range', ''),
                      tr_data.get('scope', ''), data.get('cast_time', 0),
                      tr_data.get('duration', ''), drdClass)

        return spell


    def get_all(self, lang=None) -> list:
        """
        Get list of Spell for selected lang
        :param lang: lang of Spell
        :return: list of Spell
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
