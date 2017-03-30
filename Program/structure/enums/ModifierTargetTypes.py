from structure.enums.AutoNumber import AutoNumber


class ModifierTargetTypes(AutoNumber):
    ITEM = ()
    CHARACTER = ()


    def by_name(self, name):
        name = name.upper()
        if name == 'AFFECTS_CHARACTER':
            return self.CHARACTER
        if name == 'AFFECTS_ITEM':
            return self.ITEM
        return None

    def __str__(self):
        return self.name
