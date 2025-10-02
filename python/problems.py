from parameters import *
from objects import *

def water_consumption_rate(current):
    """
    Calculate water consumption rate in mol/s from current using Faraday's law.
    :param current: Current in Amperes [A]
    :return n_H2O: Water consumption rate in mol/s
    """
    n_H2O = None
    return None

def water_generation_rate(current):
    """
    Calculate H2 and O2 production rates from current using Faraday's law.
    :param current: Current in Amperes [A]
    :return n_H2: Hydrogen production rate in mol/s
    :return n_O2: Oxygen production rate in mol/s
    """
    return None


def nd_e__g(current):
    return MEMBRANE_AREA_SUPERFICIAL * current / FARADAY_CONSTANT

def nd_j__g(current):
    v = [-2, 2, 1]
    v_e = 4
    return  v / v_e * nd_e__g(current)

def nd_H20__d():
    pass


def main():

    # Initialize system and tanks
    system = System()

    anode_tank = Tank(system, ANODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE, bar_to_Pa(30.0))
    cathode_tank = Tank(system, CATHODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE, bar_to_Pa(30.0))

    anode_tank.liquid_mol = {"H2O" : ANODE_LIQUID_VOLUME * H2O_DENSITY / H2_MOLAR_MASS, "H2": 0, "O2": 0}
    anode_tank.update_levels()
    cathode_tank.liquid_mol = {"H2O" : ANODE_LIQUID_VOLUME * H2O_DENSITY / H2_MOLAR_MASS, "H2": 0, "O2": 0} 
    cathode_tank.update_levels()
    # PROBLEM 1 - Overall stoichiometric coefficients -------------------------------------
    # Reaction: 2H2O -> 2H2 + O2 + (4e-)
    v = [-2, 2, 1]
    v_e = 4

    # PROBLEM 2 - Water amounts in separator tanks ----------------------------------------
    print(anode_tank.find_liquid_mass())  # kg
    print(anode_tank.liquid_mol) # mol

    print(cathode_tank.find_liquid_mass()) # kg
    print(cathode_tank.liquid_mol) # mol

    # PROBLEM 3 - Gas amounts in separator systems ----------------------------------------
    # if saturation pressure > tank pressure, water cannot stay liquid -> vaporizes
    print(anode_tank.find_saturation_pressure())
    print(cathode_tank.find_saturation_pressure())
    print(anode_tank.find_gas_partial_pressure())
    print(cathode_tank.find_gas_partial_pressure())

    # PROBLEM 4 - Water consumption in electrolyzer ----------------------------------------

    current_density = 2e-5  # A/m2

    # PROBLEM 5 - Water flow through the membrane ----------------------------------------
    nd_H20__d()

    # PROBLEM 6 - 

if __name__ == "__main__":
    main()