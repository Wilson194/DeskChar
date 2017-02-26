from structure.enums.AutoNumber import AutoNumber


class ObjectType(AutoNumber):
    ITEM = ()
    SPELL = ()
    ABILITY = ()

    def icon(self):
        if self is ObjectType.SPELL:
            return 'resources/icons/book.png'

        return 'resources/icons/book.png'
