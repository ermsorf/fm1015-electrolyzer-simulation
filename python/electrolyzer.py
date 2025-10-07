from objects import System, Tank
from parameters import *
from enum import Enum

class DIRECTION(Enum):
    """
    Assuming flow FROM anode TO cathode
    --> Anode generation is negative, cathode generation is positive.
    Negative generation is assumed not lost,
    but transferred to other side (zero-sum).
    """
    A2C = 1
    C2A = -1
    ANODE_TO_CATHODE = 1
    CATHODE_TO_ANODE = -1
    ANODE_GENERATION = -1
    CATHODE_GENERATION = 1
    ANODE_CONSUMPTION = 1
    CATHODE_CONSUMPTION = -1

class Electrolyzer:
    drag: dict
    diffusion: dict
    generation: dict

    def __init__(self, anode: Tank, cathode: Tank):
        self.anode = anode
        self.cathode = cathode 
        self.drag = {"H2O": 0, "H2": 0, "O2": 0}
        self.diffusion = {"H2O": 0, "H2": 0, "O2": 0}
        self.generation = {"H2O": 0, "H2": 0, "O2": 0}
        self.ipp = 0

    def set_ipp(self, ipp):
        self.ipp = ipp
    
    def get_total_flow(self)->dict:
        out = {"H2O": 0, "H2": 0, "O2": 0}
        for key, diffusion, drag, generation in (
            out.keys(), 
            self.diffusion.items(),
            self.drag.items(),
            self.generation.items()
        ):
            out[key] += diffusion[key]
            out[key] += drag[key]
            out[key] += generation[key]
        return out
        

    def get_drag(self) -> dict:
        return self.drag

    def get_diffusion(self) -> dict:
        return self.diffusion

    def get_generation(self) -> dict:
        return self.generation

    def oxygen_generation(self):
        stochiometric_coefficient = STOICHIOMETRIC_MATRIX["O2"] / ELECTRON_STOICHIOMETRIC_MATRIX
        electrolyzer_properties = ELECTROLYZER_CELL_COUNT * MEMBRANE_AREA_SUPERFICIAL
        constant_terms = stochiometric_coefficient * electrolyzer_properties / FARADAY_CONSTANT
        self.generation["O2"] = constant_terms * self.ipp * DIRECTION.ANODE_GENERATION
        

    def hydrogen_generation(self):
        self.generation["H2"] = 0

    def water_generation(self):
        self.generation["H2O"] = 0

    
    def oxygen_diffusion(self):
        self.diffusion["O2"] = 0

    def hydrogen_diffusion(self):
        self.diffusion["H2"] = 0

    def water_diffusion(self):
        self.diffusion["H2O"] = 0


    def oxygen_drag(self):
        self.drag["O2"] = 0

    def hydrogen_drag(self):
        self.drag["H2"] = 0

    def water_drag(self):
        self.drag["H2O"] = 0