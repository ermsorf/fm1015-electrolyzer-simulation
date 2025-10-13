from python.objects.tank import Tank
from python.objects.mols import Mols
from python.parameters import (
ANODE_REFERENCE_INJECTION,
ANODE_LIQUID_VOLUME,
ANODE_SEPARATOR_CONTROLLER_GAIN
)

def inlet_pump(tank: Tank):
    volume_difference = ANODE_LIQUID_VOLUME - tank.volume
    inlet_flow = ANODE_REFERENCE_INJECTION + ANODE_SEPARATOR_CONTROLLER_GAIN * volume_difference
    
    print("Inlet flow (mol/s):", inlet_flow)
    if inlet_flow < 0:
        inlet_flow = 0  # Prevent negative flow rates
    return Mols(LH2O=inlet_flow) 

    

if __name__ == "__main__":
    from python.objects.system import System, initialize_test_tanks
    system, atank, ctank = initialize_test_tanks()
    
    print("Initial anode tank H2O:", atank.mols["LH2O"])
    print("Initial anode tank volume:", atank.volume)
    
    atank.add_influent(inlet_pump)

    for n in range(50):
        atank.mols["LH2O"] -= 0.1  # Simulate consumption of H2O
        atank.calc_rates() # runs all influent and effluent functions(here only inlet pump)
        atank.update_mols()
        print(f"Level atank: ", atank.mols["LH2O"])
    