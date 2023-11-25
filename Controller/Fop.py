import numpy as np

def foptd(t, K=1, tau=1, tau_d=0):
    tau_d = max(0,tau_d)
    tau = max(0,tau)
    return np.array([K*(1-np.exp(-(t-tau_d)/tau)) if t >= tau_d else 0 for t in t])

def err(X,t,y):
    K,tau,tau_d = X
    z = foptd(t,K,tau,tau_d)
    iae = sum(abs(z-y))*(max(t)-min(t))/len(t)
    return iae