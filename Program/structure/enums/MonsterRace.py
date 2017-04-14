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
