from structure.enums.AutoNumber import AutoNumber


class Items(AutoNumber):
    GENERIC = ()
    CONTAINER = ()
    MELEE_WEAPON = ()
    RANGED_WEAPON = ()
    THROWABLE_WEAPON = ()
    ARMOR = ()
    MONEY = ()


    def by_name(self, name: str):
        name = name.upper()
        if name == 'GENERIC':
            return self.GENERIC
        if name == 'CONTAINER':
            return self.CONTAINER
        if name == 'MELEE_WEAPON' or name == 'MELEEWEAPON':
            return self.MELEE_WEAPON
        if name == 'RANGED_WEAPON' or name == 'RANGEDWEAPON':
            return self.RANGED_WEAPON
        if name == 'THROWABLE_WEAPON' or name == 'THROWABLEWEAPON':
            return self.THROWABLE_WEAPON
        if name == 'ARMOR':
            return self.ARMOR
        if name == 'MONEY':
            return self.MONEY
        return None


    def instance(self):
        from structure.items.Item import Item
        from structure.items.Armor import Armor
        from structure.items.Container import Container
        from structure.items.MeleeWeapon import MeleeWeapon
        from structure.items.RangeWeapon import RangeWeapon
        from structure.items.ThrowableWeapon import ThrowableWeapon
        from structure.items.Money import Money

        if self is self.GENERIC:
            return Item
        if self is self.CONTAINER:
            return Container
        if self is self.MELEE_WEAPON:
            return MeleeWeapon
        if self is self.RANGED_WEAPON:
            return RangeWeapon
        if self is self.THROWABLE_WEAPON:
            return ThrowableWeapon
        if self is self.ARMOR:
            return Armor
        if self is self.MONEY:
            return Money
        return None


