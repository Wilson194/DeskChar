from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.ItemDAO import ItemDAO
from presentation.layouts.ItemLayout import ItemLayout
from structure.abilities.Ability import Ability
from structure.enums.ObjectType import ObjectType
from data.DAO.SpellDAO import SpellDAO
from presentation.layouts.SpellLayout import SpellLayout
from structure.items.Item import Item
from structure.spells.Spell import Spell
from presentation.layouts.AbilityLayout import AbilityLayout


class TabWidgetManager:
    """
    Manager for Tab widget
    """


    def __init__(self):
        pass


    def get_data(self, target_id: int, target_type: ObjectType) -> list:
        """
        Return list of objects, objects are for one ID but all langs
        :param target_id: id of object
        :param target_type: Type of object
        :return: List of object
        """
        data = []

        if target_type is ObjectType.SPELL:
            langs = SpellDAO().get_languages(target_id)
            for lang in langs:
                spell = SpellDAO().get_spell(target_id, lang)
                data.append(spell)

        elif target_type is ObjectType.ABILITY:
            langs = AbilityDAO().get_languages(target_id)
            for lang in langs:
                ability = AbilityDAO().get_ability(target_id, lang)
                data.append(ability)

        elif target_type is ObjectType.ITEM:
            langs = ItemDAO().get_languages(target_id)
            for lang in langs:
                item = ItemDAO().get_item(target_id, lang)
                data.append(item)

        return data


    def get_layout(self, target_type: ObjectType, parent):
        """
        Get layout for targget type
        :param target_type: Type of object
        :param parent: parent object for creating leyout
        :return: Layout for target object
        """
        if target_type is ObjectType.SPELL:
            return SpellLayout(parent)
        if target_type is ObjectType.ABILITY:
            return AbilityLayout(parent)
        if target_type is ObjectType.ITEM:
            return ItemLayout(parent)



    def get_empty_object(self, target_type: ObjectType, id: int, lang: str) -> object:
        """
        Create empty object for id and lang
        :param target_type: Type ob object
        :param id: id of object
        :param lang: lang code of object
        :return: New empty object
        """
        if target_type is ObjectType.SPELL:
            return Spell(id, lang)
        if target_type is ObjectType.ABILITY:
            return Ability(id, lang)
        if target_type is ObjectType.ITEM:
            return Item(id, lang)

        return None
