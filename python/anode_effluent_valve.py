from parameters import *
from objects import Mols

def anode_valve_effluent(anode_tank: 'Tank'):

    anode_pressure = anode_tank.pressure
    anode_pressure_delta = anode_pressure - ANODE_EXTERNAL_PRESSURE
    Y = 1 - min(1, (2/3)*(anode_pressure_delta /anode_pressure))
    gas_volume = anode_tank.gas_volume
    sum_y_times_Mi = 0
    for key in ["GH2O","GH2","GO2"]:
        sum_y_times_Mi += anode_tank.gas_mol.get(key)*anode_tank.gas_mass.get(key)
    sqrt1 = anode_pressure_delta/( VALVE_SCALING_PRESSURE*VALVE_SCALING_GAS_DENSITY*gas_volume)
    sqrt2 = 1/(sum_y_times_Mi)

    for key in ["GH2O","GH2","GO2"]:



    mols = Mols()
    pass 


if __name__ == "__main__":
    from objects.tank import Tank