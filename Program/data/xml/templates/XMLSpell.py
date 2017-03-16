from data.DAO.SpellDAO import SpellDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Classes import Classes
from structure.spells.Spell import Spell


class XMLSpell(XMLTemplate):
    ROOT_NAME = 'spell'


    def __init__(self):
        self.DAO = SpellDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            mani = self.get_value(root, 'manaInitial', lang)
            manc = self.get_value(root, 'manaContinual', lang)
            rang = self.get_value(root, 'range', lang)
            scop = self.get_value(root, 'scope', lang)
            cati = self.get_value(root, 'castTime')
            dura = self.get_value(root, 'duration', lang)
            clas = self.get_value(root, 'class', None, False)

            clas_num = Classes.by_name(Classes, clas)

            obj = Spell(None, lang, name, desc, mani, manc,
                        rang, scop, cati, dura, clas_num.value)
            data[lang] = obj

        return data



    def remap_names(self, name: str) -> str:
        if name == 'mana_cost_initial':
            return 'manaInitial'
        if name == 'mana_cost_continual':
            return 'manaContinual'
        if name == 'drd_class':
            return 'class'
        if name == 'ID':
            return 'id'
        if name == 'cast_time':
            return 'castTime'
        return name
