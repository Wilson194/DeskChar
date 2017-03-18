from data.DAO.DAO import DAO
from data.DAO.interface.IModifierDAO import IModifierDAO
from data.database.ObjectDatabase import ObjectDatabase
from structure.effects.Modifier import Modifier


class ModifierDAO(DAO, IModifierDAO):
    def create(self, modifier: Modifier) -> int:
        return ObjectDatabase(self.DATABASE_DRIVER).insert_object(modifier)


    def update(self, modifier: Modifier) -> None:
        pass


    def delete(self, modifier_id: int) -> None:
        pass


    def get(self, modifier_id: int) -> Modifier:
        pass


    def get_all(self) -> list:
        pass
