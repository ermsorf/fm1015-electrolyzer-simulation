# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())
from typing import TYPE_CHECKING, Callable
from python.parameters import *
from python.objects.mols import Mols
from python import vt_flash

if TYPE_CHECKING:
    from python.objects.system import System

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

        

    def add_influent(self, *influent: Callable) -> None:
        """
        List of functions that add mols to the tank.
        Each function should take the tank as an argument and modify its liq_mol and gas_mol attributes.
        """
        self.influent_functions.extend(influent)

    def add_effluent(self, *effluent: Callable) -> None:
        """
        List of functions that remove mols from the tank.
        Each function should take the tank as an argument
        and modify its liq_mol and gas_mol attributes.
        """
        self.effluent_functions.extend(effluent)

if __name__ == "__main__":
    initialize_test_tanks()