# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())
class System:
    next_tanks: list['Tank']
    tanks: list['Tank']
    cellcount: int
    def __init__(self):
        self.tanks = list()
        self.next_tanks = list()
        self.cellcount = None # set to 0?

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

    def update_state(self):
        for tank in self.next_tanks:
            tank.update_mole_balance()
        self.reload_tanks()

    def log_state(self):
        pass

# import if running as main - makes IDE happy
if __name__ == "__main__":
    from objects.objects import Tank