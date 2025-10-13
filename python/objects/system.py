# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())

from objects.electrolyzer import Electrolyzer
from objects.tank import Tank
from typing import List
class System:
    next_tanks: List[Tank]
    tanks: List[Tank]
    cellcount: int
    time: float
    electrolyzer: Electrolyzer
    def __init__(self):
        self.tanks: List[Tank] = list()
        self.next_tanks: List[Tank] = list()
        self.cellcount = int()
        self.time = float()

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

    def step(self):
        self.electrolyzer.step()
        for tank in self.next_tanks:
            tank.step()
        self.reload_tanks()
        self.clear_step_flags()



    def log_state(self):
        pass
