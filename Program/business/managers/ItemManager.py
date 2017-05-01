from business.managers.interface.IItemManager import IItemManager
from data.DAO.ItemDAO import ItemDAO
from structure.enums.ObjectType import ObjectType
from structure.items.Item import Item


class ItemManager(IItemManager):
    def __init__(self):
        self.DAO = ItemDAO()


    def create(self, item: Item, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(item, nodeParentId, contextType)


    def update(self, item: Item):
        return self.DAO.update(item)


    def delete(self, itemId: int):
        return self.DAO.delete(itemId)


    def get(self, itemId: int, lang=None, nodeId: int = None, contextType: ObjectType = None) -> Item:
        return self.DAO.get(itemId, lang, nodeId, contextType)


    def get_all(self, lang=None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang) -> Item:
        item = Item(None, lang)
        id = self.DAO.create(item)
        item.id = id

        return item
