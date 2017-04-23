from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType


class XMLAbilityContext(XMLTemplate):
    ROOT_NAME = 'context'
    OBJECT_TYPE = ObjectType.ABILITY_CONTEXT


    def __init__(self):
        self.id = XElement('id')
        # self.name = XAttribElement('name', 'lang')
        # self.description = XAttribElement('description', 'lang')

        self.targetAttribute = XElement('attribute', CharacterAttributes)

        self.valueType = XElement('modifyType', ModifierValueTypes)
        self.value = XElement('value')
