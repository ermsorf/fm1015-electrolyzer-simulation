from python.parameters import *
from python.objects.mols import Mols
from typing import Literal

def general_valve_effluent(tank: 'Tank', tank_type = Literal["anode", "cathode"]):
    pressure = tank.pressure
    external_pressure = ANODE_EXTERNAL_PRESSURE if tank_type == "anode" else CATHODE_EXTERNAL_PRESSURE
    pressure_delta = pressure - external_pressure
    molar_masses = [H2O_MOLAR_MASS,H2_MOLAR_MASS,O2_MOLAR_MASS]
    # This breaks if gas fractions is a dict: (fix: use .values())
    sum_mass = 0
    for fraction, mass in zip(tank.gas_fractions, molar_masses):
        sum_mass += fraction*mass

    # Prevent reverse flow
    if pressure_delta < 0:
        pressure_delta = 0

    scaling_factors = VALVE_SCALING_PRESSURE * VALVE_SCALING_GAS_DENSITY
    influent_density = sum_mass / tank.gas_volume # confirm that this is gas
    pressure_sqrt = pressure_delta * influent_density / scaling_factors
    Y = 1 - min(1, (2/3)*(pressure_delta /pressure))
    # TODO find these values
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