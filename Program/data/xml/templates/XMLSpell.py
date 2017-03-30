from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Classes import Classes
from structure.enums.ObjectType import ObjectType
from data.xml.templates.XMLTemplate import XInstance, XElement, XAttribElement


class XMLSpell(XMLTemplate):
    ROOT_NAME = 'spell'
    OBJECT_TYPE = ObjectType.SPELL


    def __init__(self):
        self.id = XElement('id')
        self.name = XAttribElement('name', 'lang')
        self.description = XAttribElement('description', 'lang')
        self.mana_cost_initial = XAttribElement('manaInitial', 'lang')
        self.mana_cost_continual = XAttribElement('manaContinual', 'lang')
        self.range = XAttribElement('range', 'lang')
        self.scope = XAttribElement('scope', 'lang')
        self.cast_time = XElement('castTime')
        self.duration = XAttribElement('duration', 'lang')
        self.drd_class = XElement('class', Classes)
