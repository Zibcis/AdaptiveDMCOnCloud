from RegulatorParametersContainer import *
import math
class AdaptiveController:

    def __init__(self):
        self.ke = 0.0
        self.Ku = []
        self.U = 0.0
        self.du = []
        self.Tp = min(Tc)
        self.Hd_maks = int(max(Hd))

    def parameterize(self, flow_rate):
        prev, neks = self.find_me( flow_rate)  ## Szukam przedziału w którym znajduje się przepływ
        self.ke = self.linear_interpolation( prev, neks, ke[prev], ke[neks], flow_rate )
        for i in range(0,self.Hd_maks-1):
            self.Ku.append(self.linear_interpolation( prev, neks, Ku[prev][i], Ku[neks][i], flow_rate))
        return 0

    def calc_U(Contr, ext_e):
        sum = 0.0
        for i in range(0, len(Contr.Ku)):
            sum = sum + Contr.Ku[i] * Contr.du[i]
        du = float(Contr.ke) * (ext_e) - sum
        U = Contr.U + du
        if U > 100.0:
            U = 100.0
        if U < 15.0:
            U = 15.0
        Contr.U = U
        lent_du = len(Contr.du)
        Contr.du.pop(lent_du - 1)
        Contr.du.insert(0, du)
        return U

    def clear_contr(self):
        self.ke = 0.0
        self.U = 0.0
        self.Ku.clear()
        self.du.clear()
        return 0

    def linear_interpolation(self, prev, neks, prev_value, neks_value, flow_rate):
        value = prev_value + ((neks_value-prev_value)/(F[neks]-F[prev]))*(flow_rate-F[prev])
        return value

    def find_me(self, flow_rate):           ##Szukanie przedziału przepływu
        dist=[]
        for F1 in F:
            dist.append(abs(F1 - flow_rate))
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
    flow_rate = 1.5
    Controller1 = AdaptiveController()
    Controller1.parameterize(flow_rate)
    print(Controller1.ke)
    print(Controller1.Ku)
    print(Controller1.Tp)

