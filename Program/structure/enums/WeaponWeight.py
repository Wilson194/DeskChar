from structure.enums.AutoNumber import AutoNumber


class WeaponWeight(AutoNumber):
    LIGHT = ()
    MIDDLE = ()
    HEAVY = ()


    def by_name(self, name: str):
        name = name.upper()
        if name == 'LIGHT':
            return self.LIGHT
        if name == 'MIDDLE':
            return self.MIDDLE
        if name == 'HEAVY':
            return self.HEAVY

        return None


    def __str__(self):
        return self.name
