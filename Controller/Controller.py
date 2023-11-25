class Controller:
    ke = 0.0
    Ku = []
    U = 0.0
    du = []
    def parameterize(self, ext_ke, ext_ku, act_cv):
        self.ke = ext_ke
        self.U = act_cv
        for i in range (0,len(ext_ku)):
            self.Ku.append(ext_ku[i])
            self.du.append(0.0)
        return 0
    
    def calc_U(Contr, ext_e):
        sum = 0.0

        for i in range (0,len(Contr.Ku)):
            sum = sum + Contr.Ku[i] * Contr.du[i]
        du = float(Contr.ke) * (ext_e) - sum
        U = Contr.U + du

        if U > 100.0:
            U = 100.0
        if U < 15.0:
            U = 15.0
        Contr.U = U
        lent_du = len(Contr.du)
        Contr.du.pop(lent_du-1)
        Contr.du.insert(0, du)
        return U

    def clear_contr(self):
        self.Ku.clear()
        self.du.clear()
        return 0

if __name__ == "__main__":
    Controller1 = Controller
    Controller1.parameterize(Controller1, -1.927047675062572, [0.512386670653035, 0.6073404748590213, 0.692785466752385, 0.7696738726536276, 0.8388625615520041, 0.9011225943276212, 0.8108828646845969, 0.7296798730584706, 0.6566086673365853, 0.5908549186294725, 0.5316858461292334, 0.4784420507658238, 0.43053016665290034, 0.38741624842858513, 0.34861982079756326, 0.31370852396070464, 0.2822932952591659, 0.25402403333567247, 0.2285856964930081, 0.20569479176857056, 0.1850962155981174, 0.16656041086004603, 0.14988080861740485, 0.13487152604758484, 0.12136529490468742, 0.10921159742868891, 0.09827498892737689, 0.08843358833737751, 0.07957771994259814, 0.0716086911129676, 0.06443769244219667, 0.057984808027348525, 0.052178124860454006, 0.046952931406947715, 0.0], 37)
    print(Controller1.Ku)
    print(Controller1.ke)
    print(Controller1.du)
    print(Controller1.U)
    U = Controller1.calc_U(Controller1, 30)
    print(U)
    print(Controller1.Ku)
    print(Controller1.ke)
    print(Controller1.du)
    print(Controller1.U)
    U = Controller1.calc_U(Controller1, 30)
    print(U)
    print(Controller1.Ku)
    print(Controller1.ke)
    print(Controller1.du)
    print(Controller1.U)
    U = Controller1.calc_U(Controller1, 30)
    print(U)
    print(Controller1.Ku)
    print(Controller1.ke)
    print(Controller1.du)
    print(Controller1.U)
    U = Controller1.calc_U(Controller1, 30)
    print(U)
    print(Controller1.Ku)
    print(Controller1.ke)
    print(Controller1.du)
    print(Controller1.U)
    Controller1.clear_contr(Controller1)
    print(U)
    print(Controller1.Ku)
    print(Controller1.ke)
    print(Controller1.du)
    print(Controller1.U)

