from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


class Modifier(Object):
    TABLE_SCHEMA = [
        'id', 'value', 'valueType', 'targetType', 'characterTargetAttribute', 'itemTargetAttribute',
        'name', 'description'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 valueType: object = None, value: int = None,
                 characterTargetAttribute: CharacterAttributes = None,
                 itemTargetAttribute: ItemsAttributes = None,
                 targetType: ObjectType = None):
        super().__init__(id, lang, name, description)

        self.__targetType = targetType

        self.__characterTargetAttribute = characterTargetAttribute
        self.__itemTargetAttribute = itemTargetAttribute

        self.__valueType = valueType
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
        from data.xml.templates.XMLModifier import XMLModifier
        return XMLModifier


    @staticmethod
    def layout():
        from presentation.layouts.ModifierLayout import ModifierLayout
        return ModifierLayout


    @property
    def children(self):
        return []


    @property
    def icon(self):
        return 'resources/icons/potionGreen.png'


    @property
    def object_type(self):
        return ObjectType.MODIFIER


    @property
    def valueType(self):
        return self.__valueType


    @valueType.setter
    def valueType(self, value):
        self.__valueType = value


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value


    @property
    def characterTargetAttribute(self):
        return self.__characterTargetAttribute


    @characterTargetAttribute.setter
    def characterTargetAttribute(self, value):
        self.__characterTargetAttribute = value


    @property
    def itemTargetAttribute(self):
        return self.__itemTargetAttribute


    @itemTargetAttribute.setter
    def itemTargetAttribute(self, value):
        self.__itemTargetAttribute = value


    @property
    def targetType(self):
        return self.__targetType


    @targetType.setter
    def targetType(self, value):
        self.__targetType = value
