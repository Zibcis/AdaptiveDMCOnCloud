import snap7.util

from Client.PLC_fun import *
from RegulatorParametersContainer import *
# Łączenie ze sterownikiem
plc = plc_connect()

# Wypełnianie database

## Wypełnianie k
read = plc.db_read(GLOBALDATA_DB, 82, BOOL_SIZE)
print(snap7.util.get_bool(read, 0, 5))
