from structure.enums.ObjectType import ObjectType


class TabWidgetManager:
    """
    Manager for Tab widget
    """


    def __init__(self):
        pass


    def get_data(self, target_id: int, target_type: ObjectType) -> list:
        """
        Return list of objects, objects are for one ID but all langs
        :param target_id: id of object
        :param target_type: Type of object
        :return: List of object
        """
        data = []
        langs = target_type.instance().DAO()().get_languages(target_id)
        for lang in langs:
            object = target_type.instance().DAO()().get(target_id, lang)
            data.append(object)

        return data


    def get_layout(self, target_type: ObjectType, parent):
        """
        Get layout for targget type
        :param target_type: Type of object
        :param parent: parent object for creating leyout
        :return: Layout for target object
        """
        return target_type.instance().layout()(parent)


    def get_empty_object(self, target_type: ObjectType, id: int, lang: str) -> object:
        """
        Create empty object for id and lang
        :param target_type: Type ob object
        :param id: id of object
        :param lang: lang code of object
        :return: New empty object
        """
        return target_type.instance()(id, lang)
