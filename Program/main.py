from structure.items.Item import *
from database.DatabaseTables import *
from database.ObjectDatabase import *
from ItemDAO import *
from AbilityDAO import *
from Spell import *
from SpellDAO import *
from structure.abilities.Ability import *

DatabaseTables().create_tables()

a = Database('test.db')

# item = Item(None, 'cs', 'Ohnivy mec', 'Mec planouci samotnym ohnem pekelnym',
#             None, 25, 25)
#
# ItemDAO().create_item(item)
#
# ItemDAO().delete_item(1)



# ab = Ability(None,'cs','Hledani stop', 'Schopnost hledani stop na zemi', '2x hod kostkou')
# AbilityDAO().create_ability(ab)

sp = Spell(None, 'cs', 'Ohnivá koule', 'Vypálíš ohnivou kouli jako ďas',
           '25 mana', '50 mana', '20 sáhů', 'velký', 2, '2 dny')

# SpellDAO().create_spell(sp)

spell = SpellDAO().get_all_spells()[0]
print(spell.name)
# i = Item(6,'cs','Ohnivy mec','Vely ohnivy mec zkazy','Weapon')
# i.a = 5
# ObjectDatabase('test.db').update_object(i)

# print(ItemDAO().get_all_items()[0].lang)

# print(i.__name__())
# print (i.__dict__.items())
# for j in i.__dict__:
#     print(j)


# ItemDAO().update_item(i)
#
#
#
# values = {
#     'weight': 30,
#     'amount': 25,
#     'capacity': 5
# }
# a.update('Item', 3, values)
