from structure.enums.AutoNumber import AutoNumber


class MonsterSize(AutoNumber):
    A0 = ()
    A = ()
    B = ()
    C = ()
    D = ()
    E = ()


    def __str__(self):
        return self.name


    def by_name(self, name):
        name = name.upper()
        if name == 'A0':
            return self.A0
        if name == 'A':
            return self.A
        if name == 'B':
            return self.B
        if name == 'C':
            return self.C
        if name == 'D':
            return self.D
        if name == 'E':
            return self.E
