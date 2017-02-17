from structure.items.Item import Item


class Armor(Item):
    def __init__(self, id: int = None, lang=None, name: str = None,
                 description: str = None, parent_id: int = None):
        super().__init__(id, lang, name, description, parent_id)
