from datetime import date

from data.DAO.LocationDAO import LocationDAO
from data.DAO.PartyCharacterDAO import PartyCharacterDAO
from data.DAO.PlayerTreeDAO import PlayerTreeDAO
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


class ScenarioDAO(DAO):
    DATABASE_TABLE = 'Scenario'
    DATABASE_DRIVER = 'test.db'
    TYPE = ObjectType.SCENARIO


    def __init__(self):
        self.database = Database(self.DATABASE_DRIVER)


    def create(self, scenario: Scenario) -> int:
        """
        Create new spell in database
        :param scenario: Spell object
        :return: id of autoincrement
        """
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(scenario)


    def update(self, scenario: Scenario):
        """
        Update spell in database
        :param scenario: Spell object with new data
        """
        ObjectDatabase(self.DATABASE_DRIVER).update_object(scenario)


    def delete(self, scenario_id: int):
        """
        Delete spell from database and all his translates
        :param scenario_id: id of spell
        """
        self.database.delete(self.DATABASE_TABLE, scenario_id)
        self.database.delete_where('translates',
                                   {'target_id': scenario_id, 'type': ObjectType.SCENARIO})


    def get(self, scenario_id: int, lang: str = None) -> Scenario:
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

        # Create party
        party = PlayerTreeDAO().get_children_objects(ObjectType.CHARACTER, scenario, direct=True)
        partyCharacters = []
        partyIds = []

        for member in party:
            partyIds.append(member.id)
            real = PartyCharacterDAO().get(member.id)
            if real:
                partyCharacters.append(real)
            else:
                partyCharacter = PartyCharacter()
                partyCharacter.character = member
                partyCharacters.append(partyCharacter)

        scenario.party = partyCharacters


        # Create npc
        data = PlayerTreeDAO().get_children_objects(ObjectType.CHARACTER, scenario)
        npc = []
        for one in data:
            if one.id not in partyIds:
                npc.append(one)

        scenario.npc = npc


        # Create locations
        locations = PlayerTreeDAO().get_children_objects(ObjectType.LOCATION, scenario, direct=True)
        scenario.locations = locations

        spells = PlayerTreeDAO().get_children_objects(ObjectType.SPELL, scenario, direct=True)
        scenario.spells = spells

        abilities = PlayerTreeDAO().get_children_objects(ObjectType.ABILITY, scenario, direct=True)
        scenario.abilities = abilities

        effects = PlayerTreeDAO().get_children_objects(ObjectType.EFFECT, scenario, direct=True)
        scenario.abilities = effects

        items = PlayerTreeDAO().get_children_objects(ObjectType.ITEM, scenario, direct=True)

        for item in items:
            if isinstance(item, Armor):
                scenario.addArmor(item)
            elif isinstance(item, Money):
                scenario.addMoney(item)
            elif isinstance(item, Container):
                scenario.addContainer(item)
            elif isinstance(item, MeleeWeapon):
                scenario.addMeleeWeapon(item)
            elif isinstance(item, RangeWeapon):
                scenario.addRangedWeapon(item)
            elif isinstance(item, ThrowableWeapon):
                scenario.addThrowableWeapon(item)
            else:
                scenario.addItem(item)

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
