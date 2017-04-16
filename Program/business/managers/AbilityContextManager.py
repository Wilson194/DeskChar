from data.DAO.AbilityContextDAO import AbilityContextDAO
from structure.effects.AbilityContext import AbilityContext


class ModifierManager:
    def __init__(self):
        self.DAO = AbilityContextDAO()


    def update(self, context: AbilityContext):
        self.DAO.update(context)


    def create_empty(self, lang):
        pass
