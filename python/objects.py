from parameters import *
import warnings

def bar_to_Pa(p_bar):
    return p_bar * 1e5

class Species:
    def __init__(self, name, molar_mass, density=None):
        self.name = name
        self.molar_mass = molar_mass  # kg/mol
        self.density = density        # kg/m3 (optional, only for liquids)

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
        self.species = {
            "H2O": Species("H2O", H2O_MOLAR_MASS, density=H2O_DENSITY),
            "H2": Species("H2", H2_MOLAR_MASS),
            "O2": Species("O2", O2_MOLAR_MASS)
        }

        self.volume = volume  # m3
        self.temperature = temperature  # K
        self.pressure = pressure  # Pa

        self.liquid_mol = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.liquid_mass = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.liquid_vol = 0

        self.gas_mol = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.gas_mass = {"H2O": 0.0, "O2": 0.0, "H2": 0.0}
        self.gas_vol = 0

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
        liquid_mass = {
            name: mol * sp.molar_mass
            for name, mol in self.liquid_mol.items() # name, mol = key, val
            for sp in [self.species[name]]
        }
        return liquid_mass
    
    def find_liquid_volume(self):
        """
        Finds volume of liquids in tank. 
        :param Tank: Tank Object
        :return liquid_vol: dict of volume of liquids in tank [m3]
        """
        liquid_vol = self.liquid_mol["H2O"] * self.species["H2O"].density
        return liquid_vol


    # GAS -------------------------------------------------------
    def find_gas_mass(self):
        """
        Finds gas masses in tank.
        :param self: Tank Object
        :return gas_mas: dict of mass of gasses in tank [kg]
        """
        gas_mass = {
            name: mol * self.species[name].molar_mass
            for name, mol in self.gas_mol.items()}
        return gas_mass

    def find_gas_volume(self):
        """
        Finds gas volume in tank.
        :param self: Tank Object
        :return gas_volume: volume of gasses in tank [m3]
        """
        # Gases mixed together, makes little sense to separate them
        return self.volume - self.liquid_vol

    # PRESSURE FUNCTIONS --------------------------------------------
    def find_tank_pressure(self):
        """
        Finds total tank pressure.
        :param self: Tank Object
        :return tank_pressure: pressure in tank [Pa]  
        """
        mol = sum(self.gas_mol.values())
        p = mol * IDEAL_GAS_CONSTANT * self.temperature / self.gas_vol
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