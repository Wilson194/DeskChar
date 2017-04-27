from structure.enums.AutoNumber import AutoNumber


class MapItemType(AutoNumber):
    OBJECT = ()
    MONSTER = ()
    ROOM = ()
    ITEM = ()

    def by_name(self, name: str):
        name = name.upper()
        if name == 'OBJECT':
            return self.OBJECT
        if name == 'MONSTER':
            return self.MONSTER
        if name == 'ROOM':
            return self.ROOM
        if name == 'ITEM':
            return self.ITEM

        return None

    def icon(self):
        if self is MapItemType.OBJECT:
            return 'resources/icons/crate.png'
        if self is MapItemType.MONSTER:
            return 'resources/icons/skull.png'
        if self is MapItemType.ROOM:
            return 'resources/icons/map.png'
        if self is MapItemType.ITEM:
            return 'resources/icons/treasure.png'

        return 'resources/icons/iconPlaceholder.png'

    def __str__(self):
        return self.name
