from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


class Effect(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, targetId: int = None,
                 targetType: ModifierTargetTypes = None):
        super().__init__(id, lang, name, description)

        self.__targetId = targetId
        self.__targetType = targetType

        self.__modifiers = []


    def __name__(self):
        names = super().__name__()
        names.append('Effect')
        return names


    @property
    def treeChildren(self):
        return [ObjectType.MODIFIER]


    @staticmethod
    def DAO():
        from data.DAO.EffectDAO import EffectDAO
        return EffectDAO


    @staticmethod
    def XmlClass():
        return None


    @staticmethod
    def layout():
        return None


    @property
    def children(self):
        return []


    @property
    def icon(self):
        return 'resources/icons/gemGreen.png'


    @property
    def object_type(self):
        return ObjectType.EFFECT


    @property
    def targetId(self):
        return self.__targetId


    @targetId.setter
    def targetId(self, value: int):
        self.__targetId = value


    @property
    def targetType(self):
        return self.__targetType


    @targetType.setter
    def targetType(self, value: str):
        self.__targetType = value


    @property
    def modifiers(self):
        return self.__modifiers


    @modifiers.setter
    def modifiers(self, value: list):
        self.__modifiers = value


    def add_modifier(self, modifier):
        self.__modifiers.append(modifier)


    def __eq__(self, other):
        if not isinstance(other, Effect):
            return False

        if super().__eq__(other) \
                and self.__targetId == other.targetId \
                and self.__targetType == other.targetType \
                and self.__modifiers == other.modifiers:
            return True

        return False
