from parameters import *
import warnings
import numpy as np

def bar_to_Pa(p_bar):
    return p_bar * 1e5

class System:
    def __init__(self):
        self.tanks = []

    def add_tank(self, tank):
        self.tanks.append(tank)

    def log_state(self):
        pass


class Tank:
    def __init__(self, system, volume, temperature, pressure):
        self.system = system

        self.volume = volume  # m3
        self.temperature = temperature  # K
        self.pressure = pressure  # Pa

        self.liquid_volume
        self.liquid_mass
        self.liquid_mol

        self.gas_volume
        self.gas_mass
        self.gas_mol
        
    def log_state():
        pass

system = System()

anode_tank = Tank(system, ANODE_SEPARATOR_VOLUME, ANODE_LIQUID_VOLUME, SYSTEM_TEMPERATURE, bar_to_Pa(1.2))
cathode_tank = Tank(system, CATHODE_SEPARATOR_VOLUME, CATHODE_LIQUID_VOLUME, SYSTEM_TEMPERATURE, bar_to_Pa(30.0))






# PROBLEM 1 - Overall stoichiometric coefficients -------------------------------------
# Reaction: 2H2O -> 2H2 + O2 + (4e-)
v = [-2, 2, 1]
v_e = 4

# PROBLEM 2 - Water amounts in separator tanks ----------------------------------------

anode_water_mass = ANODE_LIQUID_VOLUME * WATER_DENSITY  # kg
anode_water_mol = anode_water_mass / WATER_MOLAR_MASS  # mol

cathode_water_mass = CATHODE_LIQUID_VOLUME * WATER_DENSITY  # kg
cathode_water_mol = cathode_water_mass / WATER_MOLAR_MASS  # mol

# PROBLEM 3 - Gas amounts in separator systems ----------------------------------------

def saturation_pressure(tank):
    """
    Finds saturation pressure of water at temperature T using Antoine equation. 
    :param Tank: Tank Object [K]
    :returns p_H2O_sat: Saturation pressure of water [Pa]
    """
    if not (0.01e5 <= tank.pressure <= 16e5):
        warnings.warn("Tank pressure out of range for Antoine equation (0.01–16 bar)", UserWarning)
    if not (273.2 <= tank.temperature <= 473.2):
        warnings.warn("Tank temperature out of range for Antoine equation (273.2–473.2 K)", UserWarning)

    T = tank.temperature
    A = ANTOINE_A
    B = ANTOINE_B
    C = ANTOINE_C
    log10_pH2O_sat = A - B / (C + T - 273.15)
    p_H2O_sat = 10**(log10_pH2O_sat / VALVE_SCALING_PRESSURE)  # in Pa
    return p_H2O_sat



# if saturation pressure > tank pressure, water cannot stay liquid -> vaporizes
anode_saturation_pressure = saturation_pressure(anode_tank.temperature)
cathode_saturation_pressure = saturation_pressure(cathode_tank.temperature) 
# Move into Tank class

def gas_volume():
    anode_gas_volume = ANODE_SEPARATOR_VOLUME - ANODE_LIQUID_VOLUME  # m3
    cathode_gas_volume = CATHODE_SEPARATOR_VOLUME - CATHODE_LIQUID_VOLUME  # m3
    return anode_gas_volume, cathode_gas_volume

def tank_partial_pressure(tank_pressure, saturation_pressure):
    if saturation_pressure >= tank_pressure:
        return 0
    return tank_pressure - saturation_pressure

def partial_pressure():
    """
    Find partial pressure using ideal gas law
    :param 
    returns partial_pressure: Partial pressure of gas in tank [Pa]
    """
    gas_volume = gas_volume()
    partial_pressure = (n * IDEAL_GAS_CONSTANT * SYSTEM_TEMPERATURE)/(gas_volume)
    

anode_o2_partial_pressure = tank_partial_pressure(anode_pressure, anode_saturation_pressure)
cathode_h2_partial_pressure = tank_partial_pressure(cathode_pressure, cathode_saturation_pressure)



# PROBLEM 4 - Water consumption in electrolyzer ----------------------------------------

current_density = 2e-5  # A/m2

def water_consumption_rate(current):
    """
    Calculate water consumption rate in mol/s from current using Faraday's law.
    :param current: Current in Amperes [A]
    :returns n_H2O: Water consumption rate in mol/s
    """
    n_H2O = -v[0] * current / (v_e * FARADAY_CONSTANT)  # mol/s
    return n_H2O

def water_generation_rate(current):
    """
    Calculate H2 and O2 production rates from current using Faraday's law.
    :param current: Current in Amperes [A]
    :returns n_H2: Hydrogen production rate in mol/s
    :returns n_O2: Oxygen production rate in mol/s
    """
    n_H2 = v[1] * current / (v_e * FARADAY_CONSTANT)  # mol/s
    n_O2 = v[2] * current / (v_e * FARADAY_CONSTANT)  # mol/s
    return n_H2, n_O2


def nd_e__g(current):
    return MEMBRANE_AREA_SUPERFICIAL * current / FARADAY_CONSTANT

def nd_j__g(current):
    return  v / v_e * nd_e__g(current)


# PROBLEM 5 - Water flow through the membrane ----------------------------------------

def nd_H20__d():
    pass


# PROBLEM 6 - 