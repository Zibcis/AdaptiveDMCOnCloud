from Client.PLC_fun import *
from RegulatorParametersContainer import *

# Łączenie ze sterownikiem
plc = plc_connect()

# Wypełnianie database

## Wypełnianie k

for i in range(0, 7):
    plc_write(plc, ADAPTIVE_PARAM_DB, ke_ADDRESS + i*REAL_SIZE, REAL_SIZE, ke[i])
    plc_write(plc, ADAPTIVE_PARAM_DB, T_ADDRESS + i*INT_SIZE, INT_SIZE, T[i])

for i in range(0, 7):
    for j in range(0, 58):
        plc_write(plc, ADAPTIVE_PARAM_DB, Ku_ADDRESS + int(58*i*REAL_SIZE) + int(j*REAL_SIZE), REAL_SIZE, Ku[i][j])
