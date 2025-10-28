import matplotlib.pyplot as plt

import numpy as np
from python.objects import *
from python.parameters import *
# from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent
import matplotlib.pyplot as plt
from python.parameters import params as p
## Initialize the system


### INIT SYSTEM ####
system = System(p)
# Track anode and cathode mols over time
time_history = []
time_history_min = []
tanks_mol_history = {
    "anode": {key: [] for key in Mols.keys()},
    "cathode": {key: [] for key in Mols.keys()}
}
custom_property_history = {
    "Anode Pressure": [],
    "Cathode Pressure": [],
    "IPP": [],
    "H2_O2_fraction": [],
    "Anode Volume Fraction": [],
    "Cathode Volume Fraction": [],
}  # Track any custom property

### RUN SIMULATION ###
duration = 60*10
dt = 0.1
steps = int(duration/dt)

for step in range(steps):
    try:
        system.step(dt)
        time_history.append(system.time)
        time_history_min.append(system.time / 60)
        print(f"Time (s): {system.time:.1f}")
        # Record all species for both tanks
        for key in Mols.keys():
            tanks_mol_history["anode"][key].append(system.anode.mols[key])
            tanks_mol_history["cathode"][key].append(system.cathode.mols[key])

        # Record custom properties
        custom_property_history["Anode Pressure"].append(system.anode.pressure)
        custom_property_history["Cathode Pressure"].append(system.cathode.pressure)
        custom_property_history["IPP"].append(p.IPP)
        custom_property_history["H2_O2_fraction"].append(float(system.anode.mols["GH2"] / system.anode.mols["GO2"]))
        custom_property_history["Anode Volume Fraction"].append(system.anode.liquid_volume / system.anode.volume)
        custom_property_history["Cathode Volume Fraction"].append(system.cathode.liquid_volume / system.cathode.volume)

    except Exception as e:
        print(f"\33[91mError at step {step}, time {system.time}s:\33[0m {e}")
        break

if system.time < duration * 0.1:
    raise RuntimeError("Simulation ran less than 10% of duration. Not continuing")


### PLOTTING  ###

save_plots = False
show_plots = False

if max(custom_property_history["IPP"]) - min(custom_property_history["IPP"]) == 0:
    plot_save_folder = __file__+"/../plots/steady/"
else:
    plot_save_folder = __file__+"/../plots/step/"

COLOR_H2O = "#1f77b4"  # blue
COLOR_H2 = "#ff7f0e"  # orange
COLOR_O2 = "#2ca02c"  # green

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['mathtext.fontset'] = 'cm'  # only math uses Computer Modern
plt.rcParams['mathtext.rm'] = 'serif'    # optional, refine math roman font

###############################################################################################################################
####################################### INDIVIDUAL PLOTS ######################################################################
###############################################################################################################################

###############################################################################################################################
# Anode liquid species plot: left axis LH2O, right axis LH2 & LO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Liquid Species', fontsize=16)

ax1.plot(time_history_min, tanks_mol_history["anode"]["LH2O"], label=r"$x_{\mathrm{H_2O}}$", linewidth=2, color=COLOR_H2O)
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$x_{\mathrm{H_2O}}$ [mol]", fontsize=16)
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history_min, tanks_mol_history["anode"]["LH2"], label=r"$x_{\mathrm{H_2}}$", linewidth=1.5, color=COLOR_H2)
ax2.plot(time_history_min, tanks_mol_history["anode"]["LO2"], label=r"$x_{\mathrm{O_2}}$", linewidth=1.5, color=COLOR_O2)
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$x_{\mathrm{H_2}}$, $x_{\mathrm{O_2}}$ [mol]")
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_liquid_species.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# Anode gas species plot: left axis GO2, right axis GH2 & GO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Gas Species', fontsize=16)

