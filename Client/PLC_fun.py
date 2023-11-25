from Parameters import *
import snap7

def plc_connect():
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)
    plc_info = plc.get_cpu_info()
    print(f'Module Type: {plc_info.ModuleTypeName}')
    state = plc.get_cpu_state()
    print(f'State: {state}')
    return plc

def plc_write(plc, database, start_address, type, data):
    match type:
        case 4:
            buffe = bytearray(type)
            snap7.util.set_real(buffe, 0, data)
        case 1:
            buffe = plc.db_read(database, start_address, type)
            snap7.util.set_bool(buffe, 0, 0, data)
    plc.db_write(database, start_address, buffe)
    return 0