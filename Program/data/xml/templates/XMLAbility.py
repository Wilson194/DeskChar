from data.DAO.AbilityDAO import AbilityDAO
from data.xml.templates.XMLTemplate import XMLTemplate
from structure.abilities.Ability import Ability
from structure.enums.Classes import Classes

from structure.enums.Races import Races


class XMLAbility(XMLTemplate):
    ROOT_NAME = 'ability'


    def __init__(self):
        self.DAO = AbilityDAO()


    def get_object(self, root) -> object:
        data = {}
        langs = self.get_langs(root)
        expr = "./{}[@lang='{}']"
        for lang in langs:
            name = self.get_value(root, 'name', lang)
            desc = self.get_value(root, 'description', lang)
            chan = self.get_value(root, 'chance', lang)
            clas = self.get_value(root, 'class', None, False)
            race = self.get_value(root, 'race', None, False)

            clas_num = Classes.by_name(Classes, clas)
            race_num = Races.by_name(Races, race)

            obj = Ability(None, lang, name, desc, chan, race_num, clas_num)
            data[lang] = obj

        return data




    def remap_names(self, name: str) -> str:
        return name
