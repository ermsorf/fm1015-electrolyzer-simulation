# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())

from python.objects.electrolyzer import Electrolyzer
from python.objects.tank import Tank
from python.objects.mols import Mols
from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent
from typing import List
from python.parameters import (
    ANODE_SEPARATOR_VOLUME, ANODE_LIQUID_VOLUME_TARGET, ANODE_EXTERNAL_PRESSURE,
    CATHODE_SEPARATOR_VOLUME, CATHODE_LIQUID_VOLUME_TARGET, CATHODE_EXTERNAL_PRESSURE,
    SYSTEM_TEMPERATURE, 
    IDEAL_GAS_CONSTANT, H2O_DENSITY, H2O_MOLAR_MASS,
)

def placeholder(number): ...




class System:
    
    cellcount: int
    time: float
    electrolyzer: Electrolyzer


    def __init__(self):

        self.initialize_system()

        self.time = float()
        self.dt = float()


    def initialize_system(self):
        self.anode = Tank(self, ANODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE)
        self.cathode = Tank(self, CATHODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE)

        self.anode.mols = Mols(
            GO2 = (ANODE_SEPARATOR_VOLUME - ANODE_LIQUID_VOLUME_TARGET) * ANODE_EXTERNAL_PRESSURE / (IDEAL_GAS_CONSTANT * self.anode.temperature),
            LH2O = ANODE_LIQUID_VOLUME_TARGET * H2O_DENSITY / H2O_MOLAR_MASS
        )
        self.cathode.mols = Mols(
            GH2 = (CATHODE_SEPARATOR_VOLUME - CATHODE_LIQUID_VOLUME_TARGET) * CATHODE_EXTERNAL_PRESSURE / (IDEAL_GAS_CONSTANT * self.cathode.temperature),
            LH2O = CATHODE_LIQUID_VOLUME_TARGET * H2O_DENSITY / H2O_MOLAR_MASS
        )

        self.anode.update_vt_flash() # update gas/liquid fractions, pressures
        self.cathode.update_vt_flash()

        self.electrolyzer = Electrolyzer(self.anode, self.cathode)

        # Add influent and effluent functions to tanks
        self.anode.add_influent(inlet_pump, anode_in_recycled)
        self.anode.add_effluent(anode_valve_effluent)
        self.cathode.add_influent(cathode_out_recycled)
        self.cathode.add_effluent(cathode_valve_effluent)
        

    def run_simulation(self, duration, dt):
        self.time = 0.0
        self.dt = dt
        steps = int(duration/dt)

        for step in range(steps):
            self.step(dt)

    def step(self, dt):
            # Update electrolyzer production rate values. (Updating electrolyzer influent and effluent return values)
            self.electrolyzer.step()

            # Update tank states (Apply influent and effluent functions)
            print("Anode calc")
            self.anode.calc_rates()
            print("Cathode calc")
            self.cathode.calc_rates()
            # NOTE: order of operations here matters, so step in system not in tank. 
            # First calculate rates, then update mols.

            # Update tank mole counts
            self.anode.update_mols()
            self.cathode.update_mols()
            
            # print("1. Anode LH2O (mol):", self.anode.mols["LH2O"])
            # Apply electrolyzer generation/consumption to tanks
            print("\033[34mElectrolyzer IPP (A/m2):\033[0m", self.electrolyzer.ipp)
            print("\033[35mElectrolyzer counts anode (mol/s):\033[0m", self.electrolyzer.get_counts_anode())
            print("\033[35mElectrolyzer counts cathode (mol/s):\033[0m", self.electrolyzer.get_counts_cathode())
            self.anode.mols += self.electrolyzer.get_counts_anode() * dt
            self.cathode.mols += self.electrolyzer.get_counts_cathode() * dt

            # Reset electrolyzer for next step
            self.electrolyzer.reset_frame()

            # Update tank states (Apply VT flash calculations)

            # print("2. Anode LH2O (mol):", self.anode.mols["LH2O"])
            self.anode.update_vt_flash()
            self.cathode.update_vt_flash()  

            # Debug prints
            # print("3. Anode LH2O (mol):", self.anode.mols["LH2O"])
            # Iterate time
            self.time += dt


