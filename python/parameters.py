# # PARAMETERS

class Parameters:

    def add_system(self, system):
        self.system = system

    def __init__(self):

        # self.SYSTEM_TEMPERATURE = 273.15 + 60
        self.BAR_TO_PA = 1e5
        self.PA_TO_BAR = 1/self.BAR_TO_PA
        self.KELVIN_TO_CELSIUS = 273.15
        self.CELSIUS_TO_KELVIN = -self.KELVIN_TO_CELSIUS
        self.ATM_TO_PA = 101325
        self.PA_TO_ATM = 1/self.ATM_TO_PA

        # self.SYSTEM_TEMPERATURE = 60 + self.CELSIUS_TO_KELVIN
        
        self.CELSIUS_TO_KELVIN = 273.15
        self.KELVIN_TO_CELSIUS = -self.CELSIUS_TO_KELVIN
        self.BAR_TO_PA = 1e5
        self.ATM_TO_PA = 101325
        self.PA_TO_ATM = 1/self.ATM_TO_PA
        self.PA_TO_BAR = 1/self.BAR_TO_PA

        self.MEMBRANE_PERMEABILITY_H2 = 5.31e-14  # mol/s/m/Pa
        self.MEMBRANE_PERMEABILITY_O2 = 2.26e-14  # mol/s/m/Pa
        self.MEMBRANE_AREA_SUPERFICIAL = 90e-4 # m2
        self.MEMBRANE_THICKNESS = 200e-6  # m

        self.ANODE_SEPARATOR_VOLUME = 0.030 # m3
        self.ANODE_LIQUID_VOLUME_TARGET = self.ANODE_SEPARATOR_VOLUME / 3 # m3
        self.ANODE_REFERENCE_INJECTION = 0.03171641791044776 # 3.17e-2 # mol/s
        self.ANODE_SEPARATOR_CONTROLLER_GAIN = 10**3 # -
        self.ANODE_EXTERNAL_PRESSURE = 1*self.BAR_TO_PA
        self.ANODE_VALVE_MASS_FLOW_CAPACITY = 2.1667e-3

        self.CATHODE_SEPARATOR_VOLUME = 0.005 # m3
        self.CATHODE_LIQUID_VOLUME_TARGET = self.CATHODE_SEPARATOR_VOLUME / 3 # m3
        self.CATHODE_SEPARATOR_CONTROLLER_GAIN = 20 # - 
        # self.CATHODE_EXTERNAL_PRESSURE = 25e5 * self.BAR
        self.CATHODE_REFERENCE_MASS_EJECTION = 5.1e-3  # kg/s 
        self.CATHODE_VALVE_MASS_FLOW_CAPACITY = 4.334e-5

        self.ELECTROLYZER_CELL_COUNT = 34

        self.STOICHIOMETRIC_MATRIX = {"H2O":-2,"H2":2, "O2":1}
        self.ELECTRON_STOICHIOMETRIC_MATRIX = 4

        self.VALVE_SCALING_PRESSURE = 1e5  # Pa
        self.VALVE_SCALING_GAS_DENSITY = 1  # kg/m3
        self.VALVE_CAPACITY_ANODE_EFFLUENT = None # Find in problem 7 , 2.4e-3
        self.VALVE_CAPACITY_CATHODE_EFFLUENT = None # Find in problem 8, 4.4e-5
        self.VALVE_CONTROL_SIGNAL = 0.5 # [0,1]

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

        # Switch dynamic simulation on/off
        self.steadystate = True


    @property
    def SYSTEM_TEMPERATURE(self):
        if self.steadystate:
          return 273.15 + 60
        else:
          if self.system.time < 60*15:
                return 273.15 + 60
          else:
                return 273.15 + 65
    
    @property
    def CATHODE_EXTERNAL_PRESSURE(self):
        if self.steadystate:
            return 25e5
        else:
            if self.system.time < 60*10:
                return 25e5
            else:
                return 24.5e5
    
    @property 
    def IPP(self):
        if self.steadystate:
            return 20000
        else:
            if self.system.time < 60*5:
                return 20000
            else:
                return 10000
    

params = Parameters()



if __name__ == "__main__":
    from numpy import sqrt
    p = params
    # Problem 1
    stoichiometric_matrix = {"H2O":-2,"H2":2, "O2":1}
    electron_stoichiometric_matrix = 4

    # Problem 2
    # Molar amounts of liquid in tanks
    M_h2o = p.H2O_MOLAR_MASS
    rho_h2o = p.H2O_DENSITY
    anode_water_amount = 1/3 * p.ANODE_SEPARATOR_VOLUME * rho_h2o / M_h2o
    cathode_water_amount = 1/3 * p.CATHODE_SEPARATOR_VOLUME * rho_h2o / M_h2o

    print("\33[30mProblem 2\33[0m")
    print("Anode H2O mols: ", anode_water_amount)
    print("Cathode H2O mols: ", cathode_water_amount)

    # Problem 3
    A = p.ANTOINE_A
    B = p.ANTOINE_B
    C = p.ANTOINE_C

    # anode
    p_a = 1.2e5
    p_a_h20_sat = 1e5 * 10**(A - (B)/(C + (p.SYSTEM_TEMPERATURE - 273.15)))
    p_a_o2 = p_a - p_a_h20_sat

    n_a_o2 = (p_a_o2 * 2/3 * p.ANODE_SEPARATOR_VOLUME)/(p.IDEAL_GAS_CONSTANT * p.SYSTEM_TEMPERATURE)

    # cathode
    p_c = 30e5
    p_c_h2o_sat = p_a_h20_sat
    p_c_h2 = p_c - p_c_h2o_sat

    n_c_h2 = (p_c_h2 * 2/3 * p.CATHODE_SEPARATOR_VOLUME)/(p.IDEAL_GAS_CONSTANT * p.SYSTEM_TEMPERATURE)

    print("\33[31mProblem 3 \33[0m")
    print("Anode GO2 mols: ", n_a_o2)
    print("Cathode GH2 mols: ", n_c_h2)


    # Problem 4
    nd_g_h2o = p.ELECTROLYZER_CELL_COUNT * (p.STOICHIOMETRIC_MATRIX["H2O"]/p.ELECTRON_STOICHIOMETRIC_MATRIX) * (p.MEMBRANE_AREA_SUPERFICIAL * p.IPP)/(p.FARADAY_CONSTANT)
    nd_i_h2o = -nd_g_h2o

    print("\33[32mProblem 4\33[0m")
    print("Water consumption rate: ", nd_g_h2o)
    print("Inlet pump rate: ", nd_i_h2o)

    # Problem 5

    # approx, nd_d = nd_d_h2o

    eta_d = 1.34 * 1e-2 * p.SYSTEM_TEMPERATURE + 0.03
    
    nd_d_h2o = p.ELECTROLYZER_CELL_COUNT * eta_d * (p.MEMBRANE_AREA_SUPERFICIAL * p.IPP)/(p.FARADAY_CONSTANT)
    md_d_h2o = p.H2O_MOLAR_MASS * nd_d_h2o

    md_cr = md_d_h2o

    print("\33[33mProblem 5\33[0m")
    print(f"Drag through membrane: {nd_d_h2o} mol, {md_d_h2o} kg")


    # Problem 6
    nd_g_o2 = (p.STOICHIOMETRIC_MATRIX["O2"]/p.ELECTRON_STOICHIOMETRIC_MATRIX) * p.ELECTROLYZER_CELL_COUNT * (p.MEMBRANE_AREA_SUPERFICIAL * p.IPP)/(p.FARADAY_CONSTANT)
    nd_g_h2 = (p.STOICHIOMETRIC_MATRIX["H2"]/p.ELECTRON_STOICHIOMETRIC_MATRIX) * p.ELECTROLYZER_CELL_COUNT * (p.MEMBRANE_AREA_SUPERFICIAL * p.IPP)/(p.FARADAY_CONSTANT)

    print("\33[34mProblem 6\33[0m")
    print("O2 generation: ", nd_g_o2)
    print("H2 generation: ", nd_g_h2)
    
    # Problem 7
    nd_a_e_o2 = nd_g_o2
    md_a_e_o2 = p.O2_MOLAR_MASS * nd_a_e_o2


    # Upstream gas density
    rho_a = (p.O2_MOLAR_MASS * p_a)/(p.IDEAL_GAS_CONSTANT * p.SYSTEM_TEMPERATURE)

    # ISA valve relation
    delta_p_a = p_a - p.ANODE_EXTERNAL_PRESSURE
    Y_a = 1 - min(1, 2/3 * (delta_p_a/p_a))
    valve_control_signal_a = 0.5
    md_a_e_c = (md_a_e_o2)/(valve_control_signal_a * Y_a * sqrt(delta_p_a / p.VALVE_SCALING_PRESSURE) * sqrt(rho_a / p.VALVE_SCALING_GAS_DENSITY))

    print("\33[35mProblem 7\33[0m")
    print(f"Anode valve capacity: {nd_a_e_o2} mol, {md_a_e_c} kg")

    # Problem 8
    nd_c_e_h2 = nd_g_h2
    md_c_e_h2 = p.H2_MOLAR_MASS * nd_c_e_h2

    # Upstream gas density
    rho_c = (p.H2_MOLAR_MASS * p_c)/(p.IDEAL_GAS_CONSTANT * p.SYSTEM_TEMPERATURE)
    
    # ISA valve relation
    delta_p_c = p_c - p.CATHODE_EXTERNAL_PRESSURE
    Y_c = 1 - min(1, 2/3 * delta_p_c/p_c)

    valve_control_signal_c = 0.5
    md_c_e_c = (md_c_e_h2)/(valve_control_signal_c * Y_c * sqrt(delta_p_c / p.VALVE_SCALING_PRESSURE) * sqrt(rho_c / p.VALVE_SCALING_GAS_DENSITY))
    

    print("\33[36mProblem 8\33[0m")
    print(f"Cathode valve capacity: {nd_c_e_h2} mol, {md_c_e_c} kg")






    

    
