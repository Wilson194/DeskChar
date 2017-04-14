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
