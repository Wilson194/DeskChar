from data.DAO.ModifierDAO import ModifierDAO
from structure.effects.Modifier import Modifier


class ModifierManager:
    def __init__(self):
        self.DAO = ModifierDAO()


    def update(self, modifier: Modifier):
        self.DAO.update(modifier)


    def create_empty(self, lang):
        pass
