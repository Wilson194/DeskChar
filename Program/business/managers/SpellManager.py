
from structure.spells.Spell import Spell


class SpellManager:
    def __init__(self):
        from data.DAO.SpellDAO import SpellDAO
        self.DAO = SpellDAO()


    def update_spell(self, spell: Spell):
        self.DAO.update(spell)


    def create_empty(self, lang):
        spell = Spell(None, lang)
        id = self.DAO.create(spell)
        spell.id = id

        return spell
