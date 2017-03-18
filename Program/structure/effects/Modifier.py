from structure.effects.Effect import Effect
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


class Modifier(Object):
    TABLE_SCHEMA = [
        'id', 'value', 'value_type', 'value_type_target', 'value_attribute_target'
    ]


    def __init__(self, lang: str, name: str, description: str, id: int = None,
                 parent_effect: Effect = None, target_type: ObjectType = None,
                 target_id: int = None, value_type: ModifierValueTypes = None,
                 value_target: int = None, value: int = None):
        super().__init__(id, lang, name, description)
        self.__parent_effect = parent_effect
        self.__target_type = target_type
        self.__target_id = target_id
        self.__value_type = value_type
        self.__value_target = value_target
        self.__value = value


    def __name__(self):
        names = super().__name__()
        names.append('Modifier')
        return names


    @staticmethod
    def DAO():
        from data.DAO.ModifierDAO import ModifierDAO
        return ModifierDAO


    @staticmethod
    def XmlClass():
        return None


    @staticmethod
    def layout():
        from presentation.layouts.ModifierLayout import ModifierLayout
        return ModifierLayout


    @property
    def children(self):
        return []


    @property
    def icon(self):
        return 'resources/icons/book.png'


    @property
    def object_type(self):
        return ObjectType.SPELL


    @property
    def parent_effect(self):
        return self.__parent_effect


    @parent_effect.setter
    def parent_effect(self, value):
        self.__parent_effect = value


    @property
    def target_type(self):
        return self.__target_type


    @target_type.setter
    def target_type(self, value):
        self.__target_type = value


    @property
    def target_id(self):
        return self.__target_id


    @target_id.setter
    def target_id(self, value):
        self.__target_id = value


    @property
    def value_type(self):
        return self.__value_type


    @value_type.setter
    def value_type(self, value):
        self.__value_type = value


    @property
    def value_target(self):
        return self.__value_target


    @value_target.setter
    def value_target(self, value):
        self.__value_target = value


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value
