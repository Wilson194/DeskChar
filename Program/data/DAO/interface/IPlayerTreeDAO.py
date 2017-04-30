from abc import ABC, abstractmethod

from structure.character.PartyCharacter import PartyCharacter
from structure.effects.Modifier import Modifier
from structure.enums.ObjectType import ObjectType
from structure.monster.Monster import Monster
from structure.spells.Spell import Spell
from structure.tree.Node import Node


class IPlayerTreeDAO(ABC):
    @abstractmethod
    def get_root_nodes(self, target_type: ObjectType) -> list:
        """
        Get all nodes with parent null
        :param target_type: Type of object
        :return: list of root nodes
        """
        pass


    @abstractmethod
    def get_nodes_search(self, targetType: ObjectType, text: str):
        """
        Get nodes witch name contain searched text
        :param targetType: Type of object in node
        :param text: searching text
        :return: list of nodes with text included
        """
        pass


    @abstractmethod
    def get_node(self, id: int) -> Node:
        """
        Get node by id
        :param id: id of node
        :return: node object if exist, None otherwise
        """
        pass


    @abstractmethod
    def get_children_objects(self, parentNodeId: int, contextType: ObjectType) -> list:
        """
        Recursively find all child object of give type, only first level object (folders will be skipped and searching deep
        :param parentNodeId parent node, where you finding
        :param contextType object type of tree
        :return: list of objects in tree
        """
        pass


    @abstractmethod
    def get_children_nodes(self, contextType: ObjectType, parent_id: int) -> list:
        """
        Get all child of parent id
        :param target_type: target type
        :param parent_id: parent id
        :return: list of nodes with parent id, or empty list
        """
        pass


    @abstractmethod
    def update_node(self, node: Node) -> None:
        """
        Update node data
        :param node: node
        """
        pass


    @abstractmethod
    def insert_node(self, node: Node, object_type: ObjectType) -> int:
        """
        Create new node in database
        :param node: node object
        :return: id of created node
        """
        pass


    @abstractmethod
    def delete_node(self, id: int):
        """
        Delete node from database
        :param id: id of node
        """
        pass


    @abstractmethod
    def get_node_by_object(self, object: object):
        """
        Return node based on object
        :param object: object that you finding
        :return: ObjectNode with object 
        """
        pass
