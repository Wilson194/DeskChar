# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(autoescape=True, loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                                                        'templates')))


def render_template(template_file, **kwargs):
    template = env.get_template(template_file)
    return template.render(**kwargs)


class HtmlHandler:
    def create_html(self, objects, destination):
        # self.to_unicode(objects)

        html = render_template(
            "base.html",
            items=objects,
        )

        with open(destination, 'w', encoding='utf8') as file:
            file.write(html)


    def to_unicode(self, objects):
        for obj in objects:
            obj.name = obj.name.encode('utf8')
            obj.description = obj.description.encode('utf8')