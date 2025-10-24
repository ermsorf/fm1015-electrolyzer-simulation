# # PARAMETERS

class Parameters:

    def add_system(self, system):
        self.system = system

    def __init__(self):
        # self.SYSTEM_TEMPERATURE = 273.15 + 60

        self.MEMBRANE_PERMEABILITY_H2 = 5.31e-14  # mol/s/m/Pa
        self.MEMBRANE_PERMEABILITY_O2 = 2.26e-14  # mol/s/m/Pa
        self.MEMBRANE_AREA_SUPERFICIAL = 90e-4 # m2
        self.MEMBRANE_THICKNESS = 200e-6  # m

        self.ANODE_SEPARATOR_VOLUME = 0.030 # m3
        # self.ANODE_LIQUID_VOLUME_TARGET = self.ANODE_SEPARATOR_VOLUME / 3 # m3
        self.ANODE_REFERENCE_INJECTION = 3.17e-2 # mol/s
        self.ANODE_SEPARATOR_CONTROLLER_GAIN = 10**3 # -
        self.ANODE_EXTERNAL_PRESSURE = 1e5

        self.CATHODE_SEPARATOR_VOLUME = 0.005 # m3
        # self.CATHODE_LIQUID_VOLUME_TARGET = self.CATHODE_SEPARATOR_VOLUME / 3 # m3
        self.CATHODE_SEPARATOR_CONTROLLER_GAIN = 20 # - 
        # self.CATHODE_EXTERNAL_PRESSURE = 25e5
        self.REFERENCE_MASS_EJECTION = 5.1e-3  # kg/s 0.003848955975614166

        self.ELECTROLYZER_CELL_COUNT = 34

        self.STOICHIOMETRIC_MATRIX = {"H2O":-2,"H2":2, "O2":1}
        self.ELECTRON_STOICHIOMETRIC_MATRIX = 4

        self.VALVE_SCALING_PRESSURE = 1e5  # Pa
        self.VALVE_SCALING_GAS_DENSITY = 1  # kg/m3
        self.VALVE_CAPACITY_ANODE_EFFLUENT = None # Find in problem 7 , 2.4e-3
        self.VALVE_CAPACITY_CATHODE_EFFLUENT = None # Find in problem 8, 4.4e-5

        # Heavyside-function state changes
        self.IPP_BASE_VALUE = 2e-1 # A/m2
        self.IPP_HEAVYSIDE_TIME = 2 # 5*60 # s
        self.IPP_HEAVYSIDE_STEP = -0.5e-1 #A/m2

        # CONSTANTS
        self.IDEAL_GAS_CONSTANT = 8.314  # J/mol/K
        self.FARADAY_CONSTANT = 9.648e4  # C/mol

        self.H2O_MOLAR_MASS = 18e-3  # kg/mol
        self.H2O_DENSITY = 1000  # kg/m3
        self.H2O_ANTOINE = 5.11564 # VALID FROM 273.20 - 473.20 K and 1000 - 1600000 Pa

        self.H2_MOLAR_MASS = 2e-3  # kg/mol
        self.O2_MOLAR_MASS = 32e-3  # kg/mol

        self.ANTOINE_A = 5.11564 # -
        self.ANTOINE_B = 1687.537 # K
        self.ANTOINE_C = 230.17 # K

        self.MIN_TANK_PRESSURE = 0.01e5 # Pa
        self.MAX_TANK_PRESSURE = 16e5 # Pa
        self.MIN_TANK_TEMPERATURE = 273.2 # K
        self.MAX_TANK_TEMPERATURE = 473.2 # K

    @property
    def SYSTEM_TEMPERATURE(self):
          return 273.15 + 60
          if self.system.time < 60*15:
                return 273.15 + 60
          else:
                return 273.15 + 65
    
    @property
    def CATHODE_EXTERNAL_PRESSURE(self):
            return 25e5
            if self.system.time < 60*10:
                return 25e5
            else:
                return 24.5e5
    
    @property
    def ANODE_LIQUID_VOLUME_TARGET(self):
            return self.ANODE_SEPARATOR_VOLUME / 3 # m3

    @property
    def CATHODE_LIQUID_VOLUME_TARGET(self):
            return self.CATHODE_SEPARATOR_VOLUME / 3 # m3

    @property 
    def IPP(self):
            return 20000
            if self.system.time < 60*5:
                return 20000
            else:
                return 10000
    

params = Parameters()