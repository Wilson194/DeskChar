from structure.enums.AutoNumber import AutoNumber


class ItemsAttributes(AutoNumber):
    WEIGHT = ()
    CONTAINER_CAPACITY = ()
    CONTAINER_WEIGHT = ()
    ARMOR_QUALITY = ()
    ARMOR_SIZE = ()
    WEAPON_STRENGTH = ()
    WEAPON_RAMPANCY = ()
    WEAPON_DEFENCE = ()
    WEAPON_INITIATIVE = ()
    WEAPON_WEIGHT = ()
    WEAPON_MELEE_LENGTH = ()
    WEAPON_MELEE_HANDLING = ()
    WEAPON_RANGED_RANGE_ALL = ()
    WEAPON_RANGED_RANGE_LOW = ()
    WEAPON_RANGED_RANGE_MEDIUM = ()
    WEAPON_RANGED_RANGE_LONG = ()


    def by_name(self, name):
        name = name.upper()
        if name == 'WEIGHT':
            return self.WEIGHT
        if name == 'CONTAINER_CAPACITY':
            return self.CONTAINER_WEIGHT
        if name == 'CONTAINER_WEIGHT':
            return self.CONTAINER_WEIGHT
        if name == 'ARMOR_QUALITY':
            return self.ARMOR_QUALITY
        if name == 'ARMOR_SIZE':
            return self.ARMOR_SIZE
        if name == 'WEAPON_STRENGTH':
            return self.WEAPON_STRENGTH
        if name == 'WEAPON_RAMPANCY':
            return self.WEAPON_RAMPANCY
        if name == 'WEAPON_DEFENCE':
            return self.WEAPON_DEFENCE
        if name == 'WEAPON_INITIATIVE':
            return self.WEAPON_INITIATIVE
        if name == 'WEAPON_WEIGHT':
            return self.WEAPON_WEIGHT
        if name == 'WEAPON_MELEE_LENGTH':
            return self.WEAPON_MELEE_LENGTH
        if name == 'WEAPON_MELEE_HANDLING':
            return self.WEAPON_MELEE_HANDLING
        if name == 'WEAPON_RANGED_RANGE_ALL':
            return self.WEAPON_RANGED_RANGE_ALL
        if name == 'WEAPON_RANGED_RANGE_LOW':
            return self.WEAPON_RANGED_RANGE_LOW
        if name == 'WEAPON_RANGED_RANGE_MEDIUM':
            return self.WEAPON_RANGED_RANGE_MEDIUM
        if name == 'WEAPON_RANGED_RANGE_LONG':
            return self.WEAPON_RANGED_RANGE_LONG



    def __str__(self):
        return self.name
