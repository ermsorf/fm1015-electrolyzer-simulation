# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())
from typing import TYPE_CHECKING, Callable
from warnings import warn
from python.parameters import params as p
from python.objects.mols import Mols
from python import vt_flash

if TYPE_CHECKING:
    from python.objects.system import System

def bar_to_Pa(p_bar):
    return p_bar * 1e5

class Tank:
    system: 'System'
    def __init__(self, system, volume):
        self.system = system

        self.volume = volume  # m3
        # self.temperature = temperature  # K

        self.influent_functions = list()
        self.effluent_functions = list()

        self.influent_values =  Mols()
        self.effluent_values = Mols()

        self.mols = Mols()
        
        self.step_completed = False # In the future, reset this on global step

        self.track_recycled = []  # For analysis purposes

    @property
    def temperature(self):
        return p.SYSTEM_TEMPERATURE

    def reset_frame(self):
        self.influent_values = Mols()
        self.effluent_values = Mols()
        self.step_completed = False

    def calc_rates(self):
        self.influent_values = Mols() # reset to zero
        self.effluent_values = Mols() # reset to zero
        self.tracked_values = {}


        for fun in self.influent_functions:
            funresult = fun(self)
            self.influent_values = self.influent_values + funresult
            self.tracked_values.update({"influent_"+fun.__name__: funresult})


        for fun in self.effluent_functions:
            self.effluent_values = self.effluent_values + fun(self)
            self.tracked_values.update({"effluent_"+fun.__name__: fun(self)})
            
                
        
    def update_mols(self):
        if self.step_completed: warn("Tried to update mols twice in step"); return
        self.mols = self.mols + ((self.influent_values - self.effluent_values) * self.system.dt)
        self.step_completed = True

    def update_vt_flash(self):
        """ Updates tank state using VT flash calculations. Updates mole fractions"""
        if any(x < 0 for x in list(self.mols.values())):
                raise ValueError("Negative mole counts in tank before VT flash.")
        
        results = vt_flash.vtflash(self.volume, self.temperature, list(self.mols.get_sums().values()))
        (
            self.liquid_fractions,
            self.gas_fractions,
            self.liquid_total_molecount,
            self.gas_total_molecount,
            self.liquid_specific_volume,
            self.gas_specific_volume,
            self.pressure
        ) = results

        self.gas_volume = self.gas_specific_volume * self.gas_total_molecount
        self.liquid_volume = self.liquid_specific_volume * self.liquid_total_molecount

        # print("Error volume", (self.gas_volume + self.liquid_volume - self.volume) / self.volume )

        if any(x < 0 for x in self.liquid_fractions) or any(x < 0 for x in self.gas_fractions):
            raise ValueError("Negative mole fractions calculated in VT flash.")
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
        # print("VT Flash Results:", results)

        

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

