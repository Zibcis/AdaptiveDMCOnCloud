import numpy as np
from array import *
from scipy.optimize import minimize
import struct
from Serwer.Controller.Fop import *
from Serwer.Controller.FOPDT import *
from Serwer.Controller.DMCV2 import *
#Funkcja do wyznaczenia parametrów modelu
def ParametryzacjaRegulatora(Time,Samp):
    D = len(Samp)
    Ti = list(Time)
    for i in range(0,D-1):
        Ti[i] = round(Ti[i],1)
    k = (Samp[D-1]-Samp[0])
    X = [k,5,5]
    k,T,T0 = minimize(err,X,args=(Ti,Samp)).x
    return [T0, T, k]

#Funkcja FOPDT
def fopdt(t, K=1, tau=1, tau_d=0):
    tau_d = max(1,tau_d)
    tau = max(1,tau)
    return np.array([K*(1-np.exp(-(t-tau_d)/tau)) if t >= tau_d else 0 for t in t])

#Wyznaczanie błędu
def err(X,t,y):
    K,tau,tau_d = X
    z = fopdt(t,K,tau,tau_d)
    iae = sum(abs(z-y))*(max(t)-min(t))/len(t)
    return iae

#Parametryzacja regulatora
def NastawyRegulatora(T0,T):
    Tp = 0.1 * T
    Tp = round(Tp,1)
    Hc = 2
    Hw = np.floor(T0/Tp + 1)
    Hp = np.around(T/Tp + T0/Tp)
    Hd = np.around((5*T)/Tp + T0/Tp)  ### Wydłużenie horyzontu dynamiki do 4-5 !!!! Było 3
    x = 0.0146/(1+(T0/T))
    k =  9.80#13 #9.80 #8.23 #5.66 #0.7225  #0.26879 #0.6009#2.549 #1.9 #0.85
    alfa = x*(np.power(k,2)*Hp)
    print(alfa)
    return Hc,Hw,Hp,Hd,alfa

def unpack(data):
    i=1
    size = len(data) / 4.0
    size = int(size)
    unstruct_data = struct.unpack('<{}f'.format(size), data)
    while unstruct_data[i] != 9999.0:
        i= i+ 1
    sep_index = i
    return sep_index

if __name__ == "__main__":
    time = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0, 185.0, 190.0, 195.0, 200.0, 205.0, 210.0, 215.0, 220.0, 225.0, 230.0, 235.0, 240.0, 245.0, 250.0, 255.0, 260.0, 265.0, 270.0, 275.0, 280.0, 285.0, 290.0, 295.0, 300.0, 305.0, 310.0, 315.0, 320.0, 325.0, 330.0, 335.0, 340.0, 345.0, 350.0, 355.0, 360.0, 365.0, 370.0, 375.0, 380.0, 385.0, 390.0, 395.0, 400.0, 405.0, 410.0, 415.0, 420.0, 425.0, 430.0, 435.0, 440.0, 445.0, 450.0, 455.0, 460.0, 465.0, 470.0, 475.0, 480.0, 485.0, 490.0, 495.0, 500.0, 505.0, 510.0, 515.0, 520.0]
    samples = [7.62939453125e-05, 0.001190185546875, 0.001953125, -0.00579071044921875, -0.10272979736328125, -0.3482208251953125, -0.7444915771484375, -1.2681198120117188, -1.8874130249023438, -2.5568161010742188, -3.2766342163085938, -4.011497497558594, -4.7443389892578125, -5.462715148925781, -6.157920837402344, -6.811210632324219, -7.445869445800781, -8.04644775390625, -8.612335205078125, -9.143821716308594, -9.641761779785156, -10.107398986816406, -10.542213439941406, -10.93994140625, -11.318473815917969, -11.671043395996094, -11.999290466308594, -12.304771423339844, -12.588981628417969, -12.848236083984375, -13.094482421875, -13.323455810546875, -13.536369323730469, -13.734336853027344, -13.91839599609375, -14.089508056640625, -14.248603820800781, -14.393669128417969, -14.531364440917969, -14.659393310546875, -14.778411865234375, -14.889060974121094, -14.991920471191406, -15.085689544677734, -15.17471694946289, -15.25747299194336, -15.334400177001953, -15.405914306640625, -15.472396850585938, -15.533012390136719, -15.590553283691406, -15.644050598144531, -15.693778991699219, -15.740009307861328, -15.782981872558594, -15.822162628173828, -15.859355926513672, -15.893928527832031, -15.926074981689453, -15.955379486083984, -15.983203887939453, -16.00905990600586, -16.033100128173828, -16.055450439453125, -16.075824737548828, -16.095165252685547, -16.113143920898438, -16.129863739013672, -16.145404815673828, -16.159564971923828, -16.173015594482422, -16.18552017211914, -16.197147369384766, -16.207958221435547, -16.217998504638672, -16.227153778076172, -16.235843658447266, -16.243927001953125, -16.251441955566406, -16.258426666259766, -16.264915466308594, -16.27096176147461, -16.276458740234375, -16.28168487548828, -16.286544799804688, -16.291046142578125, -16.295246124267578, -16.299148559570312, -16.302703857421875, -16.306072235107422, -16.309215545654297, -16.3121337890625, -16.314842224121094, -16.317306518554688, -16.31964874267578, -16.32183074951172, -16.323867797851562, -16.32577133178711, -16.32745361328125, -16.329071044921875, -16.330596923828125, -16.331981658935547, -16.333316802978516, -16.33449935913086, -16.335643768310547]
    reg_parameters = ParametryzacjaRegulatora(time, samples)
    print(reg_parameters)
    Tc = reg_parameters[1]*0.1
    Hc, Hw, Hp, Hd, alfa = NastawyRegulatora(reg_parameters[0], reg_parameters[1])
    calculated_samples = FOPDT(reg_parameters[1], reg_parameters[0], reg_parameters[2]/5, int(Hp), int(Hd))
    print(calculated_samples)
    ke, Ku = DMC_reg(calculated_samples, int(Hc), int(Hw), int(Hp), int(Hd), alfa)
    print(ke)
    print(Ku)
