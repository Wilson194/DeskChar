from structure.enums.AutoNumber import AutoNumber


class Classes(AutoNumber):
    ALCHEMIST = ()
    MAGICIAN = ()
    RANGER = ()
    THIEF = ()
    WARRIOR = ()

    def xml_name(self):
        return self.name