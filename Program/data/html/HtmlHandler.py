# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, FileSystemLoader
from presentation.Translate import Translate
import os

from structure.enums.Items import Items
from structure.enums.ObjectType import ObjectType

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(autoescape=True, loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                                                        'templates')))


def render_template(template_file, **kwargs):
    template = env.get_template(template_file)
    return template.render(**kwargs)


class HtmlHandler:
    def create_html(self, objects, destination):
        # self.to_unicode(objects)

        export = objects[0].object_type
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


    def to_unicode(self, objects):
        for obj in objects:
            obj.name = obj.name.encode('utf8')
            obj.description = obj.description.encode('utf8')
