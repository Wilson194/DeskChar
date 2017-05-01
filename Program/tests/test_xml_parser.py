import unittest
from lxml import etree
import filecmp
import os

from data.xml.ParserHandler import ParserHandler
from structure.character.Character import Character
from structure.effects.Effect import Effect
from structure.effects.Modifier import Modifier
from structure.enums.Alignment import Alignment
from structure.enums.ArmorSize import ArmorSize
from structure.enums.Classes import Classes
from structure.enums.ItemsAttributes import ItemsAttributes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.enums.ModifierValueTypes import ModifierValueTypes
from structure.enums.Races import Races
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.spells.Spell import Spell


class TestXMLParser(unittest.TestCase):
    """
    Test XML parser. Test import and export XML file.
    XML file is tested based on prepared template
    """


    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        if os.path.isfile('tests/resources/character_out.xml'):
            os.remove('tests/resources/character_out.xml')


    def test_parse(self):
        """
        Test parse prepared template.
        :return: 
        """
        objects = ParserHandler().import_xml('tests/resources/character.xml')

        character = objects[0]['cs']

        self.assertEqual(character.name, 'Wilson', 'Bad name of character')
        self.assertEqual(character.description, 'Postava Wilson', 'Bad description of character')

        self.assertEqual(character.currentMana, 90, 'Bad value of current mana')
        self.assertEqual(character.maxMana, 150, 'Bad value of max mana')
        self.assertEqual(character.currentHealth, 20, 'Bad value of current Health')
        self.assertEqual(character.maxHealth, 20, 'Bad value of nax health')
        self.assertEqual(character.charisma, 35, 'Bad value of charisma')
        self.assertEqual(character.intelligence, 40, 'Bad value of inteligence')
        self.assertEqual(character.strength, 20, 'Bad value of strength')
        self.assertEqual(character.age, 24, 'Bad value of age')
        self.assertEqual(character.height, 195, 'Bad value of height')
        self.assertEqual(character.weight, 87, 'Bad value of weight')
        self.assertEqual(character.level, 13, 'Bad value of level')
        self.assertEqual(character.xp, 1555, 'Bad value of xp')
        self.assertEqual(character.alignment, Alignment.LAWFUL_GOOD, 'Bad value of alignment')
        self.assertEqual(character.drdClass, Classes.MAGICIAN, 'Bad value of drdClass')
        self.assertEqual(character.drdRace, Races.ELF, 'Bad value of drdRace')
        self.assertEqual(character.mobility, 20, 'Bad value of mobility')
        self.assertEqual(character.agility, 20, 'Bad value of agility')
        self.assertEqual(character.toughness, 18, 'Bad value of toughness')

        spell = character.spells[0]

        self.assertEqual(spell.name, 'Ohnivá koule', 'Bad name of spell')
        self.assertEqual(spell.description, 'Ohnivá koule', 'Bad description of spell')
        self.assertEqual(spell.drd_class, Classes.MAGICIAN, 'Bad class of spell')
        self.assertEqual(spell.mana_cost_continual, '0', 'Bad value of mana cost continual of spell')
        self.assertEqual(spell.mana_cost_initial, '10', 'Bad value of mana cost initial of spell')
        self.assertEqual(spell.range, '10 sáhů', 'Bad value of range of spell')
        self.assertEqual(spell.duration, '1', 'Bad value of duration of spell')
        self.assertEqual(spell.cast_time, 1, 'Bad value of cast time of spell')
        self.assertEqual(spell.scope, '1 sáh', 'Bad value of scope of spell')

        armor = character.inventory.armors[0]

        self.assertEqual(armor.name, 'Plášť', 'Bad name of armor')
        self.assertEqual(armor.description, 'Plášť', 'Bad description of armor')
        self.assertEqual(armor.price, 50, ' Bad price of armor')
        self.assertEqual(armor.quality, 20, 'Bad quality of armor')
        self.assertEqual(armor.weightA, 12, 'Bad weightA of armor')
        self.assertEqual(armor.weightB, 12, 'Bad weightB of armor')
        self.assertEqual(armor.weightC, 15, 'Bad weightC of armor')
        self.assertEqual(armor.size, ArmorSize.B, 'Bad size of armor')
        self.assertEqual(armor.amount, 1, 'Bad amount of armor')

        effect = armor.effects[0]

        self.assertEqual(effect.name, 'Ochrana', 'Bad name of armor effect')
        self.assertEqual(effect.description, 'Ochrana pláště', 'Bad description of armor effect')
        self.assertEqual(effect.targetType, ModifierTargetTypes.ARMOR, 'Bad target type of armor effect')
        self.assertEqual(bool(effect.active), True, 'Bad value of armor effect active')

        modifier = effect.modifiers[0]

        self.assertEqual(modifier.targetType, ModifierTargetTypes.ARMOR, 'Bad target type of effect modifier')
        self.assertEqual(modifier.itemTargetAttribute, ItemsAttributes.WEAPON_DEFENCE, 'Bad item attribute of effect modifier')
        self.assertEqual(modifier.characterTargetAttribute, None, 'Character target attribute is not None')
        self.assertEqual(modifier.valueType, ModifierValueTypes.FROM_TOTAL, 'Bad value type of effect modifier')
        self.assertEqual(modifier.value, 15, 'Bad value of effect modifier')


    def test_export(self):
        """
        Test create new XML template same as prepared one
        :return: 
        """
        character = Character(3, 'cs', 'Wilson', 'Postava Wilson', 20, 35, 40, 20, 20, 18, 24, 195, 87, 13, 1555, 20, 150,
                              Classes.MAGICIAN, Races.ELF, Alignment.LAWFUL_GOOD, 20, 90)

        spell = Spell(5, 'cs', 'Ohnivá koule', 'Ohnivá koule', '10', '0', '10 sáhů', '1 sáh', 1, '1', Classes.MAGICIAN)

        character.spells = [spell]

        armor = Armor(27, 'cs', 'Plášť', 'Plášť', None, 50, 20, 12, 12, 15, ArmorSize.B, 1)
        effect = Effect(8, 'cs', 'Ochrana', 'Ochrana pláště', ModifierTargetTypes.ARMOR, True)
        modifier = Modifier(14, 'cs', '', '', ModifierValueTypes.FROM_TOTAL, 15, None, ItemsAttributes.WEAPON_DEFENCE,
                            ModifierTargetTypes.ARMOR)
        inventory = Container(24, 'cs', 'Inventory', None, -1)
        ground = Container(25, 'cs', 'Ground', None, -2)

        effect.modifiers = [modifier]
        armor.effects = [effect]
        character.inventory = inventory
        character.ground = ground
        character.inventory.armors = [armor]

        root = character.XmlClass()().create_xml(character)

        root = ParserHandler().sort_tree(root)

        with open('tests/resources/character_out.xml', 'w', encoding='UTF-8') as out:
            out.write(etree.tostring(root, pretty_print=True, encoding='UTF-8').decode('UTF-8'))

        self.assertTrue(filecmp.cmp('tests/resources/character_out.xml', 'tests/resources/character.xml'), 'Files are not same')
