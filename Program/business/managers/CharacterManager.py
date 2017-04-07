from structure.character.Character import Character
from structure.spells.Spell import Spell


class CharacterManager:
    def __init__(self):
        from data.DAO.CharacterDAO import CharacterDAO
        self.DAO = CharacterDAO()


    def update_character(self, character: Character):
        self.DAO.update(character)


    def create_empty(self, lang):
        character = Character(None, lang)
        id = self.DAO.create(character)
        character.id = id

        return character
