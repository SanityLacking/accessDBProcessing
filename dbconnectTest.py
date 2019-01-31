import pyodbc
from os.path import abspath
[x for x in pyodbc.drivers() if x.startswith("Microsoft Access Driver")] # check i have the drivers for pyodbc installed
driver=""
from optparse import OptionParser
usage=''
parser = OptionParser(usage=usage)
(options, args) = parser.parse_args()


if len(args) != 1:
        parser.error('dbfile argument required')

if args[0].endswith('.accdb'):
    driver = 'Microsoft Access Driver (*.mdb, *.accdb)'
else:
    driver = 'Microsoft Access Driver (*.mdb, *.accdb)'
    # driver = 'Microsoft Access Driver (*.mdb)'
global CNXNSTRING
CNXNSTRING = 'DRIVER={%s};DBQ=%s;ExtendedAnsiSQL=1' % (driver, abspath(args[0]))
print(CNXNSTRING)
# conn_str = (
#     r'DRIVER={Microsoft Access Driver (*.mbd, *.accdb)};'
#     r'DBQ=empty.accdb'
# )
cnxn = pyodbc.connect(CNXNSTRING)
crsr = cnxn.cursor()

for table_info in crsr.tables(tableType='TABLE'):
   print(table_info.table_name)

crsr.execute("select * from [Raw Logging Data] where Easting is NULL or  Northing is NULL ")
row = crsr.fetchall()
if row: 
    print(row)
    