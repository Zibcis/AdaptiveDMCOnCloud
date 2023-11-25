
def FOPDT(T,T0,k1,Hp,Hd):
    #Potrzebne dane
    Tp = 0.1 * T
    Tp = round(Tp,1)
    Samp = []
    i=0
    k=0
    Thout1 = 0.0
    Thout2 = 0.0
    
    while(i<=Hd+Hp):
        if(k>=T0):
            Thout2 = Thout1 + (((-1)/T)*Thout1 + (k1/T))*Tp
        Samp.append(Thout2)
        i = i + 1
        k=k+Tp
        Thout1 = Thout2
    return Samp