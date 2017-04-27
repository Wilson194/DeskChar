from structure.enums.AutoNumber import AutoNumber


class ModifierValueTypes(AutoNumber):
    TO_TOTAL = ()
    FROM_BASE = ()
    FROM_TOTAL = ()
    TYPE_ARMOR_SIZE = ()
    TYPE_WEAPON_HANDLING = ()
    TYPE_WEAPON_WEIGHT = ()


    def by_name(self, name):
        name = name.upper()
        if name == 'TO_TOTAL':
            return self.TO_TOTAL
        if name == 'FROM_BASE':
            return self.FROM_BASE
        if name == 'FROM_TOTAL':
            return self.FROM_TOTAL
        if name == 'TYPE_ARMOR_SIZE':
            return self.TYPE_ARMOR_SIZE
        if name == 'TYPE_WEAPON_HANDLING':
            return self.TYPE_WEAPON_HANDLING
        if name == 'TYPE_WEAPON_WEIGHT':
            return self.TYPE_WEAPON_WEIGHT
        return None


    def __str__(self):
        return self.name
