# Parameters for testing
import numpy as np
from parameters import *

V_a = ANODE_SEPARATOR_VOLUME # Anode volume, [M^3]
T_a = SYSTEM_TEMPERATURE # Anode temperature, [K]
T = T_a # Whatever tbh OBS DETTE ER LITT JUKS
n_a = [556, 0, 0.7224] # Total number of moles (H2O, H2, O2) in anode tank 

n_ag = np.zeros(3) # Array to hold number of moles in anode, gas
n_al = np.zeros(3) # Array to hold number of moles in anode, liquid
p_a = np.zeros(3) # Pressure in anode

R = IDEAL_GAS_CONSTANT # J/mol*K


# liquid saturation
p__sat_h2o = 10**(ANTOINE_A - ANTOINE_B/(ANTOINE_C+T+KELVIN_TO_CELSIUS))*BAR_TO_PA #Saturation pressure of H2O at T (54) [Pa]
SATURATION_A = 2.23
SATURATION_B = -3.332e-3
SATURATION_C = 6.421e-6
vspec__lsat_h2o = (SATURATION_A+SATURATION_B*T+SATURATION_C*T**2)*1e-5 #Specific volume of H2O at T (55) [m^3/mole]
# Phi
PHI_CONSTANT = 1.0012
PHI_SCALING = -1.6e-3
phi_exponential = np.exp(8.7*((T+KELVIN_TO_CELSIUS)/373.15))
phi__lsat_h2o = PHI_CONSTANT + PHI_SCALING*phi_exponential
#Fugacity
f__lsat_h2o = phi__lsat_h2o*p__sat_h2o 

H_maxh2 = 7.54e4*ATM_TO_PA #Hmax
H_maxo2 = 7.08e4*ATM_TO_PA
T_maxh2 = 1/(3.09e-3)   #Tmax
T_maxo2 = 1/(2.73e-3) 
T_ch2o  = 641.7 #Critical temp [K]

T_dimh2 = (1/T_maxh2-1/T_ch2o)/(1/T-1/T_ch2o) #Dimensionless T
T_dimo2 = (1/T_maxo2-1/T_ch2o)/(1/T-1/T_ch2o)
H_dimh2  = 10**-(1.142-2.846/T_dimh2+2.486/T_dimh2**2-0.9761/T_dimh2**3+0.2001/T_dimh2**4) #Dimensionless H
H_dimo2  = 10**-(1.142-2.846/T_dimo2+2.486/T_dimo2**2-0.9761/T_dimo2**3+0.2001/T_dimo2**4)

H_h2h2o = H_maxh2*H_dimh2 #H value for species
H_o2h2o = H_maxo2*H_dimo2


def vtflash(V,T,n):
    p_a[0] = p__sat_h2o #Ph20 = psath2o, eq 34
    
    n_al[0] = (f__lsat_h2o*V-n[0]*T*R)/(f__lsat_h2o*vspec__lsat_h2o-R*T)
    n_ag[0] = n[0]-n_al[0]
    n_ag[1] = n[1]
    n_ag[2] = n[2]

    V_l = n_al[0]*vspec__lsat_h2o
    V_g = V - V_l
    
    p_a[1] = n_ag[1]*R*T/V_g
    p_a[2] = n_ag[2]*R*T/V_g
    ptot_a = sum(p_a)
    
    ntot_ag = sum(n_ag)
    y_a =n_ag/ntot_ag
    n_al[1] = n_al[0]*(p_a[1]/H_h2h2o)
    n_al[2] = n_al[0]*(p_a[2]/H_o2h2o)
    ntot_al = sum(n_al)
    x_a =n_al/ntot_al
    
    n_ag[1] -= n_al[1]    
    n_ag[2] -= n_al[2]
    ntot_ag = sum(n_ag)
    y_a = n_ag/ntot_ag
    ptot_a = p_a[0] + R*T/V_g*(n_ag[1]+n_ag[2])
    Vspec__a_g = V_g/ntot_ag
    Vspec__a_l = V_l/ntot_al
    return (x_a, y_a, ntot_al, ntot_ag, Vspec__a_l, Vspec__a_g, ptot_a)
# "Constants" and other formula expected to be found elsewhere in code




if __name__ == '__main__':
    ans = (vtflash(V_a,T_a,n_a))
    target_values = [
        [0.99998439638184, 0.00000000e+00, 1.560361815987251e-05],
        [0.1659012208029624, 0.0, 0.8340987791970376],
        555.8667142157208,
        0.8556857842792654,
        1.832575476118332e-05,
        0.023154904848707365,
        119726.20009420183
    ]
    for a, t in zip(ans,target_values):
        if isinstance(t, list):
            for (asublist, tsublist) in zip(a,t):
                assert asublist == tsublist, "sublist changed"
        else:
            assert a == t, "value changed"
    
""" Expected values
xa ≈ 0.999984, 0, 1.5588 · 10−5
ya = (0.16589, 0, 0.83411)
naℓ ≈ 555.87 mol
nag ≈ 0.85569 mol
V aℓ ≈ 1.8326 · 10−5 m3/mol
V ag ≈ 0.02315 m3/mol
pa ≈ 1.19732 · 105 Pa.
"""