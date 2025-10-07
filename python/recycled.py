from objects import Tank, System, initialize_test_tanks
from parameters import (
CATHODE_LIQUID_VOLUME, CATHODE_SEPARATOR_CONTROLLER_GAIN,
SYSTEM_TEMPERATURE,
H2O_DENSITY, H2O_MOLAR_MASS, H2_MOLAR_MASS, O2_MOLAR_MASS
)

def anode_in_recycled(anode_tank):
    """
    Add recycled into anode tank
    """
    recycled_flow = recycled(anode_tank)
    for species, flow in recycled_flow.items():
        anode_tank.liq_mol[species] += flow

def cathode_out_recycled(cathode_tank):
    """
    Remove recycled from cathode tank
    """
    recycled_flow = recycled(cathode_tank)
    for species, flow in recycled_flow.items():
        cathode_tank.liq_mol[species] -= flow


def recycled(tank):
    """
    Compute recycled cathode effluent mol balances
    """
    # Calculate cathode mass rate (kg/s)
    cathode_mass_rate = cathode_mass_rate_pump(tank)
    
    if cathode_mass_rate <= 0:
        return {"H2O": 0, "H2": 0, "O2": 0}
    
    # Assume tank and pump concentrations are identical
    try:
        molar_masses = {"H2O": H2O_MOLAR_MASS, "H2": H2_MOLAR_MASS, "O2": O2_MOLAR_MASS}
        
        # Calculate total mass of liquid in tank
        total_mass = sum([tank.liq_mol[sp] * molar_masses[sp] for sp in molar_masses.keys()])
        
        if total_mass == 0:
            return {"H2O": 0, "H2": 0, "O2": 0}
    
    except ZeroDivisionError:
        return {"H2O": 0, "H2": 0, "O2": 0}

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
    return nd__cr    

def cathode_mass_rate_pump(tank):
    """md_p__cr. Compute the mass flow rate of the cathode pump. """
    # Calculate actual liquid volume in tank (convert moles to volume)
    liquid_volume_actual = tank.liq_mol["H2O"] * H2O_MOLAR_MASS / H2O_DENSITY  # m3
    liquid_volume_target = CATHODE_LIQUID_VOLUME  # m3
    volume_error = liquid_volume_actual - liquid_volume_target  # m3

    # print(volume_error)
    
    # Only pump out when liquid level is above target (positive volume error)
    # Mass flow rate should be proportional to how much above target we are
    if volume_error > 0:
        mass_rate_actual = CATHODE_SEPARATOR_CONTROLLER_GAIN * volume_error * H2O_DENSITY  # kg/s
    else:
        mass_rate_actual = 0  # No pumping when below or at target
    
    return mass_rate_actual


if __name__ == "__main__":
    system, atank, ctank = initialize_test_tanks()
    cathode_out_recycled(ctank)
    print("After removing recycled from cathode tank:", ctank.liq_mol)

    for n in range(100):
        ctank.liq_mol["H2O"] += 0.1  # Add some H2O for testing
        cathode_out_recycled(ctank)
        print("Level", ctank.liq_mol["H2O"])