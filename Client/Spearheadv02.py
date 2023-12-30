import socket
import struct
import time
import snap7
from Client.Parameters import *
from Client.Picker import *
from Client.PLC_fun import *

#Potrzebne dane               
i = 0
Samples = []
Time = []
TC = 1.84
k = 0
data = []
only_one_time = [0, 0, 0, 0]
send_mess = 0
u_i = 86

# Łączenie ze sterownikieniem
plc = plc_connect()
# Główna pętla
while True:
    State = int.from_bytes(plc.db_read(GLOBALDATA_DB, JUMP_ADDRESS, INT_SIZE), "big")
    match State:
        case 0:     # Inicjalizacja - dojście do wartości pod zadaną
            if only_one_time[0] == 0:
                print("Rozpoczynam proces inicjalizacji")
                data.append(1)
                data_size = len(data)
                msg = struct.pack('<{}f'.format(data_size), *data)
                data = []
                s = socket.socket()
                s.connect((IP_serv, port))
                s.send(msg)
                send_mess = 1
                only_one_time[0] = 1
        case 1:     # Skok w otoczeniu punktu pracy
            if only_one_time[1] == 0:
                print("Wykonania skoku w otoczeniu punktu pracy")
                data.append(2)
                data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE), 0))
                data_size = len(data)
                msg = struct.pack('<{}f'.format(data_size), *data)
                data = []
                s = socket.socket()
                s.connect((IP_serv, port))
                s.send(msg)
                send_mess = 1
                only_one_time[1] = 1
            else:           #pobieranie próbek - na razie bez doboru wartości skoku
                plc_write(plc, GLOBALDATA_DB, ST_HOLD_ADDRESS, BOOL_SIZE, 1)
                Samples, Time, Err = picker(plc, TC)
                if Err == 0:
                    data.append(3)
                    for x in Samples:
                        data.append(x)
                    data.append(9999)
                    for t in Time:
                        data.append(t)
                    print(data)
                    Samples = []
                    Time = []
                    data_size = len(data)
                    msg = struct.pack('<{}f'.format(data_size), *data)
                    data = []
                    s = socket.socket()
                    s.connect((IP_serv, port))
                    s.send(msg)
                    send_mess = 1
                #else:   do zrobienia - mechanizm doboru wartości skoku
        case 2:     ## Wyliczenie sterowania
            plc_write(plc, GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE, u_i)
            Start = time.time()
            data.append(4)
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE), 0))
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_ADDRESS, REAL_SIZE), 0))
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_zad_ADDRESSS, REAL_SIZE), 0))
            data_size = len(data)
            msg = struct.pack('<{}f'.format(data_size), *data)
            data = []
            s = socket.socket()
            s.connect((IP_serv, port))
            s.send(msg)
            send_mess = 1
            #only_one_time[2] = 1  Nie wiem czy potrzebne - chyba nie
        case 3:  ## Wyliczenie sterowania
            plc_write(plc, GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE, u_i)
            Start = time.time()
            data.append(4)
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE), 0))
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_ADDRESS, REAL_SIZE), 0))
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_zad_ADDRESSS, REAL_SIZE), 0))
            data_size = len(data)
            msg = struct.pack('<{}f'.format(data_size), *data)
            data = []
            s = socket.socket()
            s.connect((IP_serv, port))
            s.send(msg)
            only_one_time[2] = 0
            send_mess = 1
            # only_one_time[2] = 1  Nie wiem czy potrzebne - chyba nie
        case 4:
            if only_one_time[2] == 0:
                data.append(2)
                data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE), 0))
                data_size = len(data)
                msg = struct.pack('<{}f'.format(data_size), *data)
                data = []
                s = socket.socket()
                s.connect((IP_serv, port))
                s.send(msg)
                send_mess = 1
                only_one_time[2] = 1
            else:  # pobieranie próbek - na razie bez doboru wartości skoku
                plc_write(plc, GLOBALDATA_DB, ST_HOLD_ADDRESS, BOOL_SIZE, 1)
                Samples, Time, Err = picker(plc, TC)
                if Err == 0:
                    data.append(3)
                    for x in Samples:
                        data.append(x)
                    data.append(9999)
                    for t in Time:
                        data.append(t)
                    data_size = len(data)
                    Samples = []
                    Time = []
                    msg = struct.pack('<{}f'.format(data_size), *data)
                    data = []
                    s = socket.socket()
                    s.connect((IP_serv, port))
                    s.send(msg)
                    send_mess = 1
        case 5:
            plc_write(plc, GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE, u_i)
            print(f"Wartość sterowania: {u_i}")
            Start = time.time()
            data.append(4)
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE), 0))
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_ADDRESS, REAL_SIZE), 0))
            data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_zad_ADDRESSS, REAL_SIZE), 0))
            data_size = len(data)
            msg = struct.pack('<{}f'.format(data_size), *data)
            data = []
            s = socket.socket()
            s.connect((IP_serv, port))
            s.send(msg)
            send_mess = 1
        case 7:
            read = plc.db_read(GLOBALDATA_DB, 82, BOOL_SIZE)
            if  snap7.util.get_bool(read, 0, 5):
                plc_write(plc, GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE, u_i)
                print(f"Wartość sterowania: {u_i}")
                Start = time.time()
                data.append(5)
                data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE), 0))
                data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_ADDRESS, REAL_SIZE), 0))
                data.append(snap7.util.get_real(plc.db_read(GLOBALDATA_DB, Thout_zad_ADDRESSS, REAL_SIZE), 0))
                data_size = len(data)
                msg = struct.pack('<{}f'.format(data_size), *data)
                data = []
                s = socket.socket()
                s.connect((IP_serv, port))
                s.send(msg)
                send_mess = 1

    if State != 65535 and send_mess == 1:
        time.sleep(0.5)
        returnmsg = s.recv(50000)
        send_mess=0
        rmsg_size = len(returnmsg)/4.0
        trmsg_size = int(rmsg_size)
        returndata = struct.unpack('<{}f'.format(trmsg_size),returnmsg)
        returnmsg=[]
        match returndata[0]:
            case 10:
                #plc_write(plc, GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE, returndata[1])
                plc_write(plc, GLOBALDATA_DB, Power_of_heater_ADDRESS, REAL_SIZE, returndata[1])
                s.close()
            case 20:
                plc_write(plc, GLOBALDATA_DB, Valve_oppening_degree_ADDRESS, REAL_SIZE, returndata[1])
                print(f"Wartość skoku: {returndata[1]}")
                s.close()
            case 30:
                TC = returndata[1]
                u_i = returndata[2]
                plc_write(plc, GLOBALDATA_DB, ST_HOLD_ADDRESS, BOOL_SIZE, 1)
                print(f"Wartość okresu próbkowania: {returndata[1]}")
                print(f"Wartość sterowania: {returndata[2]}")
            case 40:
                u_i = returndata[1]
                stop = time.time()
                procesing_time = stop - Start
                time.sleep(TC - procesing_time)
            case 50:
                u_i = returndata[1]
                if len(returndata) == 3:
                    TC = returndata[2]
                stop = time.time()
                procesing_time = stop - Start
                time.sleep(TC - procesing_time)



