from data.DAO.DAO import DAO
from data.DAO.EffectDAO import EffectDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.interface.IItemDAO import IItemDAO
from data.database.ObjectDatabase import ObjectDatabase
from structure.enums.ArmorSize import ArmorSize
from structure.enums.Handling import Handling
from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.enums.Races import Races
from structure.enums.WeaponWeight import WeaponWeight
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.Item import Item
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon
from structure.tree.NodeObject import NodeObject


class ItemDAO(DAO, IItemDAO):
    DATABASE_TABLE = 'Item'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.ITEM


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, item: Item, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new Item, depend on item type, insert correct data
        Items types:
            Item, Armor, Container, MeleeWeapon, ThrowableWeapon, RangedWeapon, Money
        :param item: Item object
        :param nodeParentId: id of parent node in tree
        :param contextType: Object type of tree, where item is located
        :return: id of created item
        """
        if not contextType:
            contextType = self.TYPE

        strValues = {
            'name'       : item.name,
            'description': item.description
        }
        intValues = {
            'amount': item.amount,
            'price' : item.price,
            'type'  : item.type.value if item.type else None,
            'weight': item.weight
        }
        if isinstance(item, Armor):
            intValues.update({
                'quality': item.quality,
                'weightA': item.weightA,
                'weightB': item.weightB,
                'weightC': item.weightC,
                'size'   : item.size.value if item.size else None,
            })

        elif isinstance(item, Container):
            intValues.update({
                'capacity' : item.capacity,
                'parent_id': item.parent_id
            })

        elif isinstance(item, MeleeWeapon):
            intValues.update({
                'strength'    : item.strength,
                'rampancy'    : item.rampancy,
                'defence'     : item.defence,
                'length'      : item.length,
                'initiative'  : item.initiative,
                'handling'    : item.handling.value if item.handling else None,
                'weaponWeight': item.weaponWeight.value if item.weaponWeight else None,
                'racial'      : item.racial.value if item.racial else None

            })
        elif isinstance(item, Money):
            intValues.update({
                'copper': item.copper,
                'silver': item.silver,
                'gold'  : item.gold
            })

        elif isinstance(item, RangeWeapon):
            intValues.update({
                'initiative'  : item.initiative,
                'strength'    : item.strength,
                'rampancy'    : item.rampancy,
                'rangeLow'    : item.rangeLow,
                'rangeMedium' : item.rangeMedium,
                'rangeHigh'   : item.rangeHigh,
                'weaponWeight': item.weaponWeight.value if item.weaponWeight else None,
                'racial'      : item.racial.value if item.racial else None
            })
        elif isinstance(item, ThrowableWeapon):
            intValues.update({
                'initiative'  : item.initiative,
                'strength'    : item.strength,
                'rampancy'    : item.rampancy,
                'rangeLow'    : item.rangeLow,
                'rangeMedium' : item.rangeMedium,
                'rangeHigh'   : item.rangeHigh,
                'defence'     : item.defence,
                'weaponWeight': item.weaponWeight.value if item.weaponWeight else None,
                'racial'      : item.racial.value if item.racial else None
            })

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        item.id = id

        self.database.insert_translate(strValues, item.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, item.name, nodeParentId, item)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for effect in item.effects:
            EffectDAO().create(effect, nodeId, contextType)

        if isinstance(item, Container):
            for one in item.containers + item.armors + item.moneyList + item.meleeWeapons + item.rangedWeapons + item.throwableWeapons + item.items:
                self.create(one, nodeId, contextType)

        return id


    def update(self, item: Item):
        """
        Update item in database
        :param item: Item object with new data
        """
        strValues = {
            'name'       : item.name,
            'description': item.description
        }
        intValues = {
            'amount': item.amount,
            'price' : item.price,
            'type'  : item.type.value if item.type else None,
            'weight': item.weight
        }
        if isinstance(item, Armor):
            intValues.update({
                'quality': item.quality,
                'weightA': item.weightA,
                'weightB': item.weightB,
                'weightC': item.weightC,
                'size'   : item.size.value,

            })

        elif isinstance(item, Container):
            intValues.update({
                'capacity': item.capacity,
            })

        elif isinstance(item, MeleeWeapon):
            intValues.update({
                'strength'    : item.strength,
                'rampancy'    : item.rampancy,
                'defence'     : item.defence,
                'length'      : item.length,
                'initiative'  : item.initiative,
                'handling'    : item.handling.value if item.handling else None,
                'weaponWeight': item.weaponWeight.value if item.weaponWeight else None,
                'racial'      : item.racial.value if item.racial else None
            })
        elif isinstance(item, Money):
            intValues.update({
                'copper': item.copper,
                'silver': item.silver,
                'gold'  : item.gold
            })

        elif isinstance(item, RangeWeapon):
            intValues.update({
                'initiative'  : item.initiative,
                'strength'    : item.strength,
                'rampancy'    : item.rampancy,
                'rangeLow'    : item.rangeLow,
                'rangeMedium' : item.rangeMedium,
                'rangeHigh'   : item.rangeHigh,
                'weaponWeight': item.weaponWeight.value if item.weaponWeight else None,
                'racial'      : item.racial.value if item.racial else None
            })
        elif isinstance(item, ThrowableWeapon):
            intValues.update({
                'initiative'  : item.initiative,
                'strength'    : item.strength,
                'rampancy'    : item.rampancy,
                'rangeLow'    : item.rangeLow,
                'rangeMedium' : item.rangeMedium,
                'rangeHigh'   : item.rangeHigh,
                'defence'     : item.defence,
                'weaponWeight': item.weaponWeight.value if item.weaponWeight else None,
                'racial'      : item.racial.value if item.racial else None
            })

        self.database.update(self.DATABASE_TABLE, item.id, intValues)
        self.database.update_translate(strValues, item.lang, item.id, self.TYPE)


    def delete(self, item_id: int):
        """
        Delete Item from database and from translate
        :param item_id: id of Item
        """
        self.database.delete(self.DATABASE_TABLE, item_id)
        self.database.delete_where('translates',
                                   {'target_id': item_id, 'type': ObjectType.ITEM})


    def get_all(self, lang=None) -> list:
        """
        Get list of items for selected lang
        :param lang: lang of items
        :return: list of items
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all('Item')

        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items


    def get(self, item_id: int, lang=None, nodeId: int = None, contextType: ObjectType = None) -> Item:
        """
        Get Item , object transable attributes depends on lang
        If nodeId and contextType is specified, whole object is returned (with all sub objects)
        If not specified, only basic attributes are set.        
        
        Returned correct type of item, depend on database, possible classes are:
                Item, Container, Armor, Money, MeleeWeapon, RangedWeapon, ThrowableWeapon
        :param item_id: id of Item
        :param lang: lang of object
        :param nodeId: id of node in tree, where object is located
        :param contextType: object type of tree, where is node
        :return: Item object
        """
        if lang is None:
            lang = 'cs'
        data = self.database.select(self.DATABASE_TABLE, {'ID': item_id})
        if not data:
            return None
        else:
            data = dict(data[0])

        tr_data = dict(self.database.select_translate(item_id, ObjectType.ITEM.value,
                                                      lang))

        if data['type'] == Items.CONTAINER.value:
            item = Container(item_id, lang, tr_data.get('name', ''),
                             tr_data.get('description', ''),
                             data.get('parent_id', 0), data.get('weight', 0),
                             data.get('price', 0),
                             data.get('capacity', 0), data.get('amount', 1))

        elif data['type'] == Items.MELEE_WEAPON.value:
            weaponWeightIndex = data.get('weaponWeight', None)
            weaponWeight = WeaponWeight(weaponWeightIndex) if weaponWeightIndex else None

            handlingIndex = data.get('handling', None)
            handling = Handling(handlingIndex) if handlingIndex else None

            racialIndex = data.get('racial', None)
            racial = Races(racialIndex) if racialIndex else None

            item = MeleeWeapon(item_id, lang, tr_data.get('name', ''),
                               tr_data.get('description', ''), data.get('parent_id', 0),
                               data.get('weight', 0), data.get('price', 0), data.get('strength', 0),
                               data.get('rampancy', 0), data.get('defence', 0),
                               data.get('length', 0), weaponWeight, handling, data.get('amount', 1), data.get('initiative', 0),
                               racial)

        elif data['type'] == Items.THROWABLE_WEAPON.value:
            weaponWeightIndex = data.get('weaponWeight', None)
            weaponWeight = WeaponWeight(weaponWeightIndex) if weaponWeightIndex else None

            racialIndex = data.get('racial', None)
            racial = Races(racialIndex) if racialIndex else None

            item = ThrowableWeapon(item_id, lang, tr_data.get('name', ''),
                                   tr_data.get('description', ''),
                                   data.get('parent_id', 0), data.get('weight', 0),
                                   data.get('price', 0), data.get('initiative', 0),
                                   data.get('strength', 0), data.get('rampancy', 0),
                                   data.get('rangeLow', 0), data.get('rangeMedium', 0),
                                   data.get('rangeHigh', 0), data.get('defence', 0),
                                   weaponWeight, data.get('amount', 1), racial)

        elif data['type'] == Items.RANGED_WEAPON.value:
            weaponWeightIndex = data.get('weaponWeight', None)
            weaponWeight = WeaponWeight(weaponWeightIndex) if weaponWeightIndex else None

            racialIndex = data.get('racial', None)
            racial = Races(racialIndex) if racialIndex else None

            item = RangeWeapon(item_id, lang, tr_data.get('name', ''),
                               tr_data.get('description', ''),
                               data.get('parent_id', 0), data.get('weight', 0),
                               data.get('price', 0), data.get('initiative', 0),
                               data.get('strength', 0), data.get('rampancy', 0),
                               data.get('rangeLow', 0), data.get('rangeMedium', 0),
                               data.get('rangeHigh', 0), data.get('amount', 1), weaponWeight, racial)

        elif data['type'] == Items.ARMOR.value:
            sizeIndex = data.get('size', None)
            size = ArmorSize(sizeIndex) if sizeIndex else None
            item = Armor(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                         data.get('parent_id', 0), data.get('price', 0), data.get('quality', 0),
                         data.get('weightA', 0), data.get('weightB', 0), data.get('weightC', 0),
                         size, data.get('amount', 1))

        elif data['type'] == Items.MONEY.value:
            item = Money(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                         data.get('parent_id', 0), data.get('copper'), data.get('silver'),
                         data.get('gold'), data.get('amount', 1))

        else:
            item = Item(item_id, lang, tr_data.get('name', ''), tr_data.get('description', ''),
                        data.get('parent_id', 0), data.get('weight', 0), data.get('price', 0),
                        data.get('amount', 1))

        if nodeId and contextType:
            objects = PlayerTreeDAO().get_children_objects(nodeId, contextType)
            effects = []

            armors = []
            containers = []
            items = []
            moneys = []
            meleeWeapons = []
            rangedWeapons = []
            throwableWeapons = []
            for one in objects:
                if one.object.object_type is ObjectType.ITEM and data['type'] == Items.CONTAINER.value:
                    childItem = self.get(one.object.id, None, one.id, contextType)
                    if isinstance(childItem, Armor):
                        armors.append(childItem)
                    elif isinstance(childItem, Container):
                        containers.append(childItem)
                    elif isinstance(childItem, Money):
                        moneys.append(childItem)
                    elif isinstance(childItem, MeleeWeapon):
                        meleeWeapons.append(childItem)
                    elif isinstance(childItem, RangeWeapon):
                        rangedWeapons.append(childItem)
                    elif isinstance(childItem, ThrowableWeapon):
                        throwableWeapons.append(childItem)
                    else:
                        items.append(childItem)
                elif one.object.object_type is ObjectType.EFFECT:
                    effect = EffectDAO().get(one.object.id, None, one.id, contextType)
                    effects.append(effect)

            if data['type'] is Items.CONTAINER.value:
                item.items = items
                item.armors = armors
                item.moneyList = moneys
                item.meleeWeapons = meleeWeapons
                item.rangedWeapons = rangedWeapons
                item.throwableWeapons = throwableWeapons
                item.containers = containers

            item.effects = effects
        return item
