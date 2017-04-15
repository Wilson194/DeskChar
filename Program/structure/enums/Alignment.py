from structure.enums.AutoNumber import AutoNumber


class Alignment(AutoNumber):
    LAWFUL_GOOD = ()
    CHAOTIC_GOOD = ()
    NEUTRAL = ()
    CHAOTIC_EVIL = ()
    LAWFUL_EVIL = ()


    def __str__(self):
        return self.name
