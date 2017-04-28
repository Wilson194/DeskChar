import sqlite3


def create_backup():
    con = sqlite3.connect('test.db')

    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON;')
    con.execute('PRAGMA ENCODING = `UTF-8`')

    cur = con.cursor()
    cur.execute("SELECT * FROM sqlite_master WHERE name != 'Settings'")

    tablesCreate = []
    tablesNames = []
    for row in cur:
        if row['sql']:
            if row['name'] != 'sqlite_sequence':
                tablesCreate.append(row['sql'] + ';')
            tablesNames.append(row['name'])

    tableInsert = []
    for name in tablesNames:
        data = cur.execute('SELECT * FROM {}'.format(name))

        for one in data:
            one = dict(one)
            # print([str(i) for i in list(one.values())])

            sql = 'INSERT INTO "{}" VALUES ({});'.format(name, ','.join([str(i) for i in list(one.values())]))
            tableInsert.append(sql)

    tableDelete = []
    for name in tablesNames:
        if name == 'sqlite_sequence':
            tableDelete.append('DELETE FROM {};'.format(name))
        else:
            tableDelete.append('DROP TABLE {};'.format(name))

    with open('text.txt', 'w') as f:
        for delete in tableDelete:
            f.write(delete)
            f.write('\n')

        for create in tablesCreate:
            f.write(create)
            f.write('\n')

        for insert in tableInsert:
            f.write(insert)
            f.write('\n')


def load_backup():
    con = sqlite3.connect('test.db')

    con.row_factory = sqlite3.Row
    # con.execute('PRAGMA foreign_keys = ON;')
    con.execute('PRAGMA ENCODING = `UTF-8`')
    con.isolation_level = None

    cur = con.cursor()

    with open('text.txt', 'r', encoding='UTF-8') as f:
        sql = f.read()

    # cur.execute('BEGIN TRANSACTION')
    for one in sql.split(';'):
        if not 'Settings' in one:
            cur.execute(one)


def dump():
    con = sqlite3.connect('test.db')
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

    with open('text.txt', 'w', encoding='UTF-8') as f:
        f.write('BEGIN TRANSACTION;\n')
        f.write('\n'.join(delete))
        f.write(data[18:])


# dump()
# create_backup()
# load_backup()



from data.drdFile.drdFile import DrdFile


a = DrdFile()
# a.create('C:/Users/horac/Desktop/test.drd')
a.open('C:/Users/horac/Desktop/Patalie.drd')