from structure.items.Item import *
from database.DatabaseTables import *
from database.ObjectDatabase import *
from ItemDAO import *

# DatabaseTables().create_tables()

a = Database('a')

# item = Item(None, 'cs', 'Ohnivy mec', 'Mec planouci samotnym ohnem pekelnym',
#             None, 25, 25)
#
# ItemDAO().create_item(item)
#
# ItemDAO().delete_item(1)



i = Item(1,'cs','Test','Test','Item')
i.a = 5
ObjectDatabase('test').insert_object(i)

#
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
