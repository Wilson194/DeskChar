from lxml import etree
from Parser import *


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


elemnt = etree.fromstring(xml)
print(elemnt)


# xml_tree = etree.parse('spells.xml')
# root = xml_tree.getroot()
# #
# element = root[0]
#
# a = XmlSpell(element).parse()
#
# new = etree.Element('spell')
# b = XmlSpell(new).create(a)
#
# print(XmlSpell(b).parse())

# for element in root:
#     print(XmlSpell(element).parse())

# for element in root:
#     a = (element.findall('name'))
#     for i in a:
#         print(i.values()[0], end='')
#         print(' -> ', end='')
#         print(i.text, end='')
#         print('; ',end='')
#     print('')




