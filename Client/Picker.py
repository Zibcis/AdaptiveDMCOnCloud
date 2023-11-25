from Parameters import *
import snap7
import time
#Funkcja pobierajaca probki z sterownika
def picker(plc,Tc):
    Samples = []
    Time = []
    t = 0.0
    while(int.from_bytes(plc.db_read(GLOBALDATA_DB,JUMP_ADDRESS,INT_SIZE),"big")==1 or int.from_bytes(plc.db_read(GLOBALDATA_DB,JUMP_ADDRESS,INT_SIZE),"big")==4 ):
        Samples.append(snap7.util.get_real(plc.db_read(SAMPLES_DB,START_ADDRESS,REAL_SIZE),0) )
        tz = round(t,1)
        Time.append(tz)
        time.sleep(Tc)
        t = t+Tc
    print('Sampling Complete')
    print(Samples)
    print(Time)
    Err = 0
    return Samples,Time, Err
