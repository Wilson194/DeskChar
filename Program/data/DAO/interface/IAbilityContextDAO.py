from abc import ABC, abstractmethod

from structure.effects.AbilityContext import AbilityContext
from structure.enums.ObjectType import ObjectType


class IAbilityContextDAO(ABC):
    @abstractmethod
    def create(self, context: AbilityContext, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new ability context
        :param context: Ability context object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created ability context
        """
        pass


    @abstractmethod
    def update(self, context: AbilityContext) -> None:
        """
        Update Ability context with new values
        :param context: Ability context object with new values    
        """
        pass


    @abstractmethod
    def delete(self, context_id: int) -> None:
        """
        Delete ability context from database
        :param context_id: id of context 
        :return: 
        """
        pass


    @abstractmethod
    def get(self, context_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> AbilityContext:
        """
        Get ability context, object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all subobjects)
        If not specified, only basic attributes are set.        
        :param context_id: id of ability context
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Ability context object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None) -> list:
        """
        Gel list of all Ability context
        :param lang: lang of objects
        :return: list of Ability context
        """
        pass
