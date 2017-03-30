from data.DAO.ModifierDAO import ModifierDAO
from data.DAO.SpellDAO import SpellDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Classes import Classes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.spells.Spell import Spell


class XMLModifier(XMLTemplate):
    ROOT_NAME = 'modifier'


    def __init__(self):
        self.DAO = ModifierDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        for lang in langs:

            targetType = self.get_value(root, 'targetType', None, False)
            targetTypeEnum = ModifierTargetTypes.by_name(ModifierTargetTypes, targetType)

            if targetTypeEnum is ModifierTargetTypes.CHARACTER:
                targetAttribute = self.get_value(root, 'characterAttribute', None, False)
                targetAttributeEnum = CharacterAttributes.by_name(CharacterAttributes,
                                                                  targetAttribute)
            else:
                targetAttribute = self.get_value(root, 'itemAttribute', None, False)
                targetAttributeEnum = ItemsAttributes.by_name(ItemsAttributes,
                                                                  targetAttribute)

            if targetAttributeEnum is ItemsAttributes.WEAPON_MELEE_HANDLING:
                pass
            elif targetAttributeEnum is ItemsAttributes.WEAPON_WEIGHT:
                pass
            else:
                valueType = self.get_value(root, 'valueType', None, False)
                valueTypeEnum = ModifierValueTypes.by_name(ModifierValueTypes, valueType)
                value = self.get_value(root,'value')

            data[lang] = obj

        return data


    def remap_names(self, name: str) -> str:
        if name == 'mana_cost_initial':
            return 'manaInitial'
        if name == 'mana_cost_continual':
            return 'manaContinual'
        if name == 'drd_class':
            return 'class'
        if name == 'ID':
            return 'id'
        if name == 'cast_time':
            return 'castTime'
        return name
