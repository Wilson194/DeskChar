from data.DAO.ItemDAO import ItemDAO
from structure.items.Item import Item


class ItemManager:
    def __init__(self):
        self.DAO = ItemDAO()


    def update_item(self, item: Item):
        self.DAO.update(item)


    def create_empty(self, lang):
        item = Item(None, lang)
        id = self.DAO.create(item)
        item.id = id

        return item