ax1.plot(time_history_min, tanks_mol_history["anode"]["GO2"], label=r"$y_{\mathrm{O_2}}$", linewidth=2, color=COLOR_O2)
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$y_{\mathrm{O_2}}$ [mol]")
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history_min, tanks_mol_history["anode"]["GH2"], label="GH2", linewidth=1.5, color=COLOR_H2)
ax2.plot(time_history_min, tanks_mol_history["anode"]["GH2O"], label="GH2O", linewidth=1.5, color=COLOR_H2O)
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$y_{\mathrm{H_2}}$, $y_{\mathrm{H_2O}}$ [mol]")
ax2.yaxis.set_label_position('right')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_gas_species.png', dpi=600)
if show_plots: plt.show()


###############################################################################################################################
# Cathode Liquid species plot: left axis LH2O, right axis LH2 & LO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Liquid Species', fontsize=16)

ax1.plot(time_history_min, tanks_mol_history["cathode"]["LH2O"], label="LH2O", linewidth=2, color='tab:blue')
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$x_{\mathrm{H_2O}}$ [mol]")
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history_min, tanks_mol_history["cathode"]["LH2"], label=r"$x_{\mathrm{H_2}}$", linewidth=1.5, color='tab:orange')
ax2.plot(time_history_min, tanks_mol_history["cathode"]["LO2"], label=r"$x_{\mathrm{O_2}}$", linewidth=1.5, color='tab:green')
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$x_{\mathrm{H_2}}$, $x_{\mathrm{O_2}}$ [mol]")
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_liquid_species.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# Cathode gas species plot: left axis GO2, right axis GH2 & GO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Gas Species', fontsize=16)

ax1.plot(time_history_min, tanks_mol_history["cathode"]["GH2"], label=r"$y_{\mathrm{H_2}}$", linewidth=2, color=COLOR_H2)
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$y_{\mathrm{H_2}}$ [mol]", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history_min, tanks_mol_history["cathode"]["GO2"], label=r"$y_{\mathrm{O_2}}$", linewidth=1.5, color=COLOR_O2)
ax2.plot(time_history_min, tanks_mol_history["cathode"]["GH2O"], label=r"$y_{\mathrm{H_2O}}$", linewidth=1.5, color=COLOR_H2O)
ax2.set_xlabel(r"$t$ _")
ax2.set_ylabel(r"$y_{\mathrm{O_2}}$, $y_{\mathrm{H_2O}}$ [mol]", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_gas_species.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# Pressure plots
plt.figure(figsize=(8, 4))
plt.plot(time_history_min, custom_property_history["Anode Pressure"], linewidth=2, color='green')
plt.title("Anode Pressure vs Time")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"Pressure [Pa]")
plt.grid(True)
plt.ticklabel_format(style='sci', useOffset=False, axis='y')
if save_plots: plt.savefig(plot_save_folder + 'anode_pressure.png', dpi=600)
if show_plots: plt.show()

plt.figure(figsize=(8, 4))
plt.plot(time_history_min, custom_property_history["Cathode Pressure"], linewidth=2, color='blue')
plt.title("Cathode Pressure vs Time")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"Pressure [Pa]")
plt.grid(True)
plt.ticklabel_format(style='sci', useOffset=False, axis='y')
if save_plots: plt.savefig(plot_save_folder + 'cathode_pressure.png', dpi=600)
if show_plots: plt.show()


###############################################################################################################################
############################################ Liquid fractions plot ############################################################
###############################################################################################################################

