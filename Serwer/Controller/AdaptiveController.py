from Serwer.Controller.RegulatorParametersContainer import *
import math
class AdaptiveController:

    def __init__(self):
        self.ke = 0.0
        self.Ku = []
        self.U = 64.0
        self.du = []
        for i in range(0, int(max(Hd))):
            self.du.append(0.0)
        self.Tp = min(Tc)
        self.Hd_maks = int(max(Hd))


    def parameterize(self, actual_temp):
        self.Ku.clear()
        prev, neks = self.find_me(actual_temp)  ## Szukam przedziału w którym znajduje się przepływ
        self.ke = self.linear_interpolation(T[prev], T[neks], ke[prev], ke[neks], actual_temp)
        for i in range(0, self.Hd_maks-1):
            self.Ku.append(self.linear_interpolation(T[prev], T[neks], Ku[prev][i], Ku[neks][i], actual_temp))
        return 0

    def calc_U(self, PV, SP):
        sum = 0.0
        ext_e = SP - PV
        for i in range(0, len(self.Ku)):
            sum = sum + self.Ku[i] * self.du[i]
        du = float(self.ke) * (ext_e) - sum
        U = self.U + du
        if U > 100.0:
            U = 100.0
        if U < 35.0:
            U = 35.0
        self.U = U
        lent_du = len(self.du)
        self.du.pop(lent_du - 1)
        self.du.insert(0, du)
        return U

    def clear_contr(self):
        self.ke = 0.0
        self.U = 0.0
        self.Ku.clear()
        self.du.clear()
        return 0

    def linear_interpolation(self, prev, neks, prev_value, neks_value, actual_temp):
        #value = prev_value + ((neks_value-prev_value)/(T[neks]-T[prev]))*(actual_temp-T[prev])
        value = ((neks_value-prev_value)/(neks-prev))*actual_temp+((prev_value*neks-neks_value*prev)/(neks-prev))
        return value

    def find_me(self, actual_temp):           ##Szukanie przedziału przepływu
        dist=[]
        for T1 in T:
            dist.append(abs(T1 - actual_temp))
        ind1 = dist.index(min(dist))
        dist[ind1]=max(dist)*100
        ind2 = dist.index(min(dist))
        if ind1 < ind2:
            prev = ind1
            neks = ind2
        else:
            prev = ind2
            neks = ind1
        return prev, neks

if __name__ == "__main__":
    flow_rate = 38.0
    Controller1 = AdaptiveController()
    print(Controller1.find_me(flow_rate))
    Controller1.parameterize(flow_rate)
    print(Controller1.ke)
    print(Controller1.Ku)
    print(Controller1.Tp)
