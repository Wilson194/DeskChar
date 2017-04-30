import unittest

from data.DAO.AbilityContextDAO import AbilityContextDAO
from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.CharacterDAO import CharacterDAO
from data.DAO.EffectDAO import EffectDAO
from data.DAO.ItemDAO import ItemDAO
from data.DAO.LocationDAO import LocationDAO
from data.DAO.ModifierDAO import ModifierDAO
from data.DAO.MonsterDAO import MonsterDAO
from data.DAO.ScenarioDAO import ScenarioDAO
from data.DAO.SpellDAO import SpellDAO
from data.database.Database import Database
from data.database.DatabaseTables import DatabaseTables
from data.database.ObjectDatabase import ObjectDatabase
from structure.abilities.Ability import Ability
from structure.character.Character import Character
from structure.effects.AbilityContext import AbilityContext
from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.enums.Alignment import Alignment
from structure.enums.ArmorSize import ArmorSize
from structure.enums.CharacterAttributes import CharacterAttributes
from structure.enums.Classes import Classes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.MonsterRace import MonsterRace
from structure.enums.MonsterSize import MonsterSize
from structure.enums.Races import Races
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.monster.Monster import Monster
from structure.scenario.Location import Location
from structure.scenario.Scenario import Scenario
from structure.spells.Spell import Spell
import datetime


class TestDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = Database('unitTests.db')
        DatabaseTables().create_tables('unitTests.db')


    @classmethod
    def tearDownClass(cls):
        database = Database('unitTests.db')
        ObjectDatabase(':memory:').drop_table('Character')


    def test_ability(self):
        DAO = AbilityDAO('unitTests.db')

        ability = Ability(None, 'cs', 'Find steps', 'You can find steps everywhere', '10% in wood', Races.ELF, Classes.RANGER, 2)
        ability2 = Ability(None, 'cs', 'Fly', 'I believe i can fly', '0.000001%', Races.ELF, Classes.RANGER, 2)

        id = DAO.create(ability)
        id2 = DAO.create(ability2)

        ability.id = id
        ability2.id = id2

        getAbility = DAO.get(id)
        getAbility2 = DAO.get(id2)

        self.assertEqual(ability, getAbility, 'First ability is not equal')
        self.assertEqual(ability2, getAbility2, 'Second ability is not equal')
        self.assertNotEqual(getAbility, getAbility2, 'First and second ability is equal')

        ability.name = 'Updated find steps'
        DAO.update(ability)
        getObject = DAO.get(id)

        self.assertEqual(getObject, ability)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_character(self):
        DAO = CharacterDAO()

        character = Character(None, 'cs', 'Wilson', 'Character Wilson', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, Classes.RANGER,
                              Races.ELF, Alignment.LAWFUL_GOOD, 1, 1)
        character2 = Character(None, 'cs', 'Don', 'Character Don', 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, Classes.MAGICIAN,
                               Races.KROLL, Alignment.LAWFUL_EVIL, 1, 1)

        id = DAO.create(character)
        id2 = DAO.create(character2)

        getCharacter = DAO.get(id)
        getCharacter2 = DAO.get(id2)

        self.assertEqual(character, getCharacter, 'First character is not equal')
        self.assertEqual(character2, getCharacter2, 'Second character is not equal')
        self.assertNotEqual(getCharacter, getCharacter2, 'First and second character is equal')

        character.intelligence = 5
        DAO.update(character)
        getObject = DAO.get(id)

        self.assertEqual(getObject, character)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_effect(self):
        DAO = EffectDAO()

        effect = Effect(None, 'cs', 'Magic defence', 'Magic defence for armor', ModifierTargetTypes.ARMOR, True)
        effect2 = Effect(None, 'cs', 'Magic attack', 'Magic attack for sword', ModifierTargetTypes.MELEE_WEAPON, False)

        id = DAO.create(effect)
        id2 = DAO.create(effect2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(effect, getObject, 'First effect is not equal')
        self.assertEqual(effect2, getObject2, 'Second effect is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second effect is equal')

        effect.name = 'Updated magic defence'
        DAO.update(effect)
        getObject = DAO.get(id)

        self.assertEqual(getObject, effect)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_spell(self):
        DAO = SpellDAO()

        spell = Spell(None, 'cs', 'Fireball', 'Mighty fireball', '8', '5', '2', '12', 2, '15', Classes.MAGICIAN)
        spell2 = Spell(None, 'cs', 'Blink', 'Fast blink', '2', '1', '6', '15', 4, '5', Classes.MAGICIAN)

        id = DAO.create(spell)
        id2 = DAO.create(spell2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(spell, getObject, 'First spell is not equal')
        self.assertEqual(spell2, getObject2, 'Second spell is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second spell is equal')

        spell.name = 'Updated fireball'
        DAO.update(spell)
        getObject = DAO.get(id)

        self.assertEqual(getObject, spell)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_item(self):
        DAO = ItemDAO()

        item = Armor(None, 'cs', 'Chain armor', 'Big armor', None, 15, 35, 10, 15, 20, ArmorSize.B, 1)
        item2 = Container(None, 'cs', 'Lather bag', 'Big lather bag', None, 15, 20, 150, 1)

        id = DAO.create(item)
        id2 = DAO.create(item2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(item, getObject, 'First item is not equal')
        self.assertEqual(item2, getObject2, 'Second item is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second item is equal')

        item.name = 'Updated chain armor'
        DAO.update(item)
        getObject = DAO.get(id)

        self.assertEqual(getObject, item)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_monster(self):
        DAO = MonsterDAO()

        monster = Monster(None, 'cs', 'Gorgona', 'Mocná gorgona', '1', '2', 3, 4, 5, 6, 7, 8, 9, Alignment.LAWFUL_EVIL, 11, 12,
                          MonsterRace.ANIMAL, MonsterSize.C)
        monster2 = Monster(None, 'cs', 'Imp', 'Malý imp', '1', '2', 3, 4, 5, 6, 7, 8, 9, Alignment.LAWFUL_EVIL, 11, 12,
                           MonsterRace.MYTHIC, MonsterSize.A)

        id = DAO.create(monster)
        id2 = DAO.create(monster2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(monster, getObject, 'First monster is not equal')
        self.assertEqual(monster2, getObject2, 'Second monster is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second monster is equal')

        monster.name = 'Updated gorgona'
        DAO.update(monster)
        getObject = DAO.get(id)

        self.assertEqual(getObject, monster)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_modifier(self):
        DAO = ModifierDAO()

        modifier = Modifier(None, 'cs', None, None, ModifierValueTypes.TO_TOTAL, 25, CharacterAttributes.STRENGTH, None,
                            ModifierTargetTypes.CHARACTER)
        modifier2 = Modifier(None, 'cs', None, None, ModifierValueTypes.FROM_BASE, 12, None, ItemsAttributes.WEAPON_DEFENCE,
                             ModifierTargetTypes.MELEE_WEAPON)

        id = DAO.create(modifier)
        id2 = DAO.create(modifier2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(modifier, getObject, 'First modifier is not equal')
        self.assertEqual(modifier2, getObject2, 'Second modifier is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second modifier is equal')

        modifier.value = 49
        DAO.update(modifier)
        getObject = DAO.get(id)

        self.assertEqual(getObject, modifier)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_context(self):
        DAO = AbilityContextDAO()

        context = AbilityContext(None, 'cs', None, None, ModifierValueTypes.FROM_BASE, 25, CharacterAttributes.STRENGTH)
        context2 = AbilityContext(None, 'cs', None, None, ModifierValueTypes.TO_TOTAL, 15, CharacterAttributes.AGILITY)

        id = DAO.create(context)
        id2 = DAO.create(context2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(context, getObject, 'First context is not equal')
        self.assertEqual(context2, getObject2, 'Second context is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second context is equal')

        context.value = 49
        DAO.update(context)
        getObject = DAO.get(id)

        self.assertEqual(getObject, context)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_location(self):
        DAO = LocationDAO()

        location = Location(None, 'cs', 'Dark wood', 'Big dark wood with dangerous thief')
        location2 = Location(None, 'cs', 'High mountain', 'Big mountain where dwarf lives')

        id = DAO.create(location)
        id2 = DAO.create(location2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(location, getObject, 'First location is not equal')
        self.assertEqual(location2, getObject2, 'Second location is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second location is equal')

        location.name = 'Updated dark wood'
        DAO.update(location)
        getObject = DAO.get(id)

        self.assertEqual(getObject, location)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)


    def test_scenario(self):
        DAO = ScenarioDAO()

        scenario = Scenario(None, 'cs', 'Scenario', 'Big scenario', datetime.date.fromordinal(6542))
        scenario2 = Scenario(None, 'cs', 'Scenario 2', 'Big scenario 2', datetime.date.fromordinal(65412))

        id = DAO.create(scenario)
        id2 = DAO.create(scenario2)

        getObject = DAO.get(id)
        getObject2 = DAO.get(id2)

        self.assertEqual(scenario, getObject, 'First scenario is not equal')
        self.assertEqual(scenario2, getObject2, 'Second scenario is not equal')
        self.assertNotEqual(getObject, getObject2, 'First and second scenario is equal')

        scenario.name = 'Updated map of underground'
        DAO.update(scenario)
        getObject = DAO.get(id)

        self.assertEqual(getObject, scenario)

        DAO.delete(id)

        deleted = DAO.get(id)
        self.assertIsNone(deleted)
