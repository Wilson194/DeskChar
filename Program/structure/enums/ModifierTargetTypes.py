from structure.enums.AutoNumber import AutoNumber


class ModifierTargetTypes(AutoNumber):
    CHARACTER = ()
    ITEM = ()
    MELEE_WEAPON = ()
    RANGED_WEAPON = ()
    CONTAINER = ()
    MONEY = ()
    ARMOR = ()
    THROWABLE_WEAPON = ()




    def by_name(self, name):
        name = name.upper()
        if name == 'AFFECTS_CHARACTER':
            return self.CHARACTER
        if name == 'AFFECTS_ITEM':
            return self.ITEM
        if name == 'AFFECTS_MELEE_WEAPON':
            return self.MELEE_WEAPON
        if name == 'AFFECTS_RANGED_WEAPON':
            return self.RANGED_WEAPON
        if name == 'AFFECTS_THROWABLE_WEAPON':
            return self.THROWABLE_WEAPON
        if name == 'AFFECT_ARMOR':
            return self.ARMOR
        if name == 'AFFECT_CONTAINER':
            return self.CONTAINER
        if name == 'AFFECTS_MONEY':
            return self.MONEY

        return None

    def __str__(self):
        return 'AFFECTS_' + self.name
