# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, FileSystemLoader
from presentation.Translate import Translate
import os
import shutil

from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.general.Object import Object
from structure.items import Container


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(autoescape=True, loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                                                        'templates')))
ICONS = ['ability.png', 'armor.png', 'axe.png', 'bag.png', 'book.png', 'bow.png', 'coin.png', 'crate.png', 'dagger.png',
         'drd.png', 'helmet.png', 'imp.png', 'location.png', 'map.png', 'skull.png', 'sword.png', 'tools.png', 'treasure.png',
         'gemRed.png', 'gemGreen.png', 'effect.png', 'gold.png', 'silver.png', 'copper.png'
         ]


def render_template(template_file, **kwargs):
    template = env.get_template(template_file)
    return template.render(**kwargs)


class HtmlHandler:
    def create_html(self, objects, destination):
        # self.to_unicode(objects)

        resourcesFolder = os.path.join(os.path.dirname(destination), 'resources')
        if not os.path.isdir(resourcesFolder):
            os.mkdir(resourcesFolder)

        if not os.path.isdir(os.path.join(resourcesFolder, 'icons')):
            os.mkdir(os.path.join(resourcesFolder, 'icons'))

        if not os.path.isdir(os.path.join(resourcesFolder, 'maps')):
            os.mkdir(os.path.join(resourcesFolder, 'maps'))

        for icon in ICONS:
            source = os.path.join('resources', 'icons', icon)
            target = os.path.join(os.path.dirname(destination), 'resources', 'icons')
            shutil.copy2(source, target)

        if len(objects) == 0:
            return

        export = objects[0].object_type

        objects.sort(key=lambda x: x.name)

        for i in range(len(objects)):
            if objects[i].description:
                objects[i].description = objects[i].description.replace('\n', '<br>')

        html = render_template(
            "base.html",
            objects=objects,
            objectType=ObjectType,
            itemType=Items,
            export=export,
            tr=Translate(),
            TR=Translate,
            base=True
        )

        with open(destination, 'w', encoding='utf8') as file:
            file.write(html)

        # ------------- Add other files -----------------------
        items = []
        spells = []
        abilities = []
        effects = []
        monsters = []
        locations = []
        maps = []
        characters = []
        for obj in objects:
            if obj.object_type is ObjectType.ITEM:
                if obj.type == Items.CONTAINER:
                    items += self.get_all_items(obj)
            else:
                items += self.get_all_items(obj)

            spells += self.get_all_spells(obj)
            abilities += self.get_all_abilities(obj)
            effects += self.get_all_effects(obj)
            monsters += self.get_all_monsters(obj)
            locations += self.get_all_locations(obj)
            maps += self.get_all_maps(obj)
            characters += self.get_all_characters(obj)

        if objects[0].object_type is not ObjectType.ITEM:
            self.create_external_html(items, ObjectType.ITEM, destination, 'items.html')

        if objects[0].object_type is not ObjectType.SPELL:
            self.create_external_html(spells, ObjectType.SPELL, destination, 'spells.html')

        if objects[0].object_type is not ObjectType.ABILITY:
            self.create_external_html(abilities, ObjectType.ABILITY, destination, 'abilities.html')

        if objects[0].object_type is not ObjectType.EFFECT:
            self.create_external_html(effects, ObjectType.EFFECT, destination, 'effects.html')

        if objects[0].object_type is not ObjectType.MONSTER:
            self.create_external_html(monsters, ObjectType.MONSTER, destination, 'monsters.html')

        self.create_external_html(locations, ObjectType.LOCATION, destination, 'locations.html')

        if objects[0].object_type is not ObjectType.MAP:
            self.create_external_html(maps, ObjectType.MAP, destination, 'maps.html')

        if objects[0].object_type is not ObjectType.CHARACTER:
            self.create_external_html(characters, ObjectType.CHARACTER, destination, 'characters.html')

        for map in maps:
            source = os.path.join('resources', 'maps', 'exportedMap-{}.png'.format(map.id))
            target = os.path.join(os.path.dirname(destination), 'resources', 'maps')
            shutil.copy2(source, target)


    def to_unicode(self, objects):
        for obj in objects:
            obj.name = obj.name.encode('utf8')
            obj.description = obj.description.encode('utf8')


    def get_all_items(self, root: Object):
        items = []

        # ------------------ Character -------------------------
        if root.object_type == ObjectType.CHARACTER:
            items += self.get_all_items(root.inventory)

        # ------------------ Monster -------------------------
        if root.object_type == ObjectType.MONSTER:
            items += root.items + root.armors + root.moneyList + root.meleeWeapons + root.rangedWeapons + root.throwableWeapons
            for container in root.containers:
                items += self.get_all_items(container)

        # ------------------ Location -------------------------
        if root.object_type == ObjectType.LOCATION:
            items += root.items + root.armors + root.moneyList + root.meleeWeapons + root.rangedWeapons + root.throwableWeapons
            for container in root.containers:
                items += self.get_all_items(container)

            for location in root.locations:
                items += self.get_all_items(location)

            for character in root.characters:
                items += self.get_all_items(character)

            for monster in root.monsters:
                items += self.get_all_items(monster)

        # ------------------ Character -------------------------
        if root.object_type == ObjectType.MONSTER:
            items += root.items + root.armors + root.moneyList + root.meleeWeapons + root.rangedWeapons + root.throwableWeapons

            for container in root.containers:
                items += self.get_all_items(container)

        # ------------------ Scenario -------------------------
        if root.object_type == ObjectType.SCENARIO:
            items += root.items + root.armors + root.moneyList + root.meleeWeapons + root.rangedWeapons + root.throwableWeapons

            for container in root.containers:
                items += self.get_all_items(container)

            for location in root.locations:
                items += self.get_all_items(location)

            for character in root.party:
                items += self.get_all_items(character)

        if root.object_type == ObjectType.ITEM:
            items.append(root)

            if root.type == Items.CONTAINER:
                items += root.items + root.armors + root.moneyList + root.meleeWeapons + root.rangedWeapons + root.throwableWeapons

                for container in root.containers:
                    items += self.get_all_items(container)

        return items


    def get_all_spells(self, root: Object):
        spells = []
        if root.object_type is ObjectType.SCENARIO:
            spells += root.spells

            for location in root.locations:
                spells += self.get_all_spells(location)

            for character in root.party:
                spells += self.get_all_spells(character)

        if root.object_type is ObjectType.LOCATION:

            for character in root.characters:
                spells += self.get_all_spells(character)

            for monster in root.monsters:
                spells += self.get_all_spells(monster)

            for location in root.locations:
                spells += self.get_all_spells(location)

        if root.object_type is ObjectType.CHARACTER:
            spells += root.spells

        if root.object_type is ObjectType.MONSTER:
            spells += root.spells

        if root.object_type is ObjectType.SPELL:
            spells.append(root)

        return spells


    def get_all_effects(self, root: Object):
        effects = []
        if root.object_type is ObjectType.SCENARIO:
            effects += root.effects

            for location in root.locations:
                effects += self.get_all_effects(location)

            for character in root.party:
                effects += self.get_all_effects(character)

        if root.object_type is ObjectType.LOCATION:

            for character in root.characters:
                effects += self.get_all_effects(character)

            for location in root.locations:
                effects += self.get_all_effects(location)

        if root.object_type is ObjectType.CHARACTER:
            effects += root.effects

        if root.object_type is ObjectType.EFFECT:
            effects.append(root)

        return effects


    def get_all_abilities(self, root: Object):
        abilities = []
        if root.object_type is ObjectType.SCENARIO:
            abilities += root.abilities

            for location in root.locations:
                abilities += self.get_all_abilities(location)

            for character in root.party:
                abilities += self.get_all_abilities(character)

        if root.object_type is ObjectType.LOCATION:

            for character in root.characters:
                abilities += self.get_all_abilities(character)

            for monster in root.monsters:
                abilities += self.get_all_abilities(monster)

            for location in root.locations:
                abilities += self.get_all_abilities(location)

        if root.object_type is ObjectType.CHARACTER:
            abilities += root.abilities

        if root.object_type is ObjectType.MONSTER:
            abilities += root.abilities

        if root.object_type is ObjectType.ABILITY:
            abilities.append(root)

        return abilities


    def get_all_monsters(self, root: Object):
        monsters = []

        if root.object_type is ObjectType.SCENARIO:

            for location in root.locations:
                monsters += self.get_all_monsters(location)

        if root.object_type is ObjectType.LOCATION:
            monsters += root.monsters

            for location in root.locations:
                monsters += self.get_all_monsters(location)

        if root.object_type is ObjectType.MONSTER:
            monsters.append(root)

        return monsters


    def get_all_locations(self, root: Object):
        locations = []

        if root.object_type == ObjectType.SCENARIO:
            locations += root.locations

            for location in root.locations:
                locations += self.get_all_locations(location)

        if root.object_type == ObjectType.LOCATION:
            locations.append(root)

            for location in root.locations:
                locations += self.get_all_locations(location)

        return locations


    def get_all_maps(self, root: Object):
        maps = []

        if root.object_type is ObjectType.SCENARIO:
            for location in root.locations:
                maps += self.get_all_maps(location)

        if root.object_type is ObjectType.LOCATION:
            maps += root.maps

            for location in root.locations:
                maps += self.get_all_maps(location)

        if root.object_type is ObjectType.MAP:
            maps.append(root)

        return maps


    def get_all_characters(self, root: Object):
        characters = []

        if root.object_type is ObjectType.SCENARIO:
            for partyCharacter in root.party:
                if partyCharacter.character:
                    characters.append(partyCharacter.character)

            for location in root.locations:
                characters += self.get_all_characters(location)

        if root.object_type is ObjectType.LOCATION:
            characters += root.characters

            for location in root.locations:
                characters += self.get_all_characters(location)

        if root.object_type is ObjectType.CHARACTER:
            characters.append(root)

        return characters


    def create_external_html(self, items, objectType, destination, filename):

        items = list(set(items))
        items.sort(key=lambda x: x.id)
        if len(items) > 0:
            html = render_template(
                "base.html",
                objects=items,
                objectType=ObjectType,
                itemType=Items,
                export=objectType,
                tr=Translate(),
                TR=Translate,
                base=False
            )

            itemFile = os.path.join(os.path.dirname(destination), filename)
            with open(itemFile, 'w', encoding='utf8') as file:
                file.write(html)
