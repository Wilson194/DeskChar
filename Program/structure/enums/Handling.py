from structure.enums.AutoNumber import AutoNumber


class Handling(AutoNumber):
    ONE_HANDED = ()
    TWO_HANDED = ()


    def by_name(self, name: str):
        name = name.upper()
        if name == 'ONE_HANDED':
            return self.ONE_HANDED
        if name == 'TWO_HANDED':
            return self.TWO_HANDED

        return None

    def xml_name(self):
        return self.name