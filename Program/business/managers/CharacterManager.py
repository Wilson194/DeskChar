from structure.character.Character import Character
from structure.enums.ObjectType import ObjectType


class CharacterManager:
    def __init__(self):
        from data.DAO.CharacterDAO import CharacterDAO
        self.DAO = CharacterDAO()


    def create(self, character: Character, nodeParentId: int = None, contextType: ObjectType = None) -> int:
        return self.DAO.create(character, nodeParentId, contextType)


    def update_character(self, character: Character):
        return self.DAO.update(character)


    def delete(self, characterId: int):
        return self.DAO.delete(characterId)


    def get(self, characterId: int, lang: str = None, nodeId: int = None, contextType: ObjectType = None) -> Character:
        return self.DAO.get(characterId, lang, nodeId, contextType)


    def get_all(self, lang: str = None) -> list:
        return self.DAO.get_all(lang)


    def create_empty(self, lang) -> Character:
        character = Character(None, lang)
        id = self.DAO.create(character)
        character.id = id

        return character
