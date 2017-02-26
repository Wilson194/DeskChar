import unittest
from lxml import etree
from data.xml.ParserHandler import *

xml = '''
<spell>
    <class>MAGICIAN</class>
    <description lang="cs">Velká ohnivá koule zla, která pálí a ničí vše v místě, kam se rozhodne dopadnout.</description>
    <duration lang="cs">Efekt okamžitý, pálí to pak ještě půl dne...</duration>
    <manaContinual lang="cs">0</manaContinual>
    <manaInitial lang="cs">5 + 1.25 ^ sáhy rozsahu</manaInitial>
    <name lang="cs">Ohnivá koule</name>
    <range lang="cs">0 - 50 sáhů</range>
    <scope lang="cs">Dle dodané magenergie</scope>
    <name lang="en">Fireball</name>
    <description lang="en">Big fiery ball of evil, which burns and destroys everything in the impact zone.</description>
    <manaInitial lang="en">5 + 1.25 ^ fathoms in scope</manaInitial>
    <manaContinual lang="en">0</manaContinual>
    <range lang="en">0 - 50 fathoms</range>
    <scope lang="en">According to supplied magenergie</scope>
    <duration lang="en">Effect is immidiate, but you can feel it for another half a day...</duration>
    <castTime>2</castTime>
</spell>
'''


class ParserTest(unittest.TestCase):
    def test_parser(self):
        xml_root = etree.fromstring(xml)

        data_dict = Parser(xml_root).parse()

        new_root = etree.Element('spell')
        new_xml = Parser(new_root).create(data_dict)

        new_data_dict = Parser(new_xml).parse()

        self.assertEqual(data_dict, new_data_dict, 'Parse create another data dictionary!')
