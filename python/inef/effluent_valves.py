import numpy as np
from python.parameters import params as p
from python.objects.mols import Mols
from typing import Literal

def general_valve_effluent(tank: 'Tank', tank_type = Literal["anode", "cathode"]):
    pressure = tank.pressure
    external_pressure = p.ANODE_EXTERNAL_PRESSURE if tank_type == "anode" else p.CATHODE_EXTERNAL_PRESSURE
    mass_flow_capacity = 2.4e-3 if tank_type == "anode" else 4.4e-5  
    pressure_delta = pressure - external_pressure
    molar_masses = [p.H2O_MOLAR_MASS,p.H2_MOLAR_MASS,p.O2_MOLAR_MASS]
    # This breaks if gas fractions is a dict: (fix: use .values())
    sum_mass = 0
    for fraction, mass in zip(tank.gas_fractions, molar_masses):
        sum_mass += fraction*mass

    # Prevent reverse flow
    if pressure_delta < 0:
        pressure_delta = 0

    scaling_factors = p.VALVE_SCALING_PRESSURE * p.VALVE_SCALING_GAS_DENSITY
    influent_density = sum_mass / tank.gas_volume # confirm that this is gas
    pressure_sqrt = np.sqrt(pressure_delta * influent_density / scaling_factors)
    Y = 1 - min(1, (2/3)*(pressure_delta /pressure))
    # TODO find these values
    valve_control_signal = 0.5 # arbitrary, consider different approaches.
    valve_mass_flow = valve_control_signal*mass_flow_capacity*Y*pressure_sqrt

    valve_mole_flow = valve_mass_flow/sum_mass

    mols = Mols()
    # This breaks if gas fractions is a dict: (fix: use .values())
    for key, fraction in zip(["GH2O","GH2","GO2"], tank.gas_fractions):
        mols[key] = fraction*valve_mole_flow
    return mols

def anode_valve_effluent(tank: 'Tank'):
    return general_valve_effluent(tank, "anode")

def cathode_valve_effluent(tank: 'Tank'):
    return general_valve_effluent(tank, "cathode")

if __name__ == "__main__":
    from objects.tank import Tank