from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.EffectDAO import EffectDAO
from structure.abilities.Ability import Ability
from structure.effects.Effect import Effect


class EffectManager:
    def __init__(self):
        self.DAO = EffectDAO()


    def update_effect(self, effect: Effect):
        self.DAO.update(effect)
