from data.DAO.EffectDAO import EffectDAO
from data.DAO.SpellDAO import SpellDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.enums.Classes import Classes
from structure.enums.ModifierTargetTypes import ModifierTargetTypes
from structure.spells.Spell import Spell




class XMLEffect(XMLTemplate):
    ROOT_NAME = 'effect'


    def __init__(self):
        self.DAO = EffectDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            taty = self.get_value(root, 'targetType', None, False)

            taty_num = ModifierTargetTypes.by_name(ModifierTargetTypes, taty)

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
