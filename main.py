from python.objects import *
from python.parameters import *
from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent

## Initialize the system

system = System()

system.run_simulation(duration=10, dt=0.1)
print(system.anode.mols)
print(system.cathode.mols)
