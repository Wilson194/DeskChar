from structure.enums.AutoNumber import AutoNumber


class ModifierValueTypes(AutoNumber):
    TO_TOTAL = ()
    FROM_BASE = ()
    FROM_TOTAL = ()


    def by_name(self, name):
        name = name.upper()
        if name == 'TO_TOTAL':
            return self.TO_TOTAL
        if name == 'FROM_BASE':
            return self.FROM_BASE
        if name == 'FROM_TOTAL':
            return self.FROM_TOTAL
        return None


    def __str__(self):
        return self.name
