# from PIL import Image
# from os import mkdir
#
# sheet = Image.open("resources/icons/image-tango-feet.png")
# count = 0
#
# for x in range(26):
#     for y in range(10):
#         a = ((x + 1) * 30) + 48
#         b = ((y + 1) * 30) + 424
#         icon = sheet.crop((a - 25, b - 25, a, b))  # Problem here
#         icon.save("resources/icons/{}.png".format(count))
#         count += 1


# from structure.enums.Classes import Classes
#
# print(Classes.ALCHEMIST)



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
from lxml import etree

xml_root = etree.fromstring(xml)

# print(xml_root.findall('name'))
expr = "//{}[@lang='{}']".format('name','cs')

a = xml_root.xpath(expr)[0]
print(a.text)