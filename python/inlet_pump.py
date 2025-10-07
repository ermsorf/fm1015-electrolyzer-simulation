from objects import Tank, System, Species
from parameters import (
ANODE_REFERENCE_INJECTION,
ANODE_REFERENCE_VOLUME,
ANODE_KP
)


def inlet_pump(tank: Tank):
    volume_difference = ANODE_REFERENCE_VOLUME - tank.volume
    inlet_flow = ANODE_REFERENCE_INJECTION + ANODE_KP*volume_difference
    flow = {
        "liquid":{
            "H2O": inlet_flow,
            "H2": 0,
            "O2": 0
        },
        "gas":{
            "H2O": 0,
            "H2": 0,
            "O2": 0
        }
    }
    return flow

    

if __name__ == "__main__":
    system = System()
    tank = Tank()
    inlet_pump(tank)