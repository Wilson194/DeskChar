from datetime import date
from datetime import datetime

from data.DAO.AbilityDAO import AbilityDAO
from data.DAO.CharacterDAO import CharacterDAO
from data.DAO.EffectDAO import EffectDAO
from data.DAO.LocationDAO import LocationDAO
from data.DAO.PartyCharacterDAO import PartyCharacterDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
from data.DAO.SpellDAO import SpellDAO
from data.database.Database import Database
from data.database.ObjectDatabase import ObjectDatabase
from structure.character.PartyCharacter import PartyCharacter
from structure.enums.Alignment import Alignment
from structure.enums.MonsterRace import MonsterRace
from structure.enums.ObjectType import ObjectType
from structure.items.Armor import Armor
from structure.items.Container import Container
from structure.items.MeleeWeapon import MeleeWeapon
from structure.items.Money import Money
from structure.items.RangeWeapon import RangeWeapon
from structure.items.ThrowableWeapon import ThrowableWeapon
from structure.monster.Monster import Monster

from data.DAO.DAO import DAO
from structure.scenario.Scenario import Scenario
from structure.tree.NodeObject import NodeObject


class ScenarioDAO(DAO):
    DATABASE_TABLE = 'Scenario'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.SCENARIO


    def __init__(self):
        self.database = ObjectDatabase(self.DATABASE_DRIVER)
        self.treeDAO = PlayerTreeDAO()


    def create(self, scenario: Scenario, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        """
        Create new spell in database
        :param scenario: Spell object
        :return: id of autoincrement
        """
        if not contextType:
            contextType = self.TYPE

        curDate = datetime.strptime(scenario.date, '%d/%m/%Y') if scenario.date else None
        intValues = {
            'date': curDate.toordinal() if curDate else None
        }

        strValues = {
            'name'       : scenario.name,
            'description': scenario.description
        }

        id = self.database.insert(self.DATABASE_TABLE, intValues)
        scenario.id = id

        self.database.insert_translate(strValues, scenario.lang, id, self.TYPE)

        # Create node for tree structure
        node = NodeObject(None, scenario.name, nodeParentId, scenario)
        nodeId = self.treeDAO.insert_node(node, contextType)

        for location in scenario.locations:
            LocationDAO().create(location, nodeId, contextType)

        for spell in scenario.spells:
            SpellDAO().create(spell, nodeId, contextType)

        for ability in scenario.abilities:
            AbilityDAO().create(ability, nodeId, contextType)

        for effect in scenario.effects:
            EffectDAO().create(effect, nodeId, contextType)

        for character in scenario.party:
            PartyCharacterDAO().create(character, nodeId, contextType)

        return id


    def update(self, scenario: Scenario):
        """
        Update spell in database
        :param scenario: Spell object with new data
        """
        intValues = {
            'date': scenario.date.toordinal() if scenario.date else None
        }

        strValues = {
            'name'       : scenario.name,
            'description': scenario.description
        }

        self.database.update(self.DATABASE_TABLE, scenario.id, intValues)
        self.database.update_translate(strValues, scenario.lang, scenario.id, self.TYPE)


    def delete(self, scenario_id: int):
        """
        Delete spell from database and all his translates
        :param scenario_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, scenario_id)
        self.database.delete_where('translates',
                                   {'target_id': scenario_id, 'type': ObjectType.SCENARIO})


    def get(self, scenario_id: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Scenario:
        """
        Get spell from database
        :param scenario_id: id of spell
        :param lang: lang of spell
        :return: Monster object
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        data = dict(self.database.select(self.DATABASE_TABLE, {'ID': scenario_id})[0])
        tr_data = dict(self.database.select_translate(scenario_id, self.TYPE.value,
                                                      lang))

        scenarioDate = date.fromordinal(data.get('date')) if data.get('date') else None
        scenario = Scenario(data.get('ID'), lang, tr_data.get('name', ''),
                            tr_data.get('description', ''), scenarioDate)

        if nodeId and contextType:
            children = self.treeDAO.get_children_objects(nodeId, contextType)

            abilities = []
            spells = []
            effects = []
            locations = []
            partyCharacters = []

            for child in children:
                if child.object.object_type is ObjectType.ABILITY:
                    ability = AbilityDAO().get(child.object.id, None, child.id, contextType)
                    abilities.append(ability)
                elif child.object.object_type is ObjectType.SPELL:
                    spell = SpellDAO().get(child.object.id, None, child.id, contextType)
                    spells.append(spell)
                elif child.object.object_type is ObjectType.EFFECT:
                    effect = EffectDAO().get(child.object.id, None, child.id, contextType)
                    effects.append(effect)
                elif child.object.object_type is ObjectType.LOCATION:
                    location = LocationDAO().get(child.object.id, None, child.id, contextType)
                    locations.append(location)

                elif child.object.object_type is ObjectType.CHARACTER:
                    character = CharacterDAO().get(child.object.id, None, child.id, contextType)
                    partyCharacter = PartyCharacterDAO().get(character.id)

                    if not partyCharacter:
                        partyCharacter = PartyCharacter()

                    partyCharacter.character = character
                    partyCharacters.append(partyCharacter)

            # Search non connected party character
            chars = self.database.select('PartyCharacter', {'scenario_id': scenario_id})
            for char in chars:
                if char['character_id'] is None:
                    partyCharacters.append(PartyCharacterDAO().get_by_id(char['ID']))

            scenario.spells = spells
            scenario.abilities = abilities
            scenario.effects = effects
            scenario.locations = locations
            scenario.party = partyCharacters

        return scenario


    def get_all(self, lang=None) -> list:
        """
        Get list of all spells from database, only one lang
        :param lang: lang code
        :return: list of Spells
        """
        if lang is None:  # TODO : default lang
            lang = 'cs'
        lines = self.database.select_all(self.DATABASE_TABLE)
        items = []
        for line in lines:
            item = self.get(line['ID'], lang)
            items.append(item)
        return items
