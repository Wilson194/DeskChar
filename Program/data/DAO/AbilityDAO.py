from data.DAO.AbilityContextDAO import AbilityContextDAO
from data.DAO.DAO import DAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SettingsDAO import SettingsDAO
from data.DAO.interface.IAbilityDAO import IAbilityDAO
from data.database.ObjectDatabase import ObjectDatabase
from structure.abilities.Ability import Ability
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.tree.NodeObject import NodeObject


class AbilityDAO(DAO, IAbilityDAO):
    DATABASE_TABLE = 'Ability'
    TYPE = ObjectType.ABILITY


    def __init__(self, databaseDriver: str = None):
        self.database = ObjectDatabase(databaseDriver if databaseDriver else self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, ability: Ability, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new ability
        :param ability: Ability object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created ability
        """

        if not contextType:
            contextType = self.TYPE

        intValues = {
            'drd_race' : ability.drd_race.value if ability.drd_race else None,
            'drd_class': ability.drd_class.value if ability.drd_class else None,
            'level'    : ability.level
        }

        strValues = {
            'name'       : ability.name,
            'description': ability.description,
            'chance'     : ability.chance
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        ability.id = id

        self.database.insert_translate(strValues, ability.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, ability.name, nodeParentId, ability)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for context in ability.contexts:
            AbilityContextDAO().create(context, nodeId, contextType)

        return id


    def update(self, ability: Ability):
        """
        Update ability in database
        :param ability: Ability object with new data
        """
        intValues = {
            'drd_race' : ability.drd_race.value if ability.drd_race else None,
            'drd_class': ability.drd_class.value if ability.drd_class else None,
            'level'    : ability.level
        }

        strValues = {
            'name'       : ability.name,
            'description': ability.description,
            'chance'     : ability.chance
        }

        self.database.update(self.DATABASE_TABLE, ability.id, intValues)
        self.database.update_translate(strValues, ability.lang, ability.id, self.TYPE)


    def delete(self, ability_id: int):
        """
        Delete ability from database and from translate
        :param ability_id: id of ability
        """

        self.database.delete(self.DATABASE_TABLE, ability_id)
        self.database.delete_where('translates',
                                   {'target_id': ability_id, 'type': ObjectType.ABILITY})


    def get(self, ability_id: int, lang=None, nodeId: int = None, contextType: ObjectType = None) -> Ability:
        """
        Get ability , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param ability_id: id of ability
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Ability object
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)

        data = self.database.select(self.DATABASE_TABLE, {'ID': ability_id})
        if not data:
            return None
        else:
            data = dict(data[0])

        tr_data = self.database.select_translate(ability_id, ObjectType.ABILITY.value, lang)

        drd_class = Classes(data.get('drd_class')) if data.get('drd_class') is not None else None
        drd_race = Races(data.get('drd_race')) if data.get('drd_race') is not None else None
        ability = Ability(ability_id, lang, tr_data.get('name', ''),
                          tr_data.get('description', ''), tr_data.get('chance', ''),
                          drd_race, drd_class, data.get('level', 1))

        if nodeId and contextType:
            children = self.treeDAO.get_children_objects(nodeId, contextType)

            contexts = []
            for child in children:
                if child.object.object_type is ObjectType.ABILITY_CONTEXT:
                    contexts.append(AbilityContextDAO().get(child.object.id, None, child.id, contextType))
            ability.contexts = contexts

        return ability


    def get_all(self, lang=None) -> list:
        """
        Get list of abilities for selected lang
        :param lang: lang of abilities
        :return: list of abilities
        """
        if lang is None:
            lang = SettingsDAO().get_value('language', str)
        lines = self.database.select_all(self.DATABASE_TABLE)

        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
