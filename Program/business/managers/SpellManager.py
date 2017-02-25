from data.DAO.SpellDAO import SpellDAO
from structure.spells.Spell import Spell


class SpellManager:
    def __init__(self):
        self.DAO = SpellDAO()


    def update_spell(self, spell: Spell):
        self.DAO.update_spell(spell)


    def create_empty(self, lang):
        spell = Spell(None, lang)
        id = self.DAO.create_spell(spell)
        spell.id = id

        return spell
