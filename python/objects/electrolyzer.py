# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd()); print(os.getcwd())


from objects import System, Tank, Mols
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
    def push_values(self):
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

    # TODO check if these should be implemented
    def water_generation(self):
        pass

    def hydrogen_generation(self):
        pass

    def oxygen_generation(self):
        stochiometric_coefficient = STOICHIOMETRIC_MATRIX["O2"] / ELECTRON_STOICHIOMETRIC_MATRIX
        electrolyzer_properties = ELECTROLYZER_CELL_COUNT * MEMBRANE_AREA_SUPERFICIAL
        constant_terms = stochiometric_coefficient * electrolyzer_properties / FARADAY_CONSTANT
        generation = constant_terms*self.ipp
        mols = Mols(GO2 = generation)
        self.anode_generation(mols)

    def water_diffusion(self):
        raise NotImplementedError("Water diffusion does not occur!")

    def hydrogen_diffusion(self):
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

    # TODO look over these to look for følgefeil
    def water_drag(self):
        DRAG_BIAS = 0.3e-1
        DRAG_SCALING_FACTOR = 1.34e-2
        drag_efficiency = DRAG_BIAS + DRAG_SCALING_FACTOR*self.anode.temperature 
        drag_capacity = drag_efficiency * (MEMBRANE_AREA_SUPERFICIAL / FARADAY_CONSTANT) * self.ipp
        H2O_INDEX = 0
        water_fraction = self.anode.liquid_fractions[H2O_INDEX]
        drag = water_fraction*drag_capacity*ELECTROLYZER_CELL_COUNT
        out = Mols(LH2O=drag)
        self.anode_send_to_cathode(out)

        
    def hydrogen_drag(self):
        DRAG_BIAS = 0.3e-1
        DRAG_SCALING_FACTOR = 1.34e-2
        drag_efficiency = DRAG_BIAS + DRAG_SCALING_FACTOR*self.anode.temperature 
        drag_capacity = drag_efficiency * (MEMBRANE_AREA_SUPERFICIAL / FARADAY_CONSTANT) * self.ipp
        H2_INDEX = 1
        hydrogen_fraction = self.anode.liquid_fractions[H2_INDEX]
        drag = hydrogen_fraction*drag_capacity*ELECTROLYZER_CELL_COUNT
        out = Mols(LH2=drag)
        self.anode_send_to_cathode(out)

    def oxygen_drag(self):
        DRAG_BIAS = 0.3e-1
        DRAG_SCALING_FACTOR = 1.34e-2
        drag_efficiency = DRAG_BIAS + DRAG_SCALING_FACTOR*self.anode.temperature 
        drag_capacity = drag_efficiency * (MEMBRANE_AREA_SUPERFICIAL / FARADAY_CONSTANT) * self.ipp
        O2_INDEX = 2
        oxygen_fraction = self.anode.liquid_fractions[O2_INDEX]
        drag = oxygen_fraction*drag_capacity*ELECTROLYZER_CELL_COUNT
        out = Mols(LO2=drag)
        self.anode_send_to_cathode(out)