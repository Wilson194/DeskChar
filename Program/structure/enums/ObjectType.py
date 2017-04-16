from structure.enums.AutoNumber import AutoNumber


class ObjectType(AutoNumber):
    ITEM = ()  # 1
    SPELL = ()  # 2
    ABILITY = ()  # 3
    MODIFIER = ()  # 4
    EFFECT = ()  # 5
    CHARACTER = ()  # 6
    MONSTER = ()  # 7
    SCENARIO = ()  # 8
    LOCATION = ()  # 9
    ABILITY_CONTEXT = ()  # 10
    PARTY_CHARACTER = ()  # 11


    def icon(self):
        if self is ObjectType.SPELL:
            return 'resources/icons/book.png'
        if self is ObjectType.ABILITY:
            return 'resources/icons/map.png'
        if self is ObjectType.ITEM:
            return 'resources/icons/crate.png'
        if self is ObjectType.MODIFIER:
            return 'resources/icons/gemGreen.png'
        if self is ObjectType.EFFECT:
            return 'resources/icons/potionGreen.png'
        if self is ObjectType.CHARACTER:
            return 'resources/icons/helmet.png'
        if self is ObjectType.MONSTER:
            return 'resources/icons/imp.png'
        if self is ObjectType.SCENARIO:
            return 'resources/icons/envelope.png'
        if self is ObjectType.LOCATION:
            return 'resources/icons/scroll.png'
        if self is ObjectType.ABILITY_CONTEXT:
            return 'resources/icons/gemRed.png'

        return 'resources/icons/book.png'


    def instance(self):
        from structure.items.Item import Item
        from structure.spells.Spell import Spell
        from structure.abilities.Ability import Ability
        from structure.effects.Effect import Effect
        from structure.effects.Modifier import Modifier
        from structure.character.Character import Character
        from structure.monster.Monster import Monster
        from structure.scenario.Scenario import Scenario
        from structure.scenario.Location import Location
        from structure.effects.AbilityContext import AbilityContext
        from structure.character.PartyCharacter import PartyCharacter

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
        if self == ObjectType.SCENARIO:
            return Scenario
        if self == ObjectType.LOCATION:
            return Location
        if self == ObjectType.ABILITY_CONTEXT:
            return AbilityContext
        if self == ObjectType.PARTY_CHARACTER:
            return PartyCharacter


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
        if name == 'SCENARIO':
            return self.SCENARIO
        if name == 'LOCATION':
            return self.LOCATION
        if name == 'ABILITY_CONTEXT' or name == 'CONTEXT':
            return self.ABILITY_CONTEXT
        if name == 'PARTY_CHARACTER' or name == 'PARTYCHARACTER':
            return self.PARTY_CHARACTER
