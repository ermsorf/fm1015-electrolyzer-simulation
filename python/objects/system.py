# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())

from objects.electrolyzer import Electrolyzer
from objects.tank import Tank
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
        anode.add_influent(placeholder(1))
        anode.add_influent(placeholder(2))

        anode.add_effluent(placeholder(3))
        anode.add_effluent(placeholder(4))

        # add cathode flows
        cathode.add_influent(placeholder(5))
        cathode.add_influent(placeholder(6))

        cathode.add_effluent(placeholder(7))
        cathode.add_effluent(placeholder(8))

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
