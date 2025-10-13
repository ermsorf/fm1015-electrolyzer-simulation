# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())
from parameters import *
from objects.mols import Mols
from objects.system import System
import vt_flash

from typing import Callable

def bar_to_Pa(p_bar):
    return p_bar * 1e5

class Tank:
    system: System
    def __init__(self, system, volume, temperature):
        self.system = system

        self.volume = volume  # m3
        self.temperature = temperature  # K

        self.influent_functions = list()
        self.effluent_functions = list()

        self.influent_values =  Mols()
        self.effluent_values = Mols()

        self.mols = Mols()
        self.step_completed = False
        

    def step(self):
        if self.step_completed: return
        for fun in self.influent_functions:
            self.mols +=fun(self)
        for fun in self.effluent_functions:
            self.mols -=fun(self)
        self.step_completed = True

    def update_vt_flash(self):
        results = vt_flash.vtflash(self.volume, self.temperature, self.mols.get_sums().values())
        (
            self.liquid_fractions,
            self.gas_fractions,
            self.liquid_total_molecount,
            self.gas_total_molecount,
            self.liquid_volume,
            self.gas_volume,
            self.pressure
        ) = results
        # CHECK are these values correctly updated?:
        # (fear is, these values are added to the total somehow / not 
        # representative of a partial volume etc etc.)
        # (fear 2: drag etc should be calculated before updating mole counts)
        self.mols=Mols(
            LH2O=self.liquid_fractions[0]*self.liquid_total_molecount,
            LH2=self.liquid_fractions[1]*self.liquid_total_molecount,
            LO2=self.liquid_fractions[2]*self.liquid_total_molecount,
            GH2O=self.gas_fractions[0]*self.gas_total_molecount,
            GH2=self.gas_fractions[1]*self.gas_total_molecount,
            GO2=self.gas_fractions[2]*self.gas_total_molecount
        )

        

    def add_influent(self, influent: Callable) -> None:
        """
        List of functions that add mols to the tank.
        Each function should take the tank as an argument and modify its liq_mol and gas_mol attributes.
        """
        self.influent_functions.append(influent)

    def add_effluent(self, effluent: Callable) -> None:
        """
        List of functions that remove mols from the tank.
        Each function should take the tank as an argument
        and modify its liq_mol and gas_mol attributes.
        """
        self.effluent_functions.append(effluent)

# TODO push function to other file / keep for now and kill down the line
def initialize_test_tanks():
    system = System()
    atank = Tank(system, ANODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE, 1.2e5)

    atank.mols["GO2"] = (ANODE_SEPARATOR_VOLUME - ANODE_LIQUID_VOLUME) * atank.pressure / (IDEAL_GAS_CONSTANT * atank.temperature)
    atank.mols["LH2O"] = ANODE_LIQUID_VOLUME * H2O_DENSITY / H2O_MOLAR_MASS

    # m3 * kg/m3 / kg/mol = mol

    ctank = Tank(system, CATHODE_SEPARATOR_VOLUME, SYSTEM_TEMPERATURE, 30e5)
    ctank.mols["GH2"] = (CATHODE_SEPARATOR_VOLUME - CATHODE_LIQUID_VOLUME) * ctank.pressure / (IDEAL_GAS_CONSTANT * ctank.temperature)
    ctank.mols["LH2O"] = CATHODE_LIQUID_VOLUME * H2O_DENSITY / H2O_MOLAR_MASS

    print(f"Anode mols: {atank.mols}")
    print(f"Cathode mols: {ctank.mols}")

    return system, atank, ctank



if __name__ == "__main__":
    initialize_test_tanks()