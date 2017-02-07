import sqlite3


class Database:
    def __init__(self, database_name):
        connection = sqlite3.connect(database_name)
        connection.row_factory = sqlite3.Row
        self.cursor = connection.cursor()


    def create_table(self, name: str, columns=None, foreigns=None):
        if columns is None:
            columns = []

        if foreigns is None:
            foreigns = []

        sql = 'CREATE TABLE ' + name + ' ('

        for column in columns:
            sql += column.to_sql() + ','

        for foreign in foreigns:
            sql += foreign.to_sql()
            sql += ','

        sql = sql[:-1] + ');'

        self.cursor.execute(sql)


    def truncate_table(self, table_name: str):
        sql = 'DELETE FROM ' + table_name
        self.cursor.execute(sql)


    def add_column(self, table_name: str, column):
        sql = 'ALTER TABLE ' + table_name + ' ADD COLUMN ' + column.to_sql()
        self.cursor.execute(sql)


    def drop_table(self, table_name: str):
        sql = 'DROP TABLE ' + table_name
        self.cursor.execute(sql)


    def insert(self, table_name: str, values: dict):
        sql = 'INSERT INTO ' + table_name + '('
        sql += array_to_string(values.keys(), ', ')
        sql += ') VALUES ('
        sql += array_to_string(values.values(), ', ')
        sql += ');'

        self.cursor.execute(sql)


    def select_all(self, table_name: str):
        sql = 'SELECT * FROM ' + table_name
        return self.cursor.execute(sql).fetchall()


    def select(self, table_name, row_filter: dict):
        sql = 'SELECT * FROM ' + table_name + ' WHERE '
        for key, value in row_filter.items():
            sql += key + ' = '
            if type(value) == str:
                sql += "'" + value + "'"
            else:
                sql += str(value)
            if not key == list(row_filter.keys())[-1]:
                sql += ' AND '
        return self.cursor.execute(sql).fetchall()


    def delete(self, table_name: str, ID: int):
        sql = 'DELETE FROM ' + table_name + ' WHERE ID = ' + str(ID)

        self.cursor.execute(sql)


class Column:
    data_types = ['INTEGER', 'TEXT', 'REAL', 'NUMERIC', 'DATE', 'DATETIME']


    def __init__(self, name, value_type, primary=False, unique=False, autoincrement=False, not_null=False):
        self.name = name

        if value_type not in self.data_types:
            raise ValueError('Bad type of column, use one of these: ' + array_to_string(self.data_types, ', '))

        self.value_type = value_type
        self.primary = primary
        self.autoincrement = autoincrement
        self.unique = unique
        self.not_null = not_null


    def to_sql(self):
        sql = self.name + ' ' + self.value_type + ' '

        if self.autoincrement:
            sql += 'AUTO INCREMENT' + ' '

        if self.primary:
            sql += 'PRIMARY KEY' + ' '

        if self.unique:
            sql += 'UNIQUE' + ' '

        if self.not_null:
            sql += 'NOT NULL' + ' '

        return sql


def array_to_string(array, separator):
    string = ''
    for value in array:
        if type(value) == str:
            string += "'" + value + "'"
        else:
            string += str(value)
        string += separator

    string = string[:-len(separator)]

    return string


class Foreign:
    def __init__(self, column, target_table, target_column):
        self.column = column
        self.target_table = target_table
        self.target_column = target_column


    def to_sql(self):
        sql = 'FOREIGN KEY(' + self.column
        sql += ') REFERENCES ' + self.target_table
        sql += '(' + self.target_column + ')'
        return sql
