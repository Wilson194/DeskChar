from business.managers.LangManager import LangManager
from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.ItemDAO import ItemDAO
from data.database.ObjectDatabase import ObjectDatabase
from data.xml.ParserHandler import ParserHandler
from structure.abilities.Ability import Ability
from structure.items.Item import Item
from structure.tree.Object import Object
from structure.tree.Folder import Folder
from structure.enums.NodeType import NodeType
from structure.tree.Node import Node
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from structure.enums.ObjectType import ObjectType
from data.DAO.SpellDAO import SpellDAO
from structure.spells.Spell import Spell


class PlayerTreeManager:
    """
    Tree manager for tree widget
    """


    def __init__(self):
        self.treeDAO = PlayerTreeDAO()


    def get_tree(self, object_type: ObjectType) -> list:
        """
        Return list of root in tree, root has children ( recursive)
        :return: list of root
        """
        roots = self.treeDAO.get_root_nodes(object_type)

        for root in roots:
            self.__create_tree(root, object_type)

        return roots


    def __create_tree(self, node: Node, type: ObjectType):
        """
        Recursive function for create tree with children
        :param node: Current node
        :param type: parent of node
        """
        children = self.treeDAO.get_children_nodes(type, node.id)
        for child in children:
            self.__create_tree(child, type)
        node.children = children


    def create_node(self, node_type: NodeType, name: str, parent_id: int = None,
                    object_type: ObjectType = None):
        """
        Create new node
        :param node_type: Node type
        :param name:  name of node
        :param parent_id: parent id
        :param object_type: Type of object
        :return: New node object
        """
        if node_type.value is NodeType.FOLDER.value:
            node = Folder(None, name, parent_id)
        else:
            obj = self.create_empty_object(object_type)
            node = Object(None, name, parent_id, obj)
        id = self.treeDAO.insert_node(node, object_type)
        node.id = id
        return node


    def delete_node(self, id):
        """
        Delete node
        :param id: id of node
        """
        self.treeDAO.delete_node(id)


    def get_node(self, id: int):
        """
        Get node by ID
        :param id: id of node
        :return: Node
        """
        return self.treeDAO.get_node(id)


    def update_node(self, node):
        """
        Update node in database
        :param node: Updated node
        """
        self.treeDAO.update_node(node)


    def update_node_parent(self, node_id, parent_id):
        """
        Update parent of node, check if parent is Folder
        :param node_id: id of node
        :param parent_id: parent id
        :return:
        """
        node = self.treeDAO.get_node(node_id)
        if not parent_id:
            if node.parent_id != parent_id:
                node.parent_id = parent_id
                self.treeDAO.update_node(node)
        else:
            parent_node = self.treeDAO.get_node(parent_id)
            if node.parent_id != parent_id and isinstance(parent_node, Folder):
                node.parent_id = parent_id
                self.treeDAO.update_node(node)


    def create_empty_object(self, object_type: ObjectType) -> Object:
        """
        Create empty object
        :param object_type: obkect type
        :return: Object if created, None otherwise
        """
        if object_type.value is ObjectType.SPELL.value:
            obj = Spell()
            spell_id = SpellDAO().create_spell(obj)
            obj.id = spell_id
        elif object_type.value is ObjectType.ABILITY.value:
            obj = Ability()
            ability_id = AbilityDAO().create_ability(obj)
            obj.id = ability_id
        elif object_type.value is ObjectType.ITEM.value:
            obj = Item()
            item_id = ItemDAO().create_item(obj)
            obj.id = item_id
        else:
            obj = None

        return obj


    def get_object(self, node_id: int):
        """
        Get node by id
        :param node_id: id of node
        :return: Node if exist, None otherwise
        """
        node = self.treeDAO.get_node(node_id)
        return node.object


    def export_to_xml(self, selected: list, path: str):
        """
        Export selected templates to xml
        :param selected: list of selected node in tree
        :param path: path to file, where will be final file
        """
        exporting = []
        for id in selected:
            node = self.treeDAO.get_node(id)
            exporting.append((ObjectType.SPELL, node.object.id))  # TODO: change default SPELL

        ParserHandler().create_xml(exporting, path)


    def import_from_xml(self, file_path, type, parent=None):
        """
        Import templates from XML file
        :param file_path: path to XML file
        :param type:
        :param parent: parent node id
        """
        objects = ParserHandler().import_xml(file_path)
        ObjectDatabase('test.db').set_many(True)

        if not LangManager().lang_exists('cs'):  # TODO : default lang
            LangManager().create_lang('Čeština', 'cs')

        for object in objects:
            default = object.pop('cs')  # TODO: default lang
            default_id = ObjectDatabase('test.db').insert_object(default)
            default.id = default_id
            for lang in object.values():
                if not LangManager().lang_exists(lang.lang):  # TODO : default lang
                    LangManager().create_lang(lang.lang, lang.lang)
                lang.id = default_id
                ObjectDatabase('test.db').update_object(lang)

            node = Object(None, default.name, parent, default)
            self.treeDAO.insert_node(node, ObjectType.SPELL) # TODO: chance default SPELL

        ObjectDatabase('test.db').insert_many_execute()
        ObjectDatabase('test.db').set_many(False)
