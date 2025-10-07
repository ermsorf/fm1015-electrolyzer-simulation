from objects import Tank, System
from parameters import (
CATHODE_LIQUID_VOLUME,
CATHODE_SEPARATOR_CONTROLLER_GAIN,
SYSTEM_TEMPERATURE,
)

def recycled(tank):
    """
    Compute recycled effluent mole balances
    """
    # TODO
    # Assume tank and pump concentrations are identical
    total_mass = sum([tank.liquid_mol[sp] * tank.species["liquid"][sp].molar_mass for sp in tank.liquid_mol.keys()])
    cathode_mass_rate = cathode_mass_rate_pump(tank)
    
    print(total_mass)
    print(tank.liquid_mol)
    # Calculate molar flow rates based on mass fractions
    H2_molar_flow = tank.liquid_mol["H2"] / total_mass * cathode_mass_rate
    O2_molar_flow = tank.liquid_mol["O2"] / total_mass * cathode_mass_rate
    H2O_molar_flow = tank.liquid_mol["H2O"] / total_mass * cathode_mass_rate
    
    nd__cr = {
        "H2O": H2O_molar_flow,
        "H2": H2_molar_flow,
        "O2": O2_molar_flow 
    }
    return nd__cr    

def cathode_mass_rate_pump(tank):
    """md_p__cr. Compute the mass flow rate of the cathode pump. """
    mass_rate_reference = tank.volume * tank.species["liquid"]["H2O"].density  # kg
    v_actual = tank.volume
    v_target = CATHODE_LIQUID_VOLUME
    mass_rate_actual = mass_rate_reference +  CATHODE_SEPARATOR_CONTROLLER_GAIN * (v_actual - v_target)
    return mass_rate_actual


if __name__ == "__main__":
    system = System()
    ctank = Tank(system, CATHODE_LIQUID_VOLUME, SYSTEM_TEMPERATURE, 30e5)
    ctank.update_levels()
    print(ctank.liquid_mol)
    recycled(ctank)
