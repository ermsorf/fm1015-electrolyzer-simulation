from parameters import *
import warnings
from typing import Callable, Optional
from operator import add,sub,mul, truediv

def bar_to_Pa(p_bar):
    return p_bar * 1e5

def generate_operator(operator: callable):
    """
    Generates a function to
    compute A[operator]B
    for two species
    (e.g A+B, A-B, A*B, A/B)
    """
    def operate(self: 'Moles', other: 'Moles'):
        out = Moles()
        for attribute in other.species.keys():
            out[attribute] = operator(self.species[attribute], other.species[attribute])
        return out
    return operate

class Moles():
    def __init__(self, H2O = 0.0, O2 = 0.0, H2 = 0.0):
        self.species = {"H2O": H2O, "O2": O2, "H2": H2}
        return 
    # getting/setting
    def __getitem__(self, name):
        return self.species[name]
    def __setitem__(self, species, value):
        self.species[species] = value
    def __iter__(self):
        return iter(self.species.values())
    # Math 
    def __add__(self, other: 'Moles'):
        op = generate_operator(add)
        return op(self, other)
    def __sub__(self, other: 'Moles'):
        op = generate_operator(sub)
        return op(self, other)
    def __mul__(self, other: 'Moles'):
        op = generate_operator(mul)
        return op(self, other)
    def __div__(self, other: 'Moles'):
        op = generate_operator(truediv)
        return op(self, other)
    def __str__(self):
        return (f' - H2O: {self.species["H2O"]}\n'
               +f' - O2: {self.species["O2"]}\n'
               +f' - H2: {self.species["H2"]}')
    # dict lookups
    @staticmethod
    def keys():
        return ("H2O", "H2", "O2")
    def values(self):
        return [self.species[key] for key in self.keys()]


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

class Tank:
    def __init__(self, system, volume, temperature, pressure):
        self.system = system

        self.volume = volume  # m3
        self.temperature = temperature  # K
        self.pressure = pressure  # Pa


        self.liq_mol = Moles()
        self.gas_mol = Moles()
        
        self.influents = list()
        self.effluents = list()
        self.influent_values =  Moles()
        self.effluent_values = Moles()


    def add_influent(self, influent: Callable) -> None:
        """
        List of functions that add mols to the tank.
        Each function should take the tank as an argument and modify its liq_mol and gas_mol attributes.
        """
        self.influents.append(influent)

    def add_effluent(self, effluent: Callable) -> None:
        """
        List of functions that remove mols from the tank.
        Each function should take the tank as an argument
        and modify its liq_mol and gas_mol attributes.
        """
        self.effluents.append(effluent)

    # Mol --------------------------------------------
    def update_mol(self):
        """
        Compute everything ✨
        Apply all functions in influents and effluents to self.
        Individual functions should return a Moles object with its 
        modifications.
        """
        self.influent_values = Moles()
        self.effluent_values = Moles()
        for function in self.influents:
            self.influent_values += function(self)
        for function in self.effluents:
            self.effluent_values += function(self)


def initialize_test_tanks():
    system = System()
    atank = Tank(system, ANODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE, 1.2e5)

    atank.gas_mol["O2"] = (ANODE_SEPARATOR_VOLUME - ANODE_LIQUID_VOLUME) * atank.pressure / (IDEAL_GAS_CONSTANT * atank.temperature)
    atank.liq_mol["H2O"] = ANODE_LIQUID_VOLUME * H2O_DENSITY / H2O_MOLAR_MASS

    # m3 * kg/m3 / kg/mol = mol

    ctank = Tank(system, CATHODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE, 30e5)
    ctank.gas_mol["H2"] = (CATHODE_SEPARATOR_VOLUME - CATHODE_LIQUID_VOLUME) * ctank.pressure / (IDEAL_GAS_CONSTANT * ctank.temperature)
    ctank.liq_mol["H2O"] = CATHODE_LIQUID_VOLUME * H2O_DENSITY / H2O_MOLAR_MASS

    print(f"Anode liq: {atank.liq_mol}")
    print(f"Cathode liq: {ctank.liq_mol}")

    print(f"Anode gas: {atank.gas_mol}")
    print(f"Cathode gas: {ctank.gas_mol}")

    return system, atank, ctank



if __name__ == "__main__":
    initialize_test_tanks()


