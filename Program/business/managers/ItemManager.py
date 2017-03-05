from data.DAO.ItemDAO import ItemDAO
from structure.items.Item import Item


class ItemManager:
    def __init__(self):
        self.DAO = ItemDAO()


    def update_item(self, item: Item):
        self.DAO.update_item(item)


    def create_empty(self, lang):
        item = Item(None, lang)
        id = self.DAO.create_item(item)
        item.id = id

        return item
