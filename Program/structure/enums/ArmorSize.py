from structure.enums.AutoNumber import AutoNumber


class ArmorSize(AutoNumber):
    A = ()
    B = ()
    C = ()


    def by_name(self, name: str):
        name = name.upper()
        if name == 'A':
            return self.A
        if name == 'B':
            return self.B
        if name == 'C':
            return self.C

        return None


    def __str__(self):
        return self.name