liq_frac_anode = {
    "LH2O": [tanks_mol_history["anode"]["LH2O"][i] / (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) if (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "LH2": [tanks_mol_history["anode"]["LH2"][i] / (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) if (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "LO2": [tanks_mol_history["anode"]["LO2"][i] / (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) if (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history_min))]
}

liq_frac_cathode = {
    "LH2O": [tanks_mol_history["cathode"]["LH2O"][i] / (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) if (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "LH2": [tanks_mol_history["cathode"]["LH2"][i] / (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) if (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "LO2": [tanks_mol_history["cathode"]["LO2"][i] / (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) if (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history_min))]
}

# Anode liquid fractions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Liquid Fractions', fontsize=16)
ax1.plot(time_history_min, liq_frac_anode["LH2O"], label=r"x_{\mathrm{H_2O}}", linewidth=2, color=COLOR_H2O)
ax1.set_xlabel(r"Time [min]")
ax1.set_ylabel(r"$x_{\mathrm{H_2O}}$ [mol]", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.ticklabel_format(useOffset=False, axis='y')
ax1.grid(True)
ax2.plot(time_history_min, liq_frac_anode["LH2"], label=r"$x_{\mathrm{H_2}}$", linewidth=1.5, color=COLOR_H2)
ax2.plot(time_history_min, liq_frac_anode["LO2"], label=r"$x_{\mathrm{O_2}}$", linewidth=1.5, color=COLOR_O2)
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$x_{\mathrm{H_2}}$, $x_{\mathrm{O_2}}$ [mol]", color='black')
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.ticklabel_format(useOffset=False, axis='y')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_liquid_fraction.png', dpi=600)
if show_plots: plt.show()

# Cathode liquid fractions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Liquid Fractions', fontsize=16)

ax1.plot(time_history_min, liq_frac_cathode["LH2O"], label=r"$x_{\mathrm{H_2O}}$", linewidth=2, color=COLOR_H2O)
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$x_{\mathrm{H_2O}}$ [mol]", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.ticklabel_format(useOffset=False, axis='y')
ax1.grid(True)

ax2.plot(time_history_min, liq_frac_cathode["LH2"], label=r"$x_{\mathrm{H_2}}$", linewidth=1.5, color=COLOR_H2)
ax2.plot(time_history_min, liq_frac_cathode["LO2"], label=r"$x_{\mathrm{O_2}}$", linewidth=1.5, color=COLOR_O2)
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$x_{\mathrm{H_2}}$, $x_{\mathrm{O_2}}$ [mol]", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.ticklabel_format(useOffset=False, axis='y')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_liquid_fraction.png', dpi=600)
if show_plots: plt.show()


###############################################################################################################################
############################################ Gas fractions plot ###############################################################
###############################################################################################################################

gas_frac_anode = {
    "GH2O": [tanks_mol_history["anode"]["GH2O"][i] / (tanks_mol_history["anode"]["GH2O"][i] + tanks_mol_history["anode"]["GH2"][i] + tanks_mol_history["anode"]["GO2"][i]) if (tanks_mol_history["anode"]["GH2O"][i] + tanks_mol_history["anode"]["GH2"][i] + tanks_mol_history["anode"]["GO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "GH2": [tanks_mol_history["anode"]["GH2"][i] / (tanks_mol_history["anode"]["GH2O"][i] + tanks_mol_history["anode"]["GH2"][i] + tanks_mol_history["anode"]["GO2"][i]) if (tanks_mol_history["anode"]["GH2O"][i] + tanks_mol_history["anode"]["GH2"][i] + tanks_mol_history["anode"]["GO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "GO2": [tanks_mol_history["anode"]["GO2"][i] / (tanks_mol_history["anode"]["GH2O"][i] + tanks_mol_history["anode"]["GH2"][i] + tanks_mol_history["anode"]["GO2"][i]) if (tanks_mol_history["anode"]["GH2O"][i] + tanks_mol_history["anode"]["GH2"][i] + tanks_mol_history["anode"]["GO2"][i]) > 0 else 0 for i in range(len(time_history_min))]
}

gas_frac_cathode = {
    "GH2O": [tanks_mol_history["cathode"]["GH2O"][i] / (tanks_mol_history["cathode"]["GH2O"][i] + tanks_mol_history["cathode"]["GH2"][i] + tanks_mol_history["cathode"]["GO2"][i]) if (tanks_mol_history["cathode"]["GH2O"][i] + tanks_mol_history["cathode"]["GH2"][i] + tanks_mol_history["cathode"]["GO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "GH2": [tanks_mol_history["cathode"]["GH2"][i] / (tanks_mol_history["cathode"]["GH2O"][i] + tanks_mol_history["cathode"]["GH2"][i] + tanks_mol_history["cathode"]["GO2"][i]) if (tanks_mol_history["cathode"]["GH2O"][i] + tanks_mol_history["cathode"]["GH2"][i] + tanks_mol_history["cathode"]["GO2"][i]) > 0 else 0 for i in range(len(time_history_min))],
    "GO2": [tanks_mol_history["cathode"]["GO2"][i] / (tanks_mol_history["cathode"]["GH2O"][i] + tanks_mol_history["cathode"]["GH2"][i] + tanks_mol_history["cathode"]["GO2"][i]) if (tanks_mol_history["cathode"]["GH2O"][i] + tanks_mol_history["cathode"]["GH2"][i] + tanks_mol_history["cathode"]["GO2"][i]) > 0 else 0 for i in range(len(time_history_min))]
}
# Anode liquid fractions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Gas Fractions', fontsize=16)
ax1.plot(time_history_min, gas_frac_anode["GH2O"], label=r"$y_{\mathrm{H_2O}}$", linewidth=2, color=COLOR_H2O)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel(r"$y_{\mathrm{H_2O}}$ [mol]", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.ticklabel_format(useOffset=False, axis='y')
ax1.grid(True)
ax2.plot(time_history_min, gas_frac_anode["GH2"], label=r"$y_{\mathrm{H_2}}$", linewidth=1.5, color=COLOR_H2)
ax2.plot(time_history_min, gas_frac_anode["GO2"], label=r"$y_{\mathrm{O_2}}$", linewidth=1.5, color=COLOR_O2)
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$y_{\mathrm{H_2}}$, $y_{\mathrm{O_2}}$ [mol]", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.ticklabel_format(useOffset=False, axis='y')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_gas_fraction.png', dpi=600)
if show_plots: plt.show()

# Cathode liquid fractions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Gas Fractions', fontsize=16)

ax1.plot(time_history_min, gas_frac_cathode["GH2O"], label=r"$y_{\mathrm{H_2O}}$", linewidth=2, color=COLOR_H2O)
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$y_{\mathrm{H_2O}}$ [mol]", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.ticklabel_format(useOffset=False, axis='y')
ax1.grid(True)

ax2.plot(time_history_min, gas_frac_cathode["GH2"], label=r"$y_{\mathrm{H_2}}$", linewidth=1.5, color=COLOR_H2)
ax2.plot(time_history_min, gas_frac_cathode["GO2"], label=r"$y_{\mathrm{O_2}}$", linewidth=1.5, color=COLOR_O2)
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$y_{\mathrm{H_2}}$, $y_{\mathrm{O_2}}$ [min]", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.ticklabel_format(useOffset=False, axis='y')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_gas_fraction.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# # Cathode oxygen diffusion and drag plot 
cathode_oxygen_diffusion = system.electrolyzer.track_oxygen_diffusion
cathode_drag = system.electrolyzer.track_drag

plt.figure(figsize=(8, 4))
plt.plot(time_history_min, [cathode_oxygen_diffusion[i]['GO2'] for i in range(len(time_history_min))], label=r"$\dot{n}^{\delta}_{\mathrm{O_2}}$", linewidth=2, color='blue')
plt.plot(time_history_min, [cathode_drag[i]['LO2'] for i in range(len(time_history_min))], label=r"$\dot{n}^{\mathrm{d}}_{\mathrm{O_2}}$", linewidth=2, color='orange')
plt.title("Cathode Oxygen Diffusion and Drag vs Time")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"$\dot{n}_{\mathrm{O_2}}$")
plt.grid(True)
plt.legend(loc='center right')
if save_plots: plt.savefig(plot_save_folder + 'cathode_o2_diffusion_drag.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
################# Electrolyzer anode and cathode generation history plots #####################################################
###############################################################################################################################

electrolyzer_history_anode = system.electrolyzer.track_anode_count
electrolyzer_history_cathode = system.electrolyzer.track_cathode_count
###############################################################################################################################
# Cathode Liquid generation plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Liquid Generation', fontsize=16)
ax1.plot(time_history_min, [electrolyzer_history_cathode[i]['LH2O'] for i in range(len(time_history_min))], label=r"$x_{\mathrm{H_2O}}$", linewidth=2, color='tab:blue')
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$x_{\mathrm{H_2O}}$", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history_min, [electrolyzer_history_cathode[i]['LH2'] for i in range(len(time_history_min))], label=r"$x_{\mathrm{H_2}}$", linewidth=1.5, color='tab:orange')
ax2.plot(time_history_min, [electrolyzer_history_cathode[i]['LO2'] for i in range(len(time_history_min))], label=r"$x_{\mathrm{O_2}}$", linewidth=1.5, color='tab:green')
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$x_{\mathrm{H_2}}$, $x_{\mathrm{O_2}}$ [mol]", color='black')
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_liquid_generation.png', dpi=600)
if show_plots: plt.show()

# Cathode Gas generation plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Gas Generation', fontsize=16)
ax1.plot(time_history_min, [electrolyzer_history_cathode[i]['GH2'] for i in range(len(time_history_min))], label="GH2", linewidth=2, color='tab:blue')
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel("GH2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history_min, [electrolyzer_history_cathode[i]['GH2O'] for i in range(len(time_history_min))], label="GH2O", linewidth=1.5, color='tab:orange')
ax2.plot(time_history_min, [electrolyzer_history_cathode[i]['GO2'] for i in range(len(time_history_min))], label="GO2", linewidth=1.5, color='tab:green')
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel("GH2O / GO2 (mol)", color='black')
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_gas_generation.png', dpi=600)
if show_plots: plt.show()


###############################################################################################################################
# Anode Liquid generation plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Liquid Generation', fontsize=16)
ax1.plot(time_history_min, [electrolyzer_history_anode[i]['LO2'] for i in range(len(time_history_min))], label="LO2", linewidth=2, color='tab:blue')
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel("LO2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history_min, [electrolyzer_history_anode[i]['LH2'] for i in range(len(time_history_min))], label="LH2", linewidth=1.5, color='tab:orange')
ax2.plot(time_history_min, [electrolyzer_history_anode[i]['LO2'] for i in range(len(time_history_min))], label="LO2", linewidth=1.5, color='tab:green')
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel("LH2 / LO2 (mol)", color='black')
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_liquid_generation.png', dpi=600)
if show_plots: plt.show()

# Anode Gas generation plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Gas Generation', fontsize=16)
ax1.plot(time_history_min, [electrolyzer_history_anode[i]['GO2'] for i in range(len(time_history_min))], label="GO2", linewidth=2, color='tab:blue')
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel("GO2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history_min, [electrolyzer_history_anode[i]['GH2O'] for i in range(len(time_history_min))], label="GH2O", linewidth=1.5, color='tab:orange')
ax2.plot(time_history_min, [electrolyzer_history_anode[i]['GH2'] for i in range(len(time_history_min))], label="GH2", linewidth=1.5, color='tab:green')
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel("GH2O / GH2 (mol)", color='black')
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_gas_generation.png', dpi=600)
if show_plots: plt.show()

##############################################################################################################################


############################################################################################################################
####################################### BIG 3x2 PLOT #######################################################################
############################################################################################################################
# # Plot results
# fig, axes = plt.subplots(3, 2, figsize=(15, 12), sharex=True)
# fig.suptitle('Electrolyzer State Over Time', fontsize=16)

# # Plot liquid species
# axes[0, 0].plot(time_history, tanks_mol_history["anode"]["LH2O"], label="LH2O", linewidth=2)
# axes[0, 0].plot(time_history, tanks_mol_history["anode"]["LH2"], label="LH2", linewidth=2)
# axes[0, 0].plot(time_history, tanks_mol_history["anode"]["LO2"], label="LO2", linewidth=2)
# axes[0, 0].set_ylabel("Moles (mol)")
# axes[0, 0].set_title("Anode Liquid Species")
# axes[0, 0].legend()
# axes[0, 0].grid(True)

# # axes[0, 1].plot(time_history, tanks_mol_history["cathode"]["LH2O"], label="LH2O", linewidth=2)
# axes[0, 1].plot(time_history, tanks_mol_history["cathode"]["LH2"], label="LH2", linewidth=2)
# # axes[0, 1].plot(time_history, tanks_mol_history["cathode"]["LO2"], label="LO2", linewidth=2)
# axes[0, 1].set_ylabel("Moles (mol)")
# axes[0, 1].set_title("Cathode Liquid Species")
# axes[0, 1].legend()
# axes[0, 1].grid(True)

# # Plot gas species
# # axes[1, 0].plot(time_history, tanks_mol_history["anode"]["GH2O"], label="GH2O", linewidth=2)
# axes[1, 0].plot(time_history, tanks_mol_history["anode"]["GH2"], label="GH2", linewidth=2)
# # axes[1, 0].plot(time_history, tanks_mol_history["anode"]["GO2"], label="GO2", linewidth=2)
# axes[1, 0].set_ylabel("Moles (mol)")
# axes[1, 0].set_title("Anode Gas Species")
# axes[1, 0].legend()
# axes[1, 0].grid(True)

# # axes[1, 1].plot(time_history, tanks_mol_history["cathode"]["GH2O"], label="GH2O", linewidth=2)
# axes[1, 1].plot(time_history, tanks_mol_history["cathode"]["GH2"], label="GH2", linewidth=2)
# # axes[1, 1].plot(time_history, tanks_mol_history["cathode"]["GO2"], label="GO2", linewidth=2)
# axes[1, 1].set_ylabel("Moles (mol)")
# axes[1, 1].set_title("Cathode Gas Species")
# axes[1, 1].legend()
# axes[1, 1].grid(True)

# # Get function names
# anode_influent_names = [f.__name__ for f in system.anode.influent_functions]
# anode_effluent_names = [f.__name__ for f in system.anode.effluent_functions]
# cathode_influent_names = [f.__name__ for f in system.cathode.influent_functions]
# cathode_effluent_names = [f.__name__ for f in system.cathode.effluent_functions]

# # Format text
# tank_function_text = (
#     "Anode Influent:\n" + ("\n".join(anode_influent_names) if anode_influent_names else "  None") + "\n\n"
#     "Anode Effluent:\n" + ("\n".join(anode_effluent_names) if anode_effluent_names else "  None") + "\n\n"
#     "Cathode Influent:\n" + ("\n".join(cathode_influent_names) if cathode_influent_names else "  None") + "\n\n"
#     "Cathode Effluent:\n" + ("\n".join(cathode_effluent_names) if cathode_effluent_names else "  None")
# )

# electrolyzer_function_names = [f.__name__ for f in system.electrolyzer.functions]
# electrolyzer_function_text = "Electrolyzer Functions:\n" + ("\n ".join(electrolyzer_function_names) if electrolyzer_function_names else "  None")

# # Display function names on the bottom-left subplot
# axes[2, 0].text(0.05, 0.95, tank_function_text, transform=axes[2, 0].transAxes, fontsize=9,
#                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


# axes[2, 0].text(0.5, 0.95, electrolyzer_function_text, transform=axes[2, 0].transAxes, fontsize=9,
#                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

# axes[2, 0].set_title("Info & Notes")
# # axes[2, 0].set_xticks([])
# axes[2, 0].set_yticks([])
# axes[2, 0].grid(True)

# axes[2, 1].plot(time_history, custom_property_history["IPP"], linewidth=2, color='green')
# axes[2, 1].set_xlabel("Time (s)")
# axes[2, 1].set_ylabel("A/cm2")
# axes[2, 1].set_title("IPP vs Time")
# axes[2, 1].grid(True)

# plt.tight_layout()
# # Add top tick marks (no labels/grid) for the first row subplots [0,0] and [0,1]
# try:
#     axes[0, 0].tick_params(axis='x', which='both', top=True,labeltop=True)
#     axes[0, 1].tick_params(axis='x', which='both', top=True, labeltop=True)
# except Exception:
#     pass




#############################################################################################################################
######################################## BERNT PLOTS ########################################################################
#############################################################################################################################

fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8, 4))
ax1.plot(time_history_min, [custom_property_history["Cathode Pressure"][i] / 1e5 for i in range(len(custom_property_history["Cathode Pressure"]))], linewidth=2, color='green')
ax1.set_title("Cathode Pressure")
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$p_c$ [bar]")
ax1.grid(True)
# ax1.ticklabel_format(style='sci', useOffset=False, axis='y')
ax2.plot(time_history_min, [custom_property_history["Anode Pressure"][i] / 1e5 for i in range(len(custom_property_history["Anode Pressure"]))], linewidth=2, color='red')
ax2.set_title("Anode Pressure")
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$p_a$ [bar]")
ax2.grid(True)
plt.tight_layout()
if show_plots: plt.show()





plt.figure(figsize=(8, 4))
plt.plot(time_history_min, custom_property_history["Anode Volume Fraction"], linewidth=2, color='blue', label=r'$V_{a}^{l} / V_{a}$')
plt.plot(time_history_min, custom_property_history["Cathode Volume Fraction"], linewidth=2, color='cyan', label=r'$V_{c}^{l} / V_{c}$')
plt.title("Liquid Volume Fractions in Separators")
plt.xlabel(r"$t$ / min")
plt.ylabel("Volume Fraction")
plt.grid(True)
plt.legend()
# plt.ticklabel_format(style='sci', useOffset=False, axis='y')
plt.tight_layout()
if show_plots: plt.show()


#############################################################################################################################
######################################## Comparison plots ###################################################################
#############################################################################################################################

plt.figure(figsize=(8, 4))
plt.plot(time_history_min, custom_property_history["H2_O2_fraction"], label=r"$\mathrm{H}_2$", linewidth=2, color=COLOR_H2)
plt.title(r"Anode $\mathrm{H}_2:\mathrm{O}_2$ ratio")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"$y_{\mathrm{H}_2}^{a} / y_{\mathrm{O}_2}^{a}$ (%)")
plt.grid(True)
if save_plots: plt.savefig(plot_save_folder + 'comparison_anode_h2.png', dpi=600)
if show_plots: plt.show()



fig, (ax1, ax2) = plt.subplots(2,1,figsize=(8, 8))
ax2.plot(time_history_min, [tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["GH2O"][i] for i in range(len(tanks_mol_history["anode"]["GH2O"]))], linewidth=2, color='green', label=r"n_{\mathrm{H_2O}}^{a}")
ax2.set_title("Anode Molar balance")
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$n^{a}$")
ax2.legend()
ax2.grid(True)
ax1.plot(time_history_min, [tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["GH2"][i] for i in range(len(tanks_mol_history["anode"]["GH2"]))], linewidth=2, color='red', label=r"n_{\mathrm{H_2}}^{a}")
ax1.plot(time_history_min, [tanks_mol_history["anode"]["LO2"][i] + tanks_mol_history["anode"]["GO2"][i] for i in range(len(tanks_mol_history["anode"]["GO2"]))], linewidth=2, color='red', label=r"n_{\mathrm{O_2}}^{a}")
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$n^{a}$")
ax1.grid(True)
ax1.legend()
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + "comparison_anode_molar_balance.png")
if show_plots: plt.show()


# plt.figure(figsize=(8, 4))
# plt.plot(time_history_min, [tanks_mol_history["cathode"][i]["GH2"] / (tanks_mol_history["cathode"][i]["GH2"]+tanks_mol_history["cathode"][i]["GH2O"]+tanks_mol_history["cathode"][i]["GO2"]) for i in range(len(tanks_mol_history["cathode"]))], linewidth=2, color='green')
# plt.title(r"Cathode $y_{\mathrm{H_2}}$")
# plt.xlabel("Time (min)")
# # plt.ylabel()
# plt.grid(True)
# if save_plots: plt.savefig(plot_save_folder + "comparison_h2_mol_fraction.png")
# plt.show()



inlet_values = [system.track_inlet[i]["LH2O"] for i in range(len(system.track_inlet))]
recycled_values = [system.track_recycled[i]["LH2O"] for i in range(len(system.track_recycled))]
plt.figure(figsize=(8, 4))
plt.plot(time_history_min, inlet_values, linewidth=2, color='blue', label=r'Inlet')
plt.plot(time_history_min, recycled_values, linewidth=2, color='cyan', label=r'Recycled')
plt.legend()
plt.grid(True)
if save_plots: plt.savefig(plot_save_folder + "comparison_molar_flow_rate.png")
if show_plots: plt.show()