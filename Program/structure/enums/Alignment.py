from structure.enums.AutoNumber import AutoNumber


class Alignment(AutoNumber):
    LAWFUL_GOOD = ()
    CHAOTIC_GOOD = ()
    NEUTRAL = ()
    CHAOTIC_EVIL = ()
    LAWFUL_EVIL = ()


    def __str__(self):
        return self.name


    def by_name(self, name: str):
        name = name.upper()
        if name == 'LAWFUL_GOOD':
            return self.LAWFUL_GOOD
        if name == 'CHAOTIC_GOOD':
            return self.CHAOTIC_GOOD
        if name == 'NEUTRAL':
            return self.NEUTRAL
        if name == 'CHAOTIC_EVIL':
            return self.CHAOTIC_EVIL
        if name == 'LAWFUL_EVIL':
            return self.LAWFUL_EVIL
