# Parameters for testing
import numpy as np
from parameters import Parameters
p = Parameters

# liquid saturation
def water_saturation_pressure(T):
    saturation_pressure = 10**(p.ANTOINE_A - p.ANTOINE_B/(p.ANTOINE_C+T+p.KELVIN_TO_CELSIUS))*p.BAR_TO_PA #Saturation pressure of H2O at T (54) [Pa]
    return saturation_pressure

def water_saturation_volume(T):
    SATURATION_A = 2.23
    SATURATION_B = -3.332e-3
    SATURATION_C = 6.421e-6
    specific_saturation_volume_H2O = (SATURATION_A+SATURATION_B*T+SATURATION_C*T**2)*1e-5 #Specific volume of H2O at T (55) [m^3/mole]
    return specific_saturation_volume_H2O

# Phi
def phi(T):
    PHI_CONSTANT = 1.0012
    PHI_SCALING = -1.6e-3
    phi_exponential = np.exp(8.7*((T+p.KELVIN_TO_CELSIUS)/373.15))
    phi_liquid_saturation_H2O = PHI_CONSTANT + PHI_SCALING*phi_exponential
    return phi_liquid_saturation_H2O

#Fugacity
def fugacity(T):
    f = phi(T)*water_saturation_pressure(T)
    return f

def Henry(T, element):
    assert element in ["H2", "O2"]
    Henry_max_H2 = 7.54e4*p.ATM_TO_PA #Hmax
    Henry_max_O2 = 7.08e4*p.ATM_TO_PA
    Max_Temperature_H2 = 1/(3.09e-3)   #Tmax
    Max_Temoperature_O2 = 1/(2.73e-3) 
    Critical_temperature_H2O  = 641.7 #Critical temp [K]

    Temperature_H2 = (1/Max_Temperature_H2-1/Critical_temperature_H2O)/(1/T-1/Critical_temperature_H2O) #Dimensionless T
    Temperature_O2 = (1/Max_Temoperature_O2-1/Critical_temperature_H2O)/(1/T-1/Critical_temperature_H2O)
    # Shorthands for next formula
    TH2 = Temperature_H2 
    TO2 = Temperature_O2
    Henry_H2  = 10**-(1.142-2.846/TH2+2.486/TH2**2-0.9761/TH2**3+0.2001/TH2**4) #Dimensionless H
    Henry_O2  = 10**-(1.142-2.846/TO2+2.486/TO2**2-0.9761/TO2**3+0.2001/TO2**4)

    Henry_Fraction_H2 = Henry_max_H2*Henry_H2 #H value for species
    Henry_Fraction_O2 = Henry_max_O2*Henry_O2
    if element == "H2":
        return Henry_Fraction_H2
    elif element == "O2":
        return Henry_Fraction_O2


def vtflash(V,T,n):
    mols_gas = np.zeros(3) # Array to hold number of moles in anode, gas
    mols_liquid = np.zeros(3) # Array to hold number of moles in anode, liquid
    pressure = np.zeros(3) # Pressure in anode
    pressure[0] = water_saturation_pressure(T) #Ph20 = psath2o, eq 34
    
    R = p.IDEAL_GAS_CONSTANT # J/mol*K
    # TODO Split up into readable chunks:
    mols_liquid[0] = (fugacity(T)*V-n[0]*T*R)/(fugacity(T)*water_saturation_volume(T)-R*T)
    mols_gas[0] = n[0]-mols_liquid[0]
    mols_gas[1] = n[1]
    mols_gas[2] = n[2]

    Volume_liquid = mols_liquid[0]*water_saturation_volume(T)
    Volume_gas = V - Volume_liquid
    
    pressure[1] = mols_gas[1]*R*T/Volume_gas
    pressure[2] = mols_gas[2]*R*T/Volume_gas
    total_pressure = sum(pressure)
    
    total_moles_gas = sum(mols_gas)
    gas_fraction_y =mols_gas/total_moles_gas
    mols_liquid[1] = mols_liquid[0]*(pressure[1]/Henry(T,"H2"))
    mols_liquid[2] = mols_liquid[0]*(pressure[2]/Henry(T,"O2"))
    total_moles_liquid = sum(mols_liquid)
    liquid_fraction_x =mols_liquid/total_moles_liquid
    
    mols_gas[1] -= mols_liquid[1]    
    mols_gas[2] -= mols_liquid[2]
    total_moles_gas = sum(mols_gas)
    gas_fraction_y = mols_gas/total_moles_gas
    total_pressure = pressure[0] + R*T/Volume_gas*(mols_gas[1]+mols_gas[2])
    specific_Volume_gas = Volume_gas/total_moles_gas
    specific_Volume_liquid = Volume_liquid/total_moles_liquid
    return (liquid_fraction_x, gas_fraction_y, total_moles_liquid, total_moles_gas, specific_Volume_liquid, specific_Volume_gas, total_pressure)
# "Constants" and other formula expected to be found elsewhere in code




if __name__ == '__main__':
    """ Expected values
    xa ≈ 0.999984, 0, 1.5588 · 10−5
    ya = (0.16589, 0, 0.83411)
    naℓ ≈ 555.87 mol
    nag ≈ 0.85569 mol
    V aℓ ≈ 1.8326 · 10−5 m3/mol
    V ag ≈ 0.02315 m3/mol
    pa ≈ 1.19732 · 105 Pa.
    """
    T_a = p.SYSTEM_TEMPERATURE # Anode temperature, [K]
    V_a = p.ANODE_SEPARATOR_VOLUME # Anode volume, [M^3]
    n_a = [556, 0, 0.7224] # Total number of moles (H2O, H2, O2) in anode tank 
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
    print("Success!")
    
