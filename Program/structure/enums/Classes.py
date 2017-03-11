from structure.enums.AutoNumber import AutoNumber


class Classes(AutoNumber):
    ALCHEMIST = ()
    MAGICIAN = ()
    RANGER = ()
    THIEF = ()
    WARRIOR = ()


    def xml_name(self):
        return self.name


    def by_name(self, name):
        name = name.upper()
        if name == 'ALCHEMIST':
            return self.ALCHEMIST
        if name == 'MAGICIAN':
            return self.MAGICIAN
        if name == 'RANGER':
            return self.RANGER
        if name == 'THIEF':
            return self.THIEF
        if name == 'WARRIOR':
            return self.WARRIOR
        return None
