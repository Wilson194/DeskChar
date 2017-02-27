from structure.enums.AutoNumber import AutoNumber


class ObjectType(AutoNumber):
    ITEM = ()
    SPELL = ()
    ABILITY = ()


    def icon(self):
        if self is ObjectType.SPELL:
            return 'resources/icons/book.png'

        return 'resources/icons/book.png'


    def by_name(self, name):
        name = name.upper()
        if name == 'ITEM':
            return self.ITEM
        if name == 'SPELL':
            return self.SPELL
        if name == 'ABILITY':
            return self.ABILITY
