from structure.enums.AutoNumber import AutoNumber


class MonsterRace(AutoNumber):
    DRAGON = ()
    ANIMAL = ()
    INSECT = ()
    UNDEAD = ()
    HUMANOID = ()
    MYTHIC = ()
    OTHERS = ()


    def __str__(self):
        return self.name


    def by_name(self, name: str):
        name = name.upper()
        if name == 'DRAGON':
            return self.DRAGON
        if name == 'ANIMAL':
            return self.ANIMAL
        if name == 'INSECT':
            return self.INSECT
        if name == 'UNDEAD':
            return self.UNDEAD
        if name == 'HUMANOID':
            return self.HUMANOID
        if name == 'MYTHIC':
            return self.MYTHIC
        if name == 'OTHERS ':
            return self.OTHERS
