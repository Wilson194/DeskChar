from abc import ABC, abstractmethod
from structure.effects.Effect import Effect
from structure.enums.ObjectType import ObjectType


class IEffectDAO(ABC):
    @abstractmethod
    def create(self, effect: Effect, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new effect
        :param effect: Effect object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created effect
        """
        pass


    @abstractmethod
    def update(self, effect: Effect) -> None:
        """
        Update effect in database
        :param effect: Effect object with new data
        """
        pass


    @abstractmethod
    def delete(self, effect_id: int) -> None:
        """
        Delete Effect from database and from translate
        :param effect_id: id of effect
        """
        pass


    @abstractmethod
    def get(self, effect_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Effect:
        """
        Get Effect , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        :param effect_id: id of Effect
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Effect object
        """
        pass


    @abstractmethod
    def get_all(self, lang: str = None) -> list:
        """
        Get list of effects for selected lang
        :param lang: lang of effects
        :return: list of effects
        """
        pass
