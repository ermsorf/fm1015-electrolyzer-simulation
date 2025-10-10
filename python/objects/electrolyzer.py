# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd()); print(os.getcwd())


from .mols import Mols
from .system import System
from .tank import Tank
from parameters import *

class Electrolyzer:
    drag: dict
    diffusion: dict
    generation: dict

    def __init__(self, anode: Tank, cathode: Tank):
        self.anode = anode
        self.cathode = cathode 
        self.anode_count = Mols()
        self.cathode_count = Mols()
        self.ipp = 0
    
    def set_ipp(self, ipp):
        self.ipp = ipp

    # Update mole counts:
    def push_vales(self):
        # TODO find out how the mole phase distribution works
        #self.anode.[liq/gas]_mol +=self.anode_count
        #self.cathode.[liq/gas]_mol +=self.cathode_count
        ...

    def anode_send_to_cathode(self, ammount: Mols):
        self.cathode_generation(ammount)
        self.anode_consumption(ammount)
    def anode_generation(self, ammount: Mols):
        self.anode_count += ammount
    def anode_consumption(self, ammount: Mols):
        self.anode_count -=ammount

    def cathode_send_to_anode(self, ammount: Mols):
        self.anode_generation(ammount)
        self.cathode_consumption(ammount)
    def cathode_generation(self, ammount: Mols):
        self.cathode_count += ammount
    def cathode_consumption(self, ammount: Mols):
        self.cathode_count -= ammount

    def oxygen_generation(self):
        stochiometric_coefficient = STOICHIOMETRIC_MATRIX["O2"] / ELECTRON_STOICHIOMETRIC_MATRIX
        electrolyzer_properties = ELECTROLYZER_CELL_COUNT * MEMBRANE_AREA_SUPERFICIAL
        constant_terms = stochiometric_coefficient * electrolyzer_properties / FARADAY_CONSTANT
        generation = constant_terms*self.ipp
        mols = Mols(O2 = generation)
        self.anode_generation(mols)

    def hydrogen_generation(self):
        self.generation["H2"] = 0

    def water_generation(self):
        self.generation["H2O"] = 0

    
    def oxygen_diffusion(self):
        """compute oxygen diffusion and send to cathode"""
        # use pressure "absolute value":
        # Negative flow in base formula
        # implies flow from anode to cathode.
        # (explicitly: stating negative flow cathode -> anode)
        # This is handled by flow direction instead of sign.
        # -AT
        membrane_size = MEMBRANE_AREA_SUPERFICIAL / MEMBRANE_THICKNESS
        membrane_properties = ELECTROLYZER_CELL_COUNT*MEMBRANE_PERMEABILITY_O2
        membrane_constant = membrane_size * membrane_properties
        cathode_pressure = self.cathode.pressure # CHECK
        anode_pressure = self.anode.pressure # CHECK
        delta_p = cathode_pressure - anode_pressure 
        diffusion = membrane_constant*delta_p
        mols = Mols(O2 = diffusion)
        self.anode_send_to_cathode(mols)

    def hydrogen_diffusion(self):
        membrane_size = MEMBRANE_AREA_SUPERFICIAL / MEMBRANE_THICKNESS
        membrane_properties = ELECTROLYZER_CELL_COUNT*MEMBRANE_PERMEABILITY_H2
        membrane_constant = membrane_size * membrane_properties
        cathode_pressure = self.cathode.pressure # CHECK
        anode_pressure = self.anode.pressure # CHECK
        delta_p = cathode_pressure - anode_pressure
        diffusion = membrane_constant*delta_p
        mols = Mols(H2 = diffusion)
        self.cathode_send_to_anode(mols)

    def water_diffusion(self):
        raise NotImplementedError("Water diffusion does not occur!")


    def oxygen_drag(self):
        self.drag["O2"] = 0

    def hydrogen_drag(self):
        self.drag["H2"] = 0

    def water_drag(self):
        self.drag["H2O"] = 0