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
from Database import Database
from Spell import Spell
from SpellDAO import SpellDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO

# s = Spell(6, 'cs', 'Ohnivá koule', 'Velká ohnivá koule', 'a', 'b', 'c', 'd', 1, 'f')
# SpellDAO().update_spell(s)

# print(SpellDAO().get_languages(6))

d  = Database('test.db')
print(d.select_all('translates'))

# p = PlayerTreeDAO()
#
# p.get_root_nodes()
# from managers.PlayerTreeManager import PlayerTreeManager
#
#
# print(PlayerTreeManager().get_spell_tree())
# from Folder import Folder
# from Node import Node
# from structure.tree.Object import Object
#
# f = Folder(2)
# o = Object()
# c = Folder()
# n = Node()
# print(isinstance(f,Folder))
# f.children = [c]
# print(c,f)
# print(f.id)
# a = [f, o]

#
# def set_name(obj):
#     # print(obj.id)
#     if obj.id is None:
#         obj.name = 'pes'
#     else:
#         obj.name = 'kocka'
#
#
# for i in a:
#     set_name(i)
#
# print(a[0].name)
# print(a[1].name)

#
# from enum import Enum
#
#
# class T(Enum):
#     SPELL = 1
#     ABILITY = 2
#
#
#
# print(T(1))