import sqlite3
from structure.general.Singleton import Singleton


class Database(metaclass=Singleton):
    """
    Class for hanling all database commands
    """


    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('PRAGMA foreign_keys = ON;')
        self.connection.execute('PRAGMA ENCODING = `UTF-8`')
        self.cursor = self.connection.cursor()
        self.__sql_buffer = ""
        self.__sql_many_state = False


    def set_many(self, value):
        self.__sql_many_state = value


    def create_table(self, name: str, columns=None, foreigns=None):
        """
        Create table in database
        :param name: name of table
        :param columns: list of object Column
        :param foreigns: list of object Foreign
        """

        if foreigns is None:
            foreigns = []

        if columns is None:
            columns = []

        sql = 'CREATE TABLE ' + name + ' ('

        for column in columns:
            sql += column.to_sql() + ','

        for foreign in foreigns:
            sql += foreign.to_sql()
            sql += ','

        sql = sql[:-1] + ');'

        self.cursor.execute(sql)


    def truncate_table(self, table_name: str):
        """
        Truncate table
        :param table_name: table name
        """
        sql = 'DELETE FROM ' + table_name
        self.cursor.execute(sql)


    def add_column(self, table_name: str, column):
        """
        Add column to table
        :param table_name: table name
        :param column: Column object
        """
        sql = 'ALTER TABLE ' + table_name + ' ADD COLUMN ' + column.to_sql()
        self.cursor.execute(sql)


    def drop_table(self, table_name: str):
        """
        Drop data from table
        :param table_name: name of table
        """
        sql = 'DROP TABLE ' + table_name
        self.cursor.execute(sql)


    def insert(self, table_name: str, values: dict, not_many=False) -> int:
        """
        Insert data into table
        :param table_name: name of table
        :param values: dictionary of pairs (name,value)
        :return: autoincrement ID
        """
        sql = 'INSERT INTO ' + table_name + '('
        sql += array_to_string(values.keys(), ', ')
        sql += ') VALUES ('
        sql += array_to_string(values.values(), ', ')
        sql += ');'

        if self.__sql_many_state and not_many is False:
            self.__sql_buffer += sql
        else:
            self.cursor.execute(sql)
            self.connection.commit()

        return self.cursor.lastrowid


    def insert_many_execute(self):
        self.connection.isolation_level = None
        self.cursor.execute('BEGIN TRANSACTION')
        for i in self.__sql_buffer.split(';'):
            self.cursor.execute(i)
        self.__sql_buffer = ""
        self.cursor.execute('COMMIT')


    def insert_null(self, table_name: str) -> int:
        """
        insert only null to get autoincrement
        :param table_name: name of table
        :return: autoincrement ID
        """
        sql = 'INSERT INTO ' + table_name + '(ID) VALUES(NULL)'
        self.cursor.execute(sql)
        self.connection.commit()

        return self.cursor.lastrowid


    def update(self, table_name: str, id: int, values: dict, not_many=False):
        """
        Update data in database
        :param table_name: name of table
        :param id: id of column in table
        :param values: dictionry of values (name,value)
        """
        sql = 'UPDATE ' + table_name + ' SET '
        for key, value in values.items():
            sql += key + ' = '
            if type(value) is str or type(value) is bytes:
                value = value.replace("'", "''")
                sql += "'" + value + "'"
            elif value is None:
                sql += 'null'
            else:
                sql += str(value)
            if not key == list(values.keys())[-1]:
                sql += ', '
        sql += ' WHERE ID = ' + str(id)
        sql += ';'
        if self.__sql_many_state and not_many is False:
            self.__sql_buffer += sql
        else:
            self.cursor.execute(sql)
            self.connection.commit()


    def select_all(self, table_name: str) -> list:
        """
        Select all data from table
        :param table_name: name of table
        :return: list of sqlite3.Row
        """
        sql = 'SELECT * FROM ' + table_name
        return self.cursor.execute(sql).fetchall()


    def select(self, table_name: str, row_filter: dict) -> list:
        """
        Select all data filtred by filter, can compare only =
        :param table_name: name of table
        :param row_filter: dictionary of filter (name,value)
        :return: list of sqlite3.Row
        """
        sql = 'SELECT * FROM ' + table_name + ' WHERE '
        for key, value in row_filter.items():
            if type(value) is tuple:
                sql += key + ' '
                sql += value[0] + ' '
                sql += "'" + value[1] + "'"
            elif type(value) == str:
                sql += key + ' = '
                sql += "'" + value + "'"
            elif value is None:
                sql += key + ' ISNULL '
            else:
                sql += key + ' = '
                sql += str(value)
            if not key == list(row_filter.keys())[-1]:
                sql += ' AND '
        return self.cursor.execute(sql).fetchall()


    def select_translate(self, target_id, type, lang) -> dict:
        """
        Select all data from translate table for target
        :param target_id: id of target object
        :param type: type of target object
        :param lang: lang
        :return: dictionary of (name, value)
        """
        sql = "SELECT * FROM translates WHERE target_id = " + str(target_id)
        sql += " AND type = '" + str(type) + "'"
        sql += " AND lang = '" + lang + "'"

        result = self.cursor.execute(sql).fetchall()

        data = {}
        for row in result:
            data[row['name']] = row['value']

        return data


    def delete(self, table_name: str, ID: int):
        """
        Delete column from database by ID
        :param table_name: name of table
        :param ID: ID which you want to delete
        """
        sql = 'DELETE FROM ' + table_name + ' WHERE ID = ' + str(ID)

        self.cursor.execute(sql)
        self.connection.commit()


    def delete_where(self, table_name: str, statements: dict):
        """
        Delete columns from database by statements, can compare only =
        :param table_name: name of table
        :param statements: dictionary of filer (name, value)
        :return:
        """
        sql = 'DELETE FROM ' + table_name + ' WHERE '
        for key, value in statements.items():
            if type(value) == str:
                sql += key + " = '" + value + "'"
            else:
                sql += key + " = " + str(value)
            sql += ' AND '
        sql = sql[:-4]
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            pass


