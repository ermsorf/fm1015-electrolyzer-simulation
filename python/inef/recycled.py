from python.objects.tank import Tank
from python.objects.mols import Mols
from python.parameters import params as p

def anode_in_recycled(anode_tank):
    """
    Add recycled into anode tank.
    Returns the molar changes for liquid and gas phases.
    """
    cathode_tank = anode_tank.system.cathode
    result = recycled(cathode_tank)
    # print("Recycled to anode (mol/s):", result)
    return result

def cathode_out_recycled(cathode_tank):
    """
    Remove recycled from cathode tank.
    Returns the molar changes for liquid and gas phases.
    """
    result = recycled(cathode_tank)
    # print("Recycled from cathode (mol/s):", result)
    print
    return result


def recycled(tank):
    """
    Compute recycled cathode effluent mol balance rates
    """
    # Calculate cathode mass rate (kg/s)
    cathode_mass_rate = cathode_mass_rate_pump(tank)
    
    if cathode_mass_rate <= 0:
        return Mols()  # No recycling if mass rate is zero or negative
    
    # Assume tank and pump concentrations are identical
    try:
        molar_masses = {"LH2O": p.H2O_MOLAR_MASS, "LH2": p.H2_MOLAR_MASS, "LO2": p.O2_MOLAR_MASS}
        
        # Calculate total mass of liquid in tank
        total_mass = sum([tank.mols[sp] * molar_masses[sp] for sp in molar_masses.keys()])
        
        if total_mass == 0:
            return Mols() # Avoid division by zero
    
    except ZeroDivisionError:
        return Mols()  # Avoid division by zero

    # Calculate mass fractions of each species in the liquid
    H2O_mass_fraction = (tank.mols["LH2O"] * molar_masses["LH2O"]) / total_mass
    H2_mass_fraction = (tank.mols["LH2"] * molar_masses["LH2"]) / total_mass
    O2_mass_fraction = (tank.mols["LO2"] * molar_masses["LO2"]) / total_mass

    # Convert mass flow rates back to molar flow rates
    H2O_molar_flow = (H2O_mass_fraction * cathode_mass_rate) / molar_masses["LH2O"]
    H2_molar_flow = (H2_mass_fraction * cathode_mass_rate) / molar_masses["LH2"]
    O2_molar_flow = (O2_mass_fraction * cathode_mass_rate) / molar_masses["LO2"]

    return Mols(LH2O = H2O_molar_flow, LO2 = O2_molar_flow, LH2 = H2_molar_flow)

def cathode_mass_rate_pump(tank):
    """md_p__cr. Compute the mass flow rate of the cathode pump. """
    # Calculate actual liquid volume in tank (convert mols to volume)
    liquid_volume_actual = tank.mols["LH2O"] * p.H2O_MOLAR_MASS / p.H2O_DENSITY  # m3
    liquid_volume_target = p.CATHODE_LIQUID_VOLUME_TARGET  # m3
    volume_error = liquid_volume_actual - liquid_volume_target  # m3
    print(f"Cathode tank volume error: {volume_error:.6f} m3")
    
    # Only pump out when liquid level is above target (positive volume error)
    # Mass flow rate should be proportional to how much above target we are
    if volume_error > 0:
        mass_rate_actual = p.CATHODE_SEPARATOR_CONTROLLER_GAIN * volume_error * p.H2O_DENSITY  # kg/s
    else:
        mass_rate_actual = 0  # No pumping when below or at target
    return mass_rate_actual




        