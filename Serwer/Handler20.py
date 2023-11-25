import socket
import struct
from Serwer_Param import *
from ParametryzacjaRegulatora import *
from FOPDT import *
from DMCV2 import *
from Controller import *



#Potrzebne zmiennee i stałe
Tc = 1
Samples = []
Sample = []
Time = []
data = []
msg = []
value_of_jump = 0.0
if_parametrized = 0
DMC_contr = Controller

#Tworzenie gniazda serwera
s = socket.socket()
host = socket.gethostname()
#Przygotowanie serwera
s.bind(('', port))
s.listen()

while True:

            #Przyjecie połączenia
            c , addr = s.accept()
            print("Connection established")
            #Odbiór danych  
            data = c.recv(50000)
            #Przetworzenie danych
            size = len(data)/4.0
            size = int(size)
            Sample = struct.unpack('<{}f'.format(size), data)
            data=[]
            match Sample[0]:
                case 1.0:   #inicjalizacja - podjazd pod punkt pracy
                    msg.append(10)
                    msg.append(40.0)
                    msg_size = len(msg)
                    returnmsg = struct.pack('<{}f'.format(msg_size),*msg)
                    msg=[]
                    c.send(returnmsg)
                    print(f"Wysłano wartość inicjalizaci: {6.5}")
                case 2.0:   #dodanie delty do sterowania - skok w otoczeniu punktu pracy
                    msg.append(20)
                    value_of_jump = Sample[1]+3
                    msg.append(value_of_jump)
                    msg_size = len(msg)
                    returnmsg = struct.pack('<{}f'.format(msg_size), *msg)
                    msg = []
                    c.send(returnmsg)
                    print(f"Wysłano wartość skoku: {value_of_jump}")
                case 3.0:   # Parametryzacja regulatora
                    sep_index = Sample.index(9999.0)
                    for i in range(1, sep_index):
                        Samples.append(Sample[i])
                        Time.append(Sample[sep_index+i])
                    print(Samples)
                    print(Time)
                    reg_parameters = ParametryzacjaRegulatora(Time, Samples)
                    Time.clear()
                    Samples.clear()
                    Tc = reg_parameters[1]*0.1
                    Hc, Hw, Hp, Hd, alfa = NastawyRegulatora(reg_parameters[0], reg_parameters[1])
                    print(Hd)
                    calculated_samples = FOPDT(reg_parameters[1], reg_parameters[0], reg_parameters[2]/3, int(Hp), int(Hd))
                    ke, Ku = DMC_reg(calculated_samples, int(Hc), int(Hw), int(Hp), int(Hd), alfa)
                    print(ke)
                    print(Ku)
                    print(Tc)
                    msg.append(30)
                    msg.append(Tc)
                    msg.append(value_of_jump)
                    msg_size = len(msg)
                    returnmsg = struct.pack('<{}f'.format(msg_size), *msg)
                    msg = []
                    c.send(returnmsg)
                    DMC_contr.clear_contr(DMC_contr)
                    print("Wartości ku oraz Ke zostały wyznaczone poprawnie")
                    if_parametrized = 0
                case 4.0:   # Wyznaczanie sterowania
                    if if_parametrized == 0:
                        DMC_contr.parameterize(DMC_contr, ke[0], Ku, Sample[1])
                        print("Ragulator został sparametryzowany poprawnie")
                        if_parametrized = 1
                        msg.append(40)
                        msg.append(Sample[1])
                        msg_size = len(msg)
                        returnmsg = struct.pack('<{}f'.format(msg_size), *msg)
                        msg = []
                        c.send(returnmsg)
                    else:
                        u_i = DMC_contr.calc_U(DMC_contr, Sample[3]-Sample[2])
                        msg.append(40)
                        msg.append(u_i)
                        msg_size = len(msg)
                        returnmsg = struct.pack('<{}f'.format(msg_size), *msg)
                        msg = []
                        c.send(returnmsg)
                        print(f"Wyznaczono sterowanie o wartości: {u_i}")
            c.close()