class Column:
    """
    Class for handling column in database
    """
    data_types = ['INTEGER', 'TEXT', 'REAL', 'NUMERIC', 'DATE', 'DATETIME']


    def __init__(self, name, value_type, primary=False, unique=False,
                 autoincrement=False, not_null=False):
        self.name = name

        if value_type not in self.data_types:
            raise ValueError(
                'Bad type of column, use one of these: ' + array_to_string(
                    self.data_types, ', '))

        self.value_type = value_type
        self.primary = primary
        self.autoincrement = autoincrement
        self.unique = unique
        self.not_null = not_null


    def to_sql(self) -> str:
        """
        Convert column to sql statement
        :return: sql string
        """
        sql = self.name + ' ' + self.value_type + ' '

        if self.primary:
            sql += 'PRIMARY KEY' + ' '

        if self.unique:
            sql += 'UNIQUE' + ' '

        if self.autoincrement:
            sql += 'AUTOINCREMENT' + ' '

        if self.not_null:
            sql += 'NOT NULL' + ' '

        return sql


class Foreign:
    """
    Class for handling foreign keys for database
    """


    def __init__(self, column, target_table, target_column, delete=None):
        self.column = column
        self.target_table = target_table
        self.target_column = target_column
        self.delete = delete


    def to_sql(self) -> str:
        """
        Convert class to sql statement
        :return: sql string
        """
        sql = 'FOREIGN KEY(' + self.column
        sql += ') REFERENCES ' + self.target_table
        sql += '(' + self.target_column + ')'
        if self.delete == 'CASCADE':
            sql += ' ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED'
        return sql


def array_to_string(array: list, separator: str) -> str:
    """
    Convert array to string, separate by separator
    :param array: given array
    :param separator: separator
    :return: converted array to string
    """
    string = ''
    for value in array:
        if type(value) == str:
            value = value.replace("'", "''")
            string += "'" + value + "'"
        elif value is None:
            string += 'null'
        else:
            string += str(value)
        string += separator

    string = string[:-len(separator)]

    return string
