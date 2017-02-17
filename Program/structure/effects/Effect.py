from structure.general.Object import Object


class Effect(Object):
    def __init__(self, id: int = None, lang: str = None, name: str = None,
                 description: str = None, target_id: int = None,
                 target_type: str = None):
        super().__init__(id, lang, name, description)

        self.__target_id = target_id
        self.__target_type = target_type

        self.__modifiers = []


    def __name__(self):
        names = super().__name__()
        names.append('Effect')
        return names


    @property
    def target_id(self):
        return self.__target_id


    @target_id.setter
    def target_id(self, value: int):
        self.__target_id = value


    @property
    def target_type(self):
        return self.__target_type


    @target_type.setter
    def target_type(self, value: str):
        self.__target_type = value


    @property
    def modifiers(self):
        return self.__modifiers


    @modifiers.setter
    def modifiers(self, value: list):
        self.__modifiers = value


    def add_modifier(self, modifier):
        self.__modifiers.append(modifier)


    def __eq__(self, other):
        if not isinstance(other, Effect):
            return False

        if super().__eq__(other) \
                and self.__target_id == other.target_id \
                and self.__target_type == other.target_type \
                and self.__modifiers == other.modifiers:
            return True

        return False
