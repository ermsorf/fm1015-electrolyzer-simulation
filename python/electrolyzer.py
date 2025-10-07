from objects import System, Tank

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
        self.generation["O2"] = 0

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