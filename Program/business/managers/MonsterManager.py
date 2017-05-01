from business.managers.interface.IMonsterManager import IMonsterManager
from data.DAO.MonsterDAO import MonsterDAO
from structure.enums.ObjectType import ObjectType
from structure.monster.Monster import Monster


class MonsterManager(IMonsterManager):
    def __init__(self):
        self.DAO = MonsterDAO()


    def create(self, monster: Monster, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(monster, nodeParentId, contextType)


    def update_monster(self, monster: Monster):
        return self.DAO.update(monster)


    def delete(self, monsterId: int):
        return self.DAO.delete(monsterId)


    def get(self, monsterId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Monster:
        return self.DAO.get(monsterId, lang, nodeId, contextType)


    def get_all(self, lang=None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang):
        item = Monster(None, lang)
        id = self.DAO.create(item)
        item.id = id

        return item
