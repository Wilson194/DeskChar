from structure.enums.AutoNumber import AutoNumber


class Races(AutoNumber):
    BARBARIAN = ()
    DWARF = ()
    ELF = ()
    HOBBIT = ()
    HUMAN = ()
    KROLL = ()
    KUDUK = ()

    def xml_name(self):
        return self.name

    def by_name(self, name):
        name = name.upper()
        if name == 'BARBARIAN':
            return self.BARBARIAN
        if name == 'DWARF':
            return self.DWARF
        if name == 'ELF':
            return self.ELF
        if name == 'HOBBIT':
            return self.HOBBIT
        if name == 'HUMAN':
            return self.HUMAN
        if name == 'KROLL':
            return self.KROLL
        if name == 'KUDUK':
            return self.KUDUK
        return None

