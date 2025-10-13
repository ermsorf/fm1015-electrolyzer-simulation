# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())

from objects.electrolyzer import Electrolyzer
from objects.tank import Tank
from inlet_pump import inlet_pump
from recycled import anode_in_recycled, cathode_out_recycled
from effluent_valves import anode_valve_effluent, cathode_valve_effluent
from typing import List
from parameters import (
    ANODE_SEPARATOR_VOLUME,
    CATHODE_SEPARATOR_VOLUME,
    SYSTEM_TEMPERATURE,
)

def placeholder(number): ...
class System:
    next_tanks: List[Tank]
    tanks: List[Tank]
    cellcount: int
    time: float
    electrolyzer: Electrolyzer
    def __init__(self):
        self.tanks: List[Tank] = list()
        self.initialize_tanks()
        self.next_tanks: List[Tank] = self.tanks

        self.cellcount = int()
        self.time = float()

    def step(self):
        self.electrolyzer.step()
        for tank in self.next_tanks:
            tank.step()
        self.reload_tanks()
        self.clear_step_flags()
    
    def initialize_tanks(self):
        # Create tanks
        anode = Tank(self, ANODE_SEPARATOR_VOLUME,SYSTEM_TEMPERATURE)
        cathode = Tank(self, CATHODE_SEPARATOR_VOLUME,SYSTEM_TEMPERATURE)
        # add anode flows
        anode.add_influent(inlet_pump)
        anode.add_influent(self.electrolyzer.get_counts_anode)
        anode.add_influent(anode_in_recycled)

        #anode.add_effluent(self.electrolyzer.get_counts_anode) # implicit from influent sums
        anode.add_effluent(anode_valve_effluent)

        # add cathode flows
        cathode.add_influent(self.electrolyzer.get_counts_cathode)

        #cathode.add_effluent(self.electrolyzer.get_counts_anode) # implicit from influent
        cathode.add_effluent(cathode_out_recycled)
        cathode.add_effluent(cathode_valve_effluent)

        # commit initialized tanks to self.tanks
        self.add_tank(anode)
        self.add_tank(cathode)

    def add_tank(self, tank):
        self.next_tanks.append(tank)
        self.tanks.append(tank)
    
    def reload_tanks(self):
        """
        update the old_tank values to be 
        equal to the current tank state.
        """
        self.tanks = list()
        for tank in self.next_tanks:
            self.tanks.append(tank)

    def clear_step_flags(self):
        for tank in self.tanks:
            tank.step_completed = False
        self.electrolyzer.step_completed = False




    def log_state(self):
        pass
