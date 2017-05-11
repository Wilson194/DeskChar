import sqlite3
import zipfile
import os
import shutil
import glob


class DrdFile:
    def __init__(self):
        pass


    def create(self, path, database: str = 'file::memory:?cache=shared'):
        """
        Create a file with whole program backup
        :param path: 
        :param database: 
        :return: 
        """
        self.__dump_db(database)
        if os.path.basename(path).endswith('.drd'):
            path = path
        else:
            path = os.path.join(os.path.dirname(path), os.path.basename(path) + '.drd')

        with zipfile.ZipFile(path, 'w') as myZip:
            myZip.write('database')

            for file in os.listdir('resources/maps/'):
                myZip.write('resources/maps/{}'.format(file), 'maps/{}'.format(file), zipfile.ZIP_DEFLATED)

        os.remove('database')


    def open(self, path):
        """
        Load new data to program
        :param path: 
        :return: 
        """
        if not os.path.isdir('temp'):
            os.mkdir('temp', 777)

        if os.path.isdir('resources/maps'):
            shutil.rmtree('resources/maps')
        os.mkdir('resources/maps')

        with zipfile.ZipFile(path) as myZip:
            myZip.extractall('temp')

        self._load_db('temp/database')

        for filename in glob.glob(os.path.join('temp/maps/*.*')):
            shutil.copy2(filename, 'resources/maps/')

        shutil.rmtree('temp')


    def __dump_db(self, database: str = "file::memory:?cache=shared"):
        """
        Dump whole database to temp file. Setting table is skipped and structure of tables are included.
        :param database: name of database, that you want to dump        
        """
        con = sqlite3.connect(database, uri=True)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA ENCODING = `UTF-8`')
        data = '\n'.join(con.iterdump())

        cur = con.cursor()
        names = cur.execute("SELECT * FROM sqlite_master WHERE name != 'Settings'")

        delete = []
        for one in names:
            if one['name'] == 'sqlite_sequence':
                delete.append('DELETE FROM `{}`;'.format(one['name']))
            else:
                delete.append('DROP TABLE IF EXISTS `{}`;'.format(one['name']))

        with open('database', 'w', encoding='UTF-8') as f:
            f.write('BEGIN TRANSACTION;\n')
            f.write('\n'.join(delete))
            f.write(data[18:])


    def _load_db(self, path, database: str = "file::memory:?cache=shared"):
        """
        Delete current database and load new database from backup file
        :param path: path, where backup file is stored
        :param database: target database
        """
        con = sqlite3.connect(database, uri=True)

        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys = OFF;')
        con.execute('PRAGMA ENCODING = `UTF-8`')
        con.isolation_level = None

        cur = con.cursor()

        with open(path, 'r', encoding='UTF-8') as f:
            sql = f.read()

        # cur.execute('BEGIN TRANSACTION')
        for one in sql.split(';'):
            if not 'Settings' in one:
                cur.execute(one)
        con.execute('PRAGMA foreign_keys = ON;')
