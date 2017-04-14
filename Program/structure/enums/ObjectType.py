from structure.enums.AutoNumber import AutoNumber


class ObjectType(AutoNumber):
    ITEM = ()
    SPELL = ()
    ABILITY = ()
    MODIFIER = ()
    EFFECT = ()
    CHARACTER = ()
    MONSTER = ()


    def icon(self):
        if self is ObjectType.SPELL:
            return 'resources/icons/book.png'
        if self is ObjectType.ABILITY:
            return 'resources/icons/map.png'
        if self is ObjectType.ITEM:
            return 'resources/icons/axe.png'
        if self is ObjectType.MODIFIER:
            return 'resources/icons/potionGreen.png'
        if self is ObjectType.EFFECT:
            return 'resources/icons/gemGreen.png'
        if self is ObjectType.CHARACTER:
            return 'resources/icons/helmet.png'
        if self is ObjectType.MONSTER:
            return 'resources/icons/imp.png'

        return 'resources/icons/book.png'


    def instance(self):
        from structure.items.Item import Item
        from structure.spells.Spell import Spell
        from structure.abilities.Ability import Ability
        from structure.effects.Effect import Effect
        from structure.effects.Modifier import Modifier
        from structure.character.Character import Character
        from structure.monster.Monster import Monster

        if self == ObjectType.ITEM:
            return Item
        if self == ObjectType.SPELL:
            return Spell
        if self == ObjectType.ABILITY:
            return Ability
        if self == ObjectType.MODIFIER:
            return Modifier
        if self == ObjectType.EFFECT:
            return Effect
        if self == ObjectType.CHARACTER:
            return Character
        if self == ObjectType.MONSTER:
            return Monster


    def by_name(self, name: str):
        name = name.upper()
        if name == 'ITEM':
            return self.ITEM
        if name == 'SPELL':
            return self.SPELL
        if name == 'ABILITY':
            return self.ABILITY
        if name == 'MODIFIER':
            return self.MODIFIER
        if name == 'EFFECT':
            return self.EFFECT
        if name == 'CHARACTER':
            return self.CHARACTER
        if name == 'MONSTER':
            return self.MONSTER
