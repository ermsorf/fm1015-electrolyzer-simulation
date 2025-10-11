# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 11:10:24 2025

@author: tehpe
"""
# Parameters for testing
import numpy as np

V_a = 0.030 # Anode volume, [M^3]
T_a = 60+273.15 # Anode temperature, [K]
n_a = [556, 0, 0.7224] # Total number of moles (H2O, H2, O2) in anode tank 

n_ag = np.zeros(3) # Array to hold number of moles in anode, gas
n_al = np.zeros(3) # Array to hold number of moles in anode, liquid
p_a = np.zeros(3) # Pressure in anode

T = T_a # Whatever tbh OBS DETTE ER LITT JUKS
A_h2o = 5.11564 #Antoine constants ABC for H2O
B_h2o = 1687.537
C_h2o = 230.17
R = 8.314 # J/mol*K

p__sat_h2o = 10**(A_h2o - B_h2o/(C_h2o+T-273.15))*100000 #Saturation pressure of H2O at T (54) [Pa]
vspec__lsat_h2o = (2.23-3.332*10**-3*T+6.421*10**-6*T**2)/10**5 #Specific volume of H2O at T (55) [m^3/mole]
phi__lsat_h2o = 1.0012-1.6*10**-3*np.exp(8.7*((T-273.15)/373.15)) 
f__lsat_h2o = phi__lsat_h2o*p__sat_h2o #Fugacity

H_maxh2 = 7.54*10**4*101325 #Hmax
H_maxo2 = 7.08*10**4*101325
T_maxh2 = 1/(3.09*10**-3)   #Tmax
T_maxo2 = 1/(2.73*10**-3)
T_ch2   = 33.2              #Critical temp
T_co2   = 154.6
T_dimh2 = (1/T_maxh2-1/T_ch2)/(1/T-1/T_ch2) #Dimensionless T
T_dimo2 = (1/T_maxo2-1/T_co2)/(1/T-1/T_co2)
H_dimh2  = 10**-(1.142-2.846/T_dimh2+2.487/T_dimh2**2-0.9761/T_dimh2**3+0.2001/T_dimh2**4) #Dimension H
H_dimo2  = 10**-(1.142-2.846/T_dimo2+2.487/T_dimo2**2-0.9761/T_dimo2**3+0.2001/T_dimo2**4)


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
    print(p_a)
    print(n_ag)
    return (x_a, y_a, ntot_al, ntot_ag, Vspec__a_l, Vspec__a_g, ptot_a)
# "Constants" and other formula expected to be found elsewhere in code




if __name__ == '__main__':
    ans = (vtflash(V_a,T_a,n_a))
""" Expected values
xa ≈ 0.999984, 0, 1.5588 · 10−5
ya = (0.16589, 0, 0.83411)
naℓ ≈ 555.87 mol
nag ≈ 0.85569 mol
V aℓ ≈ 1.8326 · 10−5 m3/mol
V ag ≈ 0.02315 m3/mol
pa ≈ 1.19732 · 105 Pa.
"""