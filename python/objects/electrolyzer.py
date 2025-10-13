# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd()); print(os.getcwd())

from objects import Mols
from parameters import *
from warnings import warn

class Electrolyzer:

    def __init__(self, anode: 'Tank', cathode: 'Tank'):
        self.anode = anode
        self.cathode = cathode 
        self.anode_count = Mols()
        self.cathode_count = Mols()
        self.ipp = float()
        self.step_completed = False # In the future, reset this on global step


    # Update electrolyzer state
    def step(self):
        if self.step_completed: return
        self.set_ipp()
        self.generation()
        self.drag()
        self.hydrogen_diffusion()
        self.oxygen_diffusion()
        self.step_completed = True

    def reset_frame(self):
        self.step_completed = False

    def _set_ipp(self, ipp):
        self.ipp = ipp

    def set_ipp(self):
        ipp = IPP_BASE_VALUE
        if self.anode.system.time >= IPP_HEAVYSIDE_TIME:
            ipp -= IPP_HEAVYSIDE_STEP
        self._set_ipp(ipp)
        

    # read state:
    def get_counts_anode(self):
        assert self.step_completed, "Tried to access values without updating electrolyzer state"
        return self.anode_count

    def get_counts_cathode(self):
        assert self.step_completed, "Tried to access values without updating electrolyzer state"
        return self.cathode_count
        

    # Update mole counts
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


    # Compute electrolyzer generations
    def generation(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        stochiometric_vector = STOICHIOMETRIC_MATRIX / ELECTRON_STOICHIOMETRIC_MATRIX
        electrolyzer_properties = ELECTROLYZER_CELL_COUNT * MEMBRANE_AREA_SUPERFICIAL
        electric_properties = self.ipp * electrolyzer_properties / FARADAY_CONSTANT
        mols = Mols()
        # TODO check if sp is liquid or gas @Fredrik/group
        for stochiometric_coefficient, sp in zip(stochiometric_vector, ["GH2O", "GH2","GO2"]):
            mols[sp] = stochiometric_coefficient*electric_properties
        self.anode_generation(mols) # double-check sign in simulation

    def water_diffusion(self):
        raise NotImplementedError("Water diffusion does not occur!")

    def hydrogen_diffusion(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        membrane_size = MEMBRANE_AREA_SUPERFICIAL / MEMBRANE_THICKNESS
        membrane_properties = ELECTROLYZER_CELL_COUNT*MEMBRANE_PERMEABILITY_H2
        membrane_constant = membrane_size * membrane_properties
        anode_pressure = self.anode.gas_fractions["H2"]*self.anode.pressure
        cathode_pressure = self.cathode.gas_fractions["H2"]*self.cathode.pressure
        # TODO check that pressure & flow direction makes sense @Petter
        delta_p = cathode_pressure - anode_pressure
        diffusion = membrane_constant*delta_p
        mols = Mols(GH2 = diffusion)
        self.cathode_send_to_anode(mols)

    def oxygen_diffusion(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        """compute oxygen diffusion and send to cathode"""
        membrane_size = MEMBRANE_AREA_SUPERFICIAL / MEMBRANE_THICKNESS
        membrane_properties = ELECTROLYZER_CELL_COUNT*MEMBRANE_PERMEABILITY_O2
        membrane_constant = membrane_size * membrane_properties
        anode_pressure = self.anode.gas_fractions["O2"]*self.anode.pressure
        cathode_pressure = self.cathode.gas_fractions["O2"]*self.cathode.pressure
        # TODO check that pressure & flow direction makes sense @Petter
        delta_p = anode_pressure - cathode_pressure 
        diffusion = membrane_constant*delta_p
        mols = Mols(GO2 = diffusion)
        self.anode_send_to_cathode(mols)

    # TODO double check the formula
    def drag(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        DRAG_BIAS = 0.3e-1
        DRAG_SCALING_FACTOR = 1.34e-2
        drag_efficiency = DRAG_BIAS + DRAG_SCALING_FACTOR*self.anode.temperature 
        drag_capacity = drag_efficiency * (MEMBRANE_AREA_SUPERFICIAL / FARADAY_CONSTANT) * self.ipp
        fractions = self.anode.liquid_fractions
        out = Mols()
        for fraction, sp in zip(fractions, ["LH2O", "LH2","LO2"]):
            out[sp] = fraction*drag_capacity*ELECTROLYZER_CELL_COUNT
        self.anode_send_to_cathode(out) # TODO Check flow directions 

if __name__ == "__main__":
    from objects.tank import Tank