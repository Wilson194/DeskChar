from abc import ABC, abstractclassmethod


class Node(ABC):
    def __init__(self, id: int=None, name: str=None, parent_id: int=None):
        self.__id = id
        self.__name = name
        self.__parent_id = parent_id

        self.__children = []


    @property
    def children(self):
        return self.__children


    @children.setter
    def children(self, value):
        self.__children = value

    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def parent_id(self):
        return self.__parent_id


    @parent_id.setter
    def parent_id(self, value):
        self.__parent_id = value
