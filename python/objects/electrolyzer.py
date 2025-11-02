# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd()); print(os.getcwd())

from typing import TYPE_CHECKING
from python.parameters import params as p
from warnings import warn

if TYPE_CHECKING:
    from python.objects.tank import Tank

from python.objects.mols import Mols

class Electrolyzer:

    def __init__(self, anode: 'Tank', cathode: 'Tank'):
        self.anode = anode
        self.cathode = cathode 
        self.anode_count = Mols()
        self.cathode_count = Mols()
        self.step_completed = False # In the future, reset this on global step

        self.functions = [
            self.generation, 
            self.drag, 
            self.hydrogen_diffusion, 
            self.oxygen_diffusion
            ]
        
        self.track_hydrogen_diffusion = []  # For analysis purposes
        self.track_oxygen_diffusion = []
        self.track_drag = []

        self.track_cathode_count = []
        self.track_anode_count = []


    # Update electrolyzer state
    def step(self):
        if self.step_completed: return
        for fun in self.functions:
            fun()
        self.step_completed = True
        self.track_cathode_count.append(self.cathode_count)
        self.track_anode_count.append(self.anode_count)

    def reset_frame(self):
        self.anode_count = Mols()
        self.cathode_count = Mols()
        self.step_completed = False
        

    # read state:
    def get_counts_anode(self):
        assert self.step_completed, "Tried to access values without updating electrolyzer state"
        return self.anode_count

    def get_counts_cathode(self):
        assert self.step_completed, "Tried to access values without updating electrolyzer state"
        return self.cathode_count
        

    # Update mole counts
    def anode_send_to_cathode(self, amount: Mols):
        self.cathode_generation(amount)
        self.anode_consumption(amount)

    def anode_generation(self, amount: Mols):
        self.anode_count += amount

    def anode_consumption(self, amount: Mols):
        self.anode_count -= amount

    def cathode_send_to_anode(self, amount: Mols):
        self.anode_generation(amount)
        self.cathode_consumption(amount)

    def cathode_generation(self, amount: Mols):
        self.cathode_count += amount

    def cathode_consumption(self, amount: Mols):
        self.cathode_count -= amount


    # Compute electrolyzer generations
    def generation(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        stochiometric_vector = [p.STOICHIOMETRIC_MATRIX[sp]/p.ELECTRON_STOICHIOMETRIC_MATRIX for sp in p.STOICHIOMETRIC_MATRIX.keys()]
        electrolyzer_properties = p.ELECTROLYZER_CELL_COUNT * p.MEMBRANE_AREA_SUPERFICIAL
        electric_properties = p.IPP * electrolyzer_properties / p.FARADAY_CONSTANT
        mols = Mols()
        # TODO check if sp is liquid or gas @Fredrik/group 
        for stochiometric_coefficient, sp in zip(stochiometric_vector, ["LH2O", "GH2","GO2"]):
            mols[sp] = stochiometric_coefficient*electric_properties
        # Logic: Generate all elements in anode --> send H2 component to cathode
        self.anode_generation(mols) # double-check sign in simulation
        transfer = Mols(GH2 = mols["GH2"])
        self.anode_send_to_cathode(transfer)

    def water_diffusion(self):
        raise NotImplementedError("Water diffusion does not occur!")

    def hydrogen_diffusion(self, track=False):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        membrane_size = p.MEMBRANE_AREA_SUPERFICIAL / p.MEMBRANE_THICKNESS
        membrane_properties = p.ELECTROLYZER_CELL_COUNT * p.MEMBRANE_PERMEABILITY_H2
        membrane_constant = membrane_size * membrane_properties

        # NOTE: H2 is index 1 in gas fractions, I DONT LIKE THIS
        anode_pressure = self.anode.gas_fractions[1]*self.anode.pressure # H2 is index 1 in gas fractions.
        cathode_pressure = self.cathode.gas_fractions[1]*self.cathode.pressure # H2 is index 1 in gas fractions
        # TODO check that pressure & flow direction makes sense @Petter
        delta_p = cathode_pressure - anode_pressure
        diffusion = membrane_constant*delta_p
        mols = Mols(GH2 = diffusion)
        self.cathode_send_to_anode(mols)
        # Track diffusion for analysis, REMOVE LATER
        self.track_hydrogen_diffusion.append(mols)

    def oxygen_diffusion(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        """compute oxygen diffusion and send to cathode"""
        membrane_size = p.MEMBRANE_AREA_SUPERFICIAL / p.MEMBRANE_THICKNESS
        membrane_properties = p.ELECTROLYZER_CELL_COUNT * p.MEMBRANE_PERMEABILITY_O2
        membrane_constant = membrane_size * membrane_properties
        # NOTE: O2 is index 2 in gas fractions, I DONT LIKE THIS
        anode_pressure = self.anode.gas_fractions[2]*self.anode.pressure
        cathode_pressure = self.cathode.gas_fractions[2]*self.cathode.pressure
        # TODO check that pressure & flow direction makes sense @Petter
        delta_p = anode_pressure - cathode_pressure 
        diffusion = membrane_constant*delta_p
        mols = Mols(GO2 = diffusion)
        self.anode_send_to_cathode(mols)
        # Track diffusion for analysis, REMOVE LATER
        self.track_oxygen_diffusion.append(mols)

    # TODO double check the formula
    def drag(self):
        if self.step_completed:
            warn("Called electrolyzer twice")
            return
        
        if p.drag_formula == "suermann":
            DRAG_BIAS = -3 # 0.03
            DRAG_SCALING_FACTOR = 1.82e-2
        else: # drag formula == onda
            DRAG_BIAS = 0.03
            DRAG_SCALING_FACTOR = 1.34e-2
        drag_efficiency = DRAG_BIAS + DRAG_SCALING_FACTOR*self.anode.temperature 
        drag_capacity = drag_efficiency * (p.MEMBRANE_AREA_SUPERFICIAL / p.FARADAY_CONSTANT) * p.IPP
        fractions = self.anode.liquid_fractions
        out = Mols()
        for fraction, sp in zip(fractions, ["LH2O", "LH2","LO2"]):
            out[sp] = fraction*drag_capacity*p.ELECTROLYZER_CELL_COUNT
        self.anode_send_to_cathode(out) # TODO Check flow directions 
        # Track drag for analysis, REMOVE LATER
        self.track_drag.append(out)

if __name__ == "__main__":
    from objects.tank import Tank
