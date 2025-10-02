from parameters import *
import warnings

def bar_to_Pa(p_bar):
    return p_bar * 1e5

class Species:
    mole_count: float
    molar_mass: float
    mass: float
    def __init__(self):
        self.mole_count = None
        self.mass = None
class Water(Species):
    def __init__(self):
        self.molar_mass = H2O_MOLAR_MASS
class Oxygen(Species):
    molar_mass: float
    def __init__(self):
        self.molar_mass = O2_MOLAR_MASS
class Hydrogen(Species):
    molar_mass: float
    def __init__(self):
        self.molar_mass = H2_MOLAR_MASS
class Phase:
    water: Water
    oxygen: Oxygen
    hydrogen: Hydrogen
    volume: float
    mass: float
    species: Species
    def __init__(self):
        self.water = Water()
        self.hydrogen = Hydrogen()
        self.oxygen = Oxygen()
        self.species = [self.water, self.hydrogen,self.oxygen]
        self.volume = None
        self.mass = None
    def refresh_mass(self):
        self.mass = self.water.mass + self.hydrogen.mass + self.oxygen.mass

class Gas(Phase):
    def __init__(self):
        super().__init__()
class Liquid(Phase):
    density: float
    def __init__(self):
        super().__init__()
        self.density = H2O_DENSITY

class System:
    tanks: list['Tank']
    cellcount: int
    def __init__(self):
        self.tanks = list()
        self.cellcount = None # set to 0?

    def add_tank(self, tank):
        self.tanks.append(tank)

    def log_state(self):
        pass


class Tank:
    def __init__(self, system, volume, temperature, pressure):
        self.system = system
        self.liquid = Liquid()
        self.gas = Gas()
        self.volume = volume  # m3
        self.temperature = temperature  # K
        self.pressure = pressure  # Pa

    def log_state(self):
        pass

    # LEVELS --------------------------------------------------------
    def update_levels(self): 
        """"
        Docstring to be added
        """

        # self.liquid_mol = self.find_liquid_mol()
        self.liquid_mass = self.find_liquid_mass()
        self.liquid_vol = self.find_liquid_volume()
        
        # self.gas_mol = self.find_gas_mol()
        self.gas_mass = self.find_gas_mass()
        self.gas_vol = self.find_gas_volume()
        print(self.gas_vol)

        self.pressure = self.find_tank_pressure()

    # LIQUID ----------------------------------------------------
    def find_liquid_mass(self):
        """
        Finds mass of liquids in tank.
        :param Tank: Tank Object
        :return liquid_mass: dict of mass of liquids in tank [kg]
        """
        for liquid in self.liquid.species:
            liquid: Species
            liquid.mass = liquid.mole_count * liquid.molar_mass
        self.liquid.refresh_mass()
        
        return self.liquid.mass
    
    def find_liquid_volume(self):
        """
        Finds volume of liquids in tank. 
        :param Tank: Tank Object
        :return liquid_vol: dict of volume of liquids in tank [m3]
        """
        self.liquid.volume = self.liquid.density + self.liquid.water.molar_mass
        # TODO expand to all liquids if task desires it?
        return self.liquid.volume


    # GAS -------------------------------------------------------
    def find_gas_mass(self):
        """
        Finds gas masses in tank.
        :param self: Tank Object
        :return gas_mas: dict of mass of gasses in tank [kg]
        """
        for gas in self.gas.species:
            gas: Species
            gas.mass = gas.mole_count * gas.molar_mass
        self.gas.refresh_mass()
        return self.gas.mass

    def find_gas_volume(self):
        """
        Finds gas volume in tank.
        :param self: Tank Object
        :return gas_volume: volume of gasses in tank [m3]
        """
        # Gases mixed together, makes little sense to separate them
        self.gas.volume = self.volume - self.liquid.volume
        return self.gas.volume

    # PRESSURE FUNCTIONS --------------------------------------------
    def find_tank_pressure(self):
        """
        Finds total tank pressure.
        :param self: Tank Object
        :return tank_pressure: pressure in tank [Pa]  
        """
        mol = 0
        for species in self.gas.species:
            mol += species.mass
        p = mol * IDEAL_GAS_CONSTANT * self.temperature / self.gas.volume
        return p


    def find_saturation_pressure(self):
        """
        Finds saturation pressure of water at temperature T using Antoine equation. 
        :param self: Tank Object 
        :returns p_H2O_sat: Saturation pressure of water [Pa]
        """
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
        """
        Finds partial pressure of gas in tank using sum of gases law.
        :param Tank: Tank Object
        :returns p_gas: Partial pressure of gas in tank [Pa]
        """
        sat_p = self.find_saturation_pressure()  
        if sat_p >= self.pressure:
            warnings.warn("Result could be inaccurate: Saturation pressure exceeds tank pressure, water vaporization present. ", UserWarning)
            return 0
        return self.pressure - sat_p