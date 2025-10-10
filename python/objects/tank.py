from parameters import *
from objects.moles import Moles
from objects.system import System

from typing import Callable

def bar_to_Pa(p_bar):
    return p_bar * 1e5

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