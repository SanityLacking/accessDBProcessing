import pyodbc
from os.path import abspath
driver=""

def dbOpen(name):
    [x for x in pyodbc.drivers() if x.startswith("Microsoft Access Driver")] # check i have the drivers for pyodbc installed
    if len(name) <= 0:
        return 'dbfile argument required'

    if name.endswith('.accdb'):
        driver = 'Microsoft Access Driver (*.mdb, *.accdb)'
    else:
        driver = 'Microsoft Access Driver (*.mdb, *.accdb)'
        # driver = 'Microsoft Access Driver (*.mdb)'
    global CNXNSTRING
    CNXNSTRING = 'DRIVER={%s};DBQ=%s;ExtendedAnsiSQL=1' % (driver, abspath(name))
    print(CNXNSTRING)
    # conn_str = (
    #     r'DRIVER={Microsoft Access Driver (*.mbd, *.accdb)};'
    #     r'DBQ=empty.accdb'
    # )
    print(CNXNSTRING)
    cnxn = pyodbc.connect(CNXNSTRING)
    crsr = cnxn.cursor()    
    return crsr

#returns list of tables for db cursor 
def listTables(cursor):
    tableList = cursor.tables(tableType='TABLE')
    # for table_info in cursor.tables(tableType='TABLE'):
    #     print(table_info.table_name)
    return tableList

def execute(cursor, str):
    cursor.execute(str)
    return cursor.fetchall()

def executeCursor(cursor, str):
    cursor.execute(str)
    return cursor
    
def fetchOne(cursor, tableName):
    cursor.execute("select * from ["+tableName+"]")
    row = cursor.fetchone()
    if row: 
        return row
    else: return ""
