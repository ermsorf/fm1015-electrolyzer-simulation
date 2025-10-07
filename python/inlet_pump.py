from objects import Tank, System, initialize_test_tanks
from parameters import (
ANODE_REFERENCE_INJECTION,
ANODE_LIQUID_VOLUME,
ANODE_SEPARATOR_CONTROLLER_GAIN
)

def inlet_pump(tank: Tank):
    volume_difference = ANODE_LIQUID_VOLUME - tank.volume
    inlet_flow = ANODE_REFERENCE_INJECTION + ANODE_SEPARATOR_CONTROLLER_GAIN*volume_difference

    tank.liq_mol["H2O"] += inlet_flow
    return None

    

if __name__ == "__main__":
    system, atank, ctank = initialize_test_tanks()
    
    print("Initial anode tank H2O:", atank.liq_mol["H2O"])
    print("Initial anode tank volume:", atank.volume)
    
    inlet_pump(atank)
    
    print("After inlet pump - anode tank H2O:", atank.liq_mol["H2O"])