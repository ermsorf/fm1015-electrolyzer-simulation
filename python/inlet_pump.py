from objects import Tank, System
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
    system = System()
    tank = Tank()
    inlet_pump(tank)