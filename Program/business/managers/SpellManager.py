from business.managers.interface.ISpellManager import ISpellManager
from structure.enums.ObjectType import ObjectType
from structure.spells.Spell import Spell


class SpellManager(ISpellManager):
    def __init__(self):
        from data.DAO.SpellDAO import SpellDAO
        self.DAO = SpellDAO()


    def create(self, spell: Spell, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(spell, nodeParentId, contextType)


    def update_spell(self, spell: Spell):
        return self.DAO.update(spell)


    def delete(self, spellId: int):
        return self.DAO.delete(spellId)


    def get(self, spellId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Spell:
        return self.DAO.get(spellId, lang, nodeId, contextType)


    def get_all(self, lang=None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang):
        spell = Spell(None, lang)
        id = self.DAO.create(spell)
        spell.id = id

        return spell
