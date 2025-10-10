from objects import Tank, System
from objects.mols import Mols
from parameters import (
CATHODE_LIQUID_VOLUME, CATHODE_SEPARATOR_CONTROLLER_GAIN,
SYSTEM_TEMPERATURE,
H2O_DENSITY, H2O_MOLAR_MASS, H2_MOLAR_MASS, O2_MOLAR_MASS
)

def anode_in_recycled(anode_tank):
    """
    Add recycled into anode tank.
    Returns the molar changes for liquid and gas phases.
    """
    return recycled(anode_tank)

def cathode_out_recycled(cathode_tank):
    """
    Remove recycled from cathode tank.
    Returns the molar changes for liquid and gas phases.
    """
    return recycled(cathode_tank)


def recycled(tank):
    """
    Compute recycled cathode effluent mol balance rates
    """
    # Calculate cathode mass rate (kg/s)
    cathode_mass_rate = cathode_mass_rate_pump(tank)
    
    if cathode_mass_rate <= 0:
        return Mols(), Mols() 
    
    # Assume tank and pump concentrations are identical
    try:
        molar_masses = {"H2O": H2O_MOLAR_MASS, "H2": H2_MOLAR_MASS, "O2": O2_MOLAR_MASS}
        
        # Calculate total mass of liquid in tank
        total_mass = sum([tank.liq_mol[sp] * molar_masses[sp] for sp in molar_masses.keys()])
        
        if total_mass == 0:
            return Mols(), Mols()
    
    except ZeroDivisionError:
        return Mols(), Mols()

    # Calculate mass fractions of each species in the liquid
    H2_mass_fraction = (tank.liq_mol["H2"] * molar_masses["H2"]) / total_mass
    O2_mass_fraction = (tank.liq_mol["O2"] * molar_masses["O2"]) / total_mass  
    H2O_mass_fraction = (tank.liq_mol["H2O"] * molar_masses["H2O"]) / total_mass
    
    # Convert mass flow rates back to molar flow rates
    H2_molar_flow = (H2_mass_fraction * cathode_mass_rate) / molar_masses["H2"]
    O2_molar_flow = (O2_mass_fraction * cathode_mass_rate) / molar_masses["O2"]
    H2O_molar_flow = (H2O_mass_fraction * cathode_mass_rate) / molar_masses["H2O"]

    nd__cr = {
        "H2O": H2O_molar_flow,
        "H2": H2_molar_flow,
        "O2": O2_molar_flow 
    }
    mol_l = Mols(O2 = O2_molar_flow, H2 = H2_molar_flow, H2O = H2O_molar_flow)
    mol_g = Mols()

    return mol_l, mol_g

def cathode_mass_rate_pump(tank):
    """md_p__cr. Compute the mass flow rate of the cathode pump. """
    # Calculate actual liquid volume in tank (convert mols to volume)
    liquid_volume_actual = tank.liq_mol["H2O"] * H2O_MOLAR_MASS / H2O_DENSITY  # m3
    liquid_volume_target = CATHODE_LIQUID_VOLUME  # m3
    volume_error = liquid_volume_actual - liquid_volume_target  # m3
    
    # Only pump out when liquid level is above target (positive volume error)
    # Mass flow rate should be proportional to how much above target we are
    if volume_error > 0:
        mass_rate_actual = CATHODE_SEPARATOR_CONTROLLER_GAIN * volume_error * H2O_DENSITY  # kg/s
    else:
        mass_rate_actual = 0  # No pumping when below or at target
    
    return mass_rate_actual


if __name__ == "__main__":
    from objects.tank import initialize_test_tanks
    system, atank, ctank = initialize_test_tanks()
    
    # To test the functions, we can call them and see the returned values
    liq_change, gas_change = cathode_out_recycled(ctank)
    print("Molar change from cathode recycled:", liq_change, gas_change)

    # To apply the changes, you would do something like this:
    ctank.add_effluent(cathode_out_recycled)
    print("After removing recycled from cathode tank:", ctank.liq_mol)
    print("100 mol water = ", 100 * H2O_MOLAR_MASS / H2O_DENSITY, "m3")
    for n in range(100):
        ctank.liq_mol["H2O"] += 0.1  # Add some H2O for testing
        ctank.update_mol() # runs all influent and effluent functions(here only recycled effluent)
        print("Level", ctank.liq_mol["H2O"])

        