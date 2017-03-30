from structure.enums.AutoNumber import AutoNumber


class CharacterAttributes(AutoNumber):
    STRENGTH = ()
    AGILITY = ()
    TOUGHNESS = ()
    INTELLIGENCE = ()
    CHARISMA = ()
    MOBILITY = ()
    STRENGTH_BONUS = ()
    AGILITY_BONUS = ()
    TOUGHNESS_BONUS = ()
    INTELLIGENCE_BONUS = ()
    CHARISMA_BONUS = ()
    MOBILITY_BONUS = ()
    HEALTH = ()
    MANA = ()
    WEIGHT = ()
    HEIGHT = ()
    OBSERVATION_RANDOM = ()
    OBSERVATION_SEARCHING = ()
    OBSERVATION_MECHANISM = ()


    def by_name(self, name):
        name = name.upper()
        if name == 'STRENGTH':
            return self.STRENGTH
        if name == 'AGILITY':
            return self.AGILITY
        if name == 'TOUGHNESS':
            return self.TOUGHNESS
        if name == 'INTELLIGENCE':
            return self.INTELLIGENCE
        if name == 'CHARISMA':
            return self.CHARISMA
        if name == 'MOBILITY':
            return self.MOBILITY
        if name == 'STRENGTH_BONUS':
            return self.STRENGTH_BONUS
        if name == 'AGILITY_BONUS':
            return self.AGILITY_BONUS
        if name == 'TOUGHNESS_BONUS':
            return self.TOUGHNESS_BONUS
        if name == 'INTELLIGENCE_BONUS':
            return self.INTELLIGENCE_BONUS
        if name == 'CHARISMA_BONUS':
            return self.CHARISMA_BONUS
        if name == 'MOBILITY_BONUS':
            return self.MOBILITY_BONUS
        if name == 'HEALTH':
            return self.HEALTH
        if name == 'MANA':
            return self.MANA
        if name == 'WEIGHT':
            return self.WEIGHT
        if name == 'HEIGHT':
            return self.HEIGHT
        if name == 'OBSERVATION_RANDOM':
            return self.OBSERVATION_RANDOM
        if name == 'OBSERVATION_SEARCHING':
            return self.OBSERVATION_SEARCHING
        if name == 'OBSERVATION_MECHANISM':
            return self.OBSERVATION_MECHANISM

        return None


    def __str__(self):
        return self.name
