# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())

from python.objects.electrolyzer import Electrolyzer
from python.objects.tank import Tank
from python.objects.mols import Mols
from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent
from typing import List
from python.parameters import Parameters, params as p

def placeholder(number): ...




class System:
    
    cellcount: int
    time: float
    electrolyzer: Electrolyzer


    def __init__(self, parameters: 'Parameters' = p, time=0.0, dt=1.0):

        self.time = 0.0
        self.dt = 1.0

        self.parameters = parameters
        self.parameters.add_system(self)

        self.initialize_system()

    def initialize_system(self):
        self.anode = Tank(self, p.ANODE_SEPARATOR_VOLUME)
        self.cathode = Tank(self, p.CATHODE_SEPARATOR_VOLUME)

        self.anode.mols = Mols(
            GO2 = 0.7221,
            LH2O = 550
        )
        self.cathode.mols = Mols(
            GH2 = 3.5863,
            LH2O = 91.67
        )

        self.anode.update_vt_flash() # update gas/liquid fractions, pressures
        self.cathode.update_vt_flash()

        self.electrolyzer = Electrolyzer(self.anode, self.cathode)

        # Add influent and effluent functions to tanks
        self.anode.add_influent(inlet_pump)
        self.anode.add_influent(anode_in_recycled)
        self.anode.add_effluent(anode_valve_effluent)

        #self.cathode.add_influent()
        self.cathode.add_effluent(cathode_valve_effluent)
        self.cathode.add_effluent(cathode_out_recycled)
        

    def run_simulation(self, duration, dt):
        self.time = 0.0
        self.dt = dt
        steps = int(duration/dt)

        for _ in range(steps):
            self.step(dt)

    def step(self, dt):
            self.dt = dt
            # Update electrolyzer production rate values. (Updating electrolyzer influent and effluent return values)
            self.electrolyzer.step()

            # Update tank states (Apply influent and effluent functions)
            self.anode.calc_rates()
            self.cathode.calc_rates()
            # NOTE: order of operations here matters, so step in system not in tank. 
            # First calculate rates, then update mols.

            # Update tank mole counts
            self.anode.update_mols()
            self.cathode.update_mols()
            

            # Apply electrolyzer generation/consumption to tanks
            
            anode_count = self.electrolyzer.get_counts_anode() * dt
            cathode_count = self.electrolyzer.get_counts_cathode() * dt

            for key in anode_count.keys():
                if anode_count[key] < 0 and abs(anode_count[key]) > self.anode.mols[key]:
                    self.anode.mols[key] = 0
                    print(f"\33[31mNot enough {key} in anode tank to satisfy electrolyzer consumption.\33[0m")
                else: self.anode.mols[key] += anode_count[key]
                if cathode_count[key] < 0 and abs(cathode_count[key]) > self.cathode.mols[key]:
                    self.cathode.mols[key] = 0
                    print(f"\33[31mNot enough {key} in cathode tank to satisfy electrolyzer consumption.\33[0m")
                else: self.cathode.mols[key] += cathode_count[key]

            # Update tank states (Apply VT flash calculations)
            self.anode.update_vt_flash()
            self.cathode.update_vt_flash()  
            
            # Reset electrolyzer for next step
            self.electrolyzer.reset_frame()
            self.anode.reset_frame()
            self.cathode.reset_frame()

            # Iterate time
            self.time += dt


