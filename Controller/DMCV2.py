import numpy as np
from array import *

def DMC_reg(Samples,Hc,Hw,Hp,Hd,alfa):
    D = len(Samples)  
    Gp = np.arange((Hp-Hw+1)*Hd,dtype=float).reshape((Hp-Hw+1,Hd))
    #Wyznaczanie macierzy Gp
    for i in range(0,(Hd-1)):
        for j in range(0,Hp-Hw+1):
            if Hw+i+j < D-1:
                Gp[j,i]=Samples[Hw+i+j]-Samples[i]
            if Hw+i+j == D-1:
                temp = Samples[Hw+i+j]
            if Hw+i+j >= D-1:
                Gp[j,i]=temp - Samples[i]
    G = np.zeros((Hp-Hw+1)*Hc,dtype=float).reshape((Hp-Hw+1,Hc))
    #Wyznaczanie macierzy G
    for i in range(0,Hc):
        for j in range(0,Hp-Hw+1):
           if(j+i)<=Hp-Hw:
                G[j+i,i] = Samples[Hw+j]
    #Wyznaczanie macierzy K
    Gt = np.transpose(G)
    I = np.eye(Hc,dtype=float)
    K = np.matmul(Gt,G)
    K = np.add(K,alfa*I)
    K = np.linalg.inv(K)
    K = np.matmul(K,Gt)
    
    ke = np.zeros(1,dtype=float)
    #Wyznaczanie wektora ke
    for i in range(Hw,Hp):
        ke[0]= ke[0] + K[0,i-Hw]
    ke = ke.tolist()

    Ku= np.zeros((Hd-1),dtype=float)
    #Wyznaczanie wektora ku
    for j in range(0,Hd-2):
        for i in range (0,Hp-Hw):
            Ku[j] = Ku[j] + K[0,i]*Gp[i,j]
    Ku = Ku.tolist()
    
    return ke, Ku

if __name__ == "__main__":
    Samples = [0,0,0.2,0.5,0.6,0.62,0.62,0.62,0.62]
    alfa = 0.01
    Hw = 3
    Hp = 6
    Hd = 6
    Hc = 3
    ke, Ku = DMC_reg(Samples,Hc,Hw,Hp,Hd,alfa)
    print(ke)
    print(Ku)
