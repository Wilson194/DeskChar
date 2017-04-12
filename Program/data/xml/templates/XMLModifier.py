from data.xml.templates.XMLTemplate import XMLTemplate, XElement, XAttribElement, XInstance
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.ObjectType import ObjectType


class XMLModifier(XMLTemplate):
    ROOT_NAME = 'modifier'
    OBJECT_TYPE = ObjectType.MODIFIER


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')

        self.targetType = XElement('targetType', ModifierTargetTypes)

        self.characterTargetAttribute = XElement('characterAttribute', CharacterAttributes)
        self.itemTargetAttribute = XElement('itemAttribute', ItemsAttributes)

        self.valueType = XElement('valueType', ModifierValueTypes)
        self.value = XElement('value')
