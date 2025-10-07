from parameters import *
import warnings
from typing import Callable

def bar_to_Pa(p_bar):
    return p_bar * 1e5

class Species:
    def __init__(self, name, molar_mass, density=None):
        self.name = name
        self.molar_mass = molar_mass  # kg/mol
        self.density = density        # kg/m3 (optional, only for liqs)

class System:
    next_tanks: list['Tank']
    cellcount: int
    def __init__(self):
        self.tanks = list()
        self.next_tanks = list()
        self.cellcount = None # set to 0?

    def add_tank(self, tank):
        self.next_tanks.append(tank)
        self.tanks.append(tank)
    
    def reload_tanks(self):
        """
        update the old_tank values to be 
        equal to the current tank state.
        """
        self.tanks = list()
        for tank in self.next_tanks:
            self.tanks.append(tank)

    def update_state(self):
        for tank in self.next_tanks:
            tank.update_mole_balance()
        self.reload_tanks()

    def log_state(self):
        pass


class Tank:
    def __init__(self, system, volume, temperature, pressure):
        self.system = system

        self.volume = volume  # m3
        self.temperature = temperature  # K
        self.pressure = pressure  # Pa

        self.liquid_mol = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.liquid_mass = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.liquid_vol = 0

        self.gas_mol = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.gas_mass = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.gas_vol = 0
        
        self.influents = list()
        self.effluents = list()

    def add_influent(self, influent: Callable) -> None:
        self.influents.append(influent)

    def add_effluent(self, effluent: Callable) -> None:
        self.effluents.append(effluent)


    def log_state(self):
        pass

    # Mole balance --------------------------------------------
    def update_mole_balance(self):
        """
        Compute everything ✨
        """
        influents = self.compute_influents()
        effluents = self.compute_effluents()
        for phase in ["liquid", "gas"]:
            for species in ["H2O", "H2", "O2"]:
                self.species[phase][species] = influents[phase][species] - effluents[phase][species]

    def compute_influents(self) -> dict:
        """
        Compute all influent mole balances
        """
        influent_sum = {"H2O": 0, "O2": 0, "H2": 0}
        for influent_function in self.influents:
            influent = influent_function(self)
            for key in influent_sum.keys():
                influent_sum[key] += influent[key]
        return influent_sum
    
    def compute_effluents(self) -> dict:
        """
        Compute all effluent mole balances
        """
        liquids = {"H2O": 0, "O2": 0, "H2": 0}
        gases = liquids.copy()
        effluent_sum = {"liquid": liquids, "gas": gases}
        for effluent_function in self.effluents:
            effluent = effluent_function(self)
            for phase in effluent_sum.keys():
                for key in phase.keys():
                    effluent_sum[phase][key] += effluent[phase][key]
        return effluent_sum
    


if __name__ == "__main__":
    system = System()
    tank = Tank(system, 1.0, 300, 1e5)
    print(tank.liq_mol)





""" OLD TANK METHODS, TO BE DELETED LATER


    # LEVELS --------------------------------------------------------
    def update_levels(self): 

        # self.liq_mol = self.find_liq_mol()
        self.liq_mass = self.find_liq_mass()
        self.liq_vol = self.find_liq_volume()
        
        # self.gas_mol = self.find_gas_mol()
        self.gas_mass = self.find_gas_mass()
        self.gas_vol = self.find_gas_volume()
        print(self.gas_vol)

        self.pressure = self.find_tank_pressure()

    # liq ----------------------------------------------------
    def find_liq_mass(self):
        
        Finds mass of liqs in tank.
        :param Tank: Tank Object
        :return liq_mass: dict of mass of liqs in tank [kg]
        
        liq_mass = {
            name: mol * sp.molar_mass
            for name, mol in self.liq_mol.items() # name, mol = key, val
            for sp in [self.species[name]]
        }
        return liq_mass
    
    def find_liq_volume(self):
        
        Finds volume of liqs in tank. 
        :param Tank: Tank Object
        :return liq_vol: dict of volume of liqs in tank [m3]
        
        liq_vol = self.liq_mol["H2O"] * self.species["H2O"].density
        return liq_vol

    # GAS -------------------------------------------------------
    def find_gas_mass(self):
        
        Finds gas masses in tank.
        :param self: Tank Object
        :return gas_mas: dict of mass of gasses in tank [kg]
        
        gas_mass = {
            name: mol * self.species[name].molar_mass
            for name, mol in self.gas_mol.items()}
        return gas_mass

    def find_gas_volume(self):
        
        Finds gas volume in tank.
        :param self: Tank Object
        :return gas_volume: volume of gasses in tank [m3]
        
        # Gases mixed together, makes little sense to separate them
        return self.volume - self.liq_vol

    # PRESSURE FUNCTIONS --------------------------------------------
    def find_tank_pressure(self):
        
        Finds total tank pressure.
        :param self: Tank Object
        :return tank_pressure: pressure in tank [Pa]  
        
        mol = sum(self.gas_mol.values())
        p = mol * IDEAL_GAS_CONSTANT * self.temperature / self.gas_vol
        return p

    def find_saturation_pressure(self):
        
        Finds saturation pressure of water at temperature T using Antoine equation. 
        :param self: Tank Object 
        :returns p_H2O_sat: Saturation pressure of water [Pa]
        
        T = self.temperature
        H2O = self.species["H2O"]

        if not (MIN_TANK_PRESSURE <= self.pressure <= MAX_TANK_PRESSURE):
            warnings.warn(f"Tank pressure {self.pressure} out of Antoine equation range (0.01–16 bar)", UserWarning)
        if not (MIN_TANK_TEMPERATURE <= T <= MAX_TANK_TEMPERATURE):
            warnings.warn("Tank temperature out of Antoine equation range (273.2–473.2 K)", UserWarning)

        # unpack Antoine coefficients
        A = ANTOINE_A
        B = ANTOINE_B
        C = ANTOINE_C

        log10_pH2O_sat = A - B / (C + T)

        p_H2O_sat = 10 ** (log10_pH2O_sat / VALVE_SCALING_PRESSURE)  # Pa
        return p_H2O_sat

    def find_gas_partial_pressure(self):
        
        Finds partial pressure of gas in tank using sum of gases law.
        :param Tank: Tank Object
        :returns p_gas: Partial pressure of gas in tank [Pa]
        
        sat_p = self.find_saturation_pressure()  
        if sat_p >= self.pressure:
            warnings.warn("Result could be inaccurate: Saturation pressure exceeds tank pressure, water vaporization present. ", UserWarning)
            return 0
        return self.pressure - sat_p

"""