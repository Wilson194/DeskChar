from data.DAO.MonsterDAO import MonsterDAO
from structure.abilities.Ability import Ability
from structure.monster.Monster import Monster


class MonsterManager:
    def __init__(self):
        self.DAO = MonsterDAO()


    def update_monster(self, monster: Monster):
        self.DAO.update(monster)
