from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object


class AbilityContext(Object):
    TABLE_SCHEMA = [
        'id', 'value', 'valueType', 'targetAttribute', 'name', 'description'
    ]


    def __init__(self, id: int = None, lang: str = None, name: str = None, description: str = None,
                 valueType: ModifierValueTypes = None, value: int = None,
                 targetAttribute: CharacterAttributes = None):
        super().__init__(id, lang, name, description)

        self.__targetAttribute = targetAttribute

        self.__valueType = valueType
        self.__value = value


    def __name__(self):
        names = super().__name__()
        names.append('AbilityContext')
        return names


    @staticmethod
    def DAO():
        from data.DAO.AbilityContextDAO import AbilityContextDAO
        return AbilityContextDAO


    @staticmethod
    def XmlClass():
        from data.xml.templates.XMLAbilityContext import XMLAbilityContext
        return XMLAbilityContext


    @staticmethod
    def layout():
        from presentation.layouts.AbilityContextLayout import AbilityContextLayout
        return AbilityContextLayout


    @property
    def children(self):
        return []


    @property
    def icon(self):
        return 'resources/icons/gemRed.png'


    @property
    def object_type(self):
        return ObjectType.ABILITY_CONTEXT


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
    def targetAttribute(self):
        return self.__targetAttribute


    @targetAttribute.setter
    def targetAttribute(self, value):
        self.__targetAttribute = value


    def printer(self, depth):
        print('{} Context - {}'.format('  ' * depth, self.name))


    def __eq__(self, other):
        if isinstance(other, AbilityContext):
            if self.value == other.value and self.valueType is other.valueType and self.targetAttribute is other.targetAttribute:
                return True
        return False
