# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, FileSystemLoader
from presentation.Translate import Translate
import os
import shutil

from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType
from structure.items import Container

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(autoescape=True, loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                                                        'templates')))


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

        for object in objects:
            shutil.copy2(object.icon, os.path.join(resourcesFolder, 'icons'))

            if object.object_type == ObjectType.MAP:
                # print(object.finalMapPath)
                fileMap = 'exportedMap-{}.png'.format(object.id)
                fileMapPath = os.path.join('resources', 'maps', fileMap)
                shutil.copy2(fileMapPath, os.path.join(resourcesFolder, 'maps'))

                for item in object.mapItems:
                    shutil.copy2(item.itemType.icon(), os.path.join(resourcesFolder, 'icons'))

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
            tr=Translate()
        )

        with open(destination, 'w', encoding='utf8') as file:
            file.write(html)

    # ********************* Character ***********************************************
        if objects[0].object_type == ObjectType.CHARACTER:
            spells = []
            abilities = []
            effects = []
            items = []
            for obj in objects:
                spells += obj.spells
                abilities += obj.abilities
                effects += obj.effects
                items += self.get_items(obj.inventory)

            spellFile = os.path.join(os.path.dirname(destination), 'spells.html')
            abilityFile = os.path.join(os.path.dirname(destination), 'abilities.html')
            effectFile = os.path.join(os.path.dirname(destination), 'effects.html')
            itemFile = os.path.join(os.path.dirname(destination), 'items.html')

            self.create_html(spells, spellFile)
            self.create_html(abilities, abilityFile)
            self.create_html(effects, effectFile)
            self.create_html(items, itemFile)





    def to_unicode(self, objects):
        for obj in objects:
            obj.name = obj.name.encode('utf8')
            obj.description = obj.description.encode('utf8')


    def get_items(self, parent: Container, items: list = []):
        items += parent.items
        items += parent.armors
        items += parent.containers
        items += parent.meleeWeapons
        items += parent.moneyList
        items += parent.rangedWeapons
        items += parent.throwableWeapons

        for cont in parent.containers:
            items = self.get_items(cont, items)

        return items
