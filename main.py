from python.objects import *
from python.parameters import *
# from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent
import matplotlib.pyplot as plt
from python.parameters import params as p
## Initialize the system
import numpy as np

### INIT SYSTEM ####
system = System(p)
# Track anode and cathode mols over time
time_history = []
tanks_mol_history = {
    "anode": {key: [] for key in Mols.keys()},
    "cathode": {key: [] for key in Mols.keys()}
}
custom_property_history = {
    "Anode Pressure": [],
    "Cathode Pressure": [],
    "IPP": [],
}  # Track any custom property

### RUN SIMULATION ###
duration = 60*10
dt = 0.1
steps = int(duration/dt)

for step in range(steps):
    try:
        system.step(dt)
        time_history.append(system.time)
        print("Time (s):", system.time)
        # Record all species for both tanks
        for key in Mols.keys():
            tanks_mol_history["anode"][key].append(system.anode.mols[key])
            tanks_mol_history["cathode"][key].append(system.cathode.mols[key])

        # Record custom properties
        custom_property_history["Anode Pressure"].append(system.anode.pressure)
        custom_property_history["Cathode Pressure"].append(system.cathode.pressure)
        custom_property_history["IPP"].append(p.IPP)
    except Exception as e:
        print(f"\33[91mError at step {step}, time {system.time}s:\33[0m {e}")
        break

### PLOTTING  ###

save_plots = True
show_plots = False

if max(custom_property_history["IPP"]) - min(custom_property_history["IPP"]) == 0:
    plot_save_folder = ".plots/steady/"
else:
    plot_save_folder = "./plots/step/"

color_h2o = "#1f77b4"  # blue
color_h2 = "#ff7f0e"  # orange
color_o2 = "#2ca02c"  # green


#############################################################################################################################
######################################## BIG 3x2 PLOT #######################################################################
#############################################################################################################################
# # Plot results
# fig, axes = plt.subplots(3, 2, figsize=(15, 12), sharex=True)
# fig.suptitle('Electrolyzer State Over Time', fontsize=16)

# # Plot liquid species
# axes[0, 0].plot(time_history, mols_history["anode"]["LH2O"], label="LH2O", linewidth=2)
# axes[0, 0].plot(time_history, mols_history["anode"]["LH2"], label="LH2", linewidth=2)
# axes[0, 0].plot(time_history, mols_history["anode"]["LO2"], label="LO2", linewidth=2)
# axes[0, 0].set_ylabel("Moles (mol)")
# axes[0, 0].set_title("Anode Liquid Species")
# axes[0, 0].legend()
# axes[0, 0].grid(True)

# # axes[0, 1].plot(time_history, mols_history["cathode"]["LH2O"], label="LH2O", linewidth=2)
# axes[0, 1].plot(time_history, mols_history["cathode"]["LH2"], label="LH2", linewidth=2)
# # axes[0, 1].plot(time_history, mols_history["cathode"]["LO2"], label="LO2", linewidth=2)
# axes[0, 1].set_ylabel("Moles (mol)")
# axes[0, 1].set_title("Cathode Liquid Species")
# axes[0, 1].legend()
# axes[0, 1].grid(True)

# # Plot gas species
# # axes[1, 0].plot(time_history, mols_history["anode"]["GH2O"], label="GH2O", linewidth=2)
# axes[1, 0].plot(time_history, mols_history["anode"]["GH2"], label="GH2", linewidth=2)
# # axes[1, 0].plot(time_history, mols_history["anode"]["GO2"], label="GO2", linewidth=2)
# axes[1, 0].set_ylabel("Moles (mol)")
# axes[1, 0].set_title("Anode Gas Species")
# axes[1, 0].legend()
# axes[1, 0].grid(True)

# # axes[1, 1].plot(time_history, mols_history["cathode"]["GH2O"], label="GH2O", linewidth=2)
# axes[1, 1].plot(time_history, mols_history["cathode"]["GH2"], label="GH2", linewidth=2)
# # axes[1, 1].plot(time_history, mols_history["cathode"]["GO2"], label="GO2", linewidth=2)
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

# # plt.show()


###############################################################################################################################
####################################### BIG INDIVIDUAL PLOTS ##################################################################
###############################################################################################################################

###############################################################################################################################
# Anode liquid species plot: left axis LH2O, right axis LH2 & LO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Liquid Species', fontsize=16)

ax1.plot(time_history, tanks_mol_history["anode"]["LH2O"], label="LH2O", linewidth=2, color=color_h2o)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("LH2O (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history, tanks_mol_history["anode"]["LH2"], label="LH2", linewidth=1.5, color=color_h2)
ax2.plot(time_history, tanks_mol_history["anode"]["LO2"], label="LO2", linewidth=1.5, color=color_o2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LH2 / LO2 (mol)", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_liquid_species.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# Anode gas species plot: left axis GO2, right axis GH2 & GO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Gas Species', fontsize=16)

ax1.plot(time_history, tanks_mol_history["anode"]["GO2"], label="GO2", linewidth=2, color=color_o2)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("GO2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='lower right')
ax1.grid(True)

ax2.plot(time_history, tanks_mol_history["anode"]["GH2"], label="GH2", linewidth=1.5, color=color_h2)
ax2.plot(time_history, tanks_mol_history["anode"]["GH2O"], label="GH2O", linewidth=1.5, color=color_h2o)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("GH2 / GH2O (mol)", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='lower right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_gas_species.png', dpi=600)
if show_plots: plt.show()


###############################################################################################################################
# Cathode Liquid species plot: left axis LH2O, right axis LH2 & LO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Liquid Species', fontsize=16)

ax1.plot(time_history, tanks_mol_history["cathode"]["LH2O"], label="LH2O", linewidth=2, color='tab:blue')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("LH2O (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history, tanks_mol_history["cathode"]["LH2"], label="LH2", linewidth=1.5, color='tab:orange')
ax2.plot(time_history, tanks_mol_history["cathode"]["LO2"], label="LO2", linewidth=1.5, color='tab:green')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LH2 / LO2 (mol)", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'cathode_liquid_species.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# Cathode gas species plot: left axis GO2, right axis GH2 & GO2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Gas Species', fontsize=16)

ax1.plot(time_history, tanks_mol_history["cathode"]["GH2"], label="GH2", linewidth=2, color=color_h2)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("GH2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)

ax2.plot(time_history, tanks_mol_history["cathode"]["GO2"], label="GO2", linewidth=1.5, color=color_o2)
ax2.plot(time_history, tanks_mol_history["cathode"]["GH2O"], label="GH2O", linewidth=1.5, color=color_h2o)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("GO2 / GH2O (mol)", color='black')
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
# Anode and Cathode Pressure plots
plt.figure(figsize=(8, 4))
plt.plot(time_history, custom_property_history["Anode Pressure"], linewidth=2, color='green')
plt.title("Anode Pressure vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (Pa)")
plt.grid(True)
plt.ticklabel_format(style='sci', useOffset=False, axis='y')
if save_plots: plt.savefig(plot_save_folder + 'anode_pressure.png', dpi=600)
if show_plots: plt.show()

plt.figure(figsize=(8, 4))
plt.plot(time_history, custom_property_history["Cathode Pressure"], linewidth=2, color='blue')
plt.title("Cathode Pressure vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (Pa)")
plt.grid(True)
plt.ticklabel_format(style='sci', useOffset=False, axis='y')
if save_plots: plt.savefig(plot_save_folder + 'cathode_pressure.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################
# # Anode GH2 plot TROUBLESHOOTING
# plt.figure(figsize=(8, 4))
# plt.plot(time_history, tanks_mol_history["anode"]["GH2"], label="H2", linewidth=2, color=color_h2)
# plt.title("Anode H2 vs Time")
# plt.xlabel("Time (s)")
# plt.ylabel("H2 (mol)")
# plt.grid(True)
# if save_plots: plt.savefig(plot_save_folder + 'anode_h2.png', dpi=600)
# if show_plots: plt.show()


###############################################################################################################################
############################################ Liquid fractions plot ############################################################
###############################################################################################################################

liq_frac_anode = {
    "LH2O": [tanks_mol_history["anode"]["LH2O"][i] / (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) if (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history))],
    "LH2": [tanks_mol_history["anode"]["LH2"][i] / (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) if (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history))],
    "LO2": [tanks_mol_history["anode"]["LO2"][i] / (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) if (tanks_mol_history["anode"]["LH2O"][i] + tanks_mol_history["anode"]["LH2"][i] + tanks_mol_history["anode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history))]
}

liq_frac_cathode = {
    "LH2O": [tanks_mol_history["cathode"]["LH2O"][i] / (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) if (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history))],
    "LH2": [tanks_mol_history["cathode"]["LH2"][i] / (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) if (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history))],
    "LO2": [tanks_mol_history["cathode"]["LO2"][i] / (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) if (tanks_mol_history["cathode"]["LH2O"][i] + tanks_mol_history["cathode"]["LH2"][i] + tanks_mol_history["cathode"]["LO2"][i]) > 0 else 0 for i in range(len(time_history))]
}

# Anode liquid fractions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Anode Liquid Fractions', fontsize=16)
ax1.plot(time_history, liq_frac_anode["LH2O"], label="LH2O", linewidth=2, color=color_h2o)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("LH2O (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.ticklabel_format(useOffset=False, axis='y')
ax1.grid(True)
ax2.plot(time_history, liq_frac_anode["LH2"], label="LH2", linewidth=1.5, color=color_h2)
ax2.plot(time_history, liq_frac_anode["LO2"], label="LO2", linewidth=1.5, color=color_o2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LH2 / LO2 (mol)", color='black')
# Place the right label outside and move it further right to avoid overlapping ax1
ax2.yaxis.set_label_position('right')
ax2.yaxis.set_label_coords(1.12, 0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.ticklabel_format(useOffset=False, axis='y')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_liquid_species.png', dpi=600)
if show_plots: plt.show()

# Cathode liquid fractions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle('Cathode Liquid Fractions', fontsize=16)

ax1.plot(time_history, liq_frac_cathode["LH2O"], label="LH2O", linewidth=2, color=color_h2o)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("LH2O (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.ticklabel_format(useOffset=False, axis='y')
ax1.grid(True)

ax2.plot(time_history, liq_frac_cathode["LH2"], label="LH2", linewidth=1.5, color=color_h2)
ax2.plot(time_history, liq_frac_cathode["LO2"], label="LO2", linewidth=1.5, color=color_o2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LH2 / LO2 (mol)", color='black')
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
# # Cathode oxygen diffusion and drag plot 
cathode_oxygen_diffusion = system.electrolyzer.track_oxygen_diffusion
cathode_oxygen_drag = system.electrolyzer.track_drag
plt.figure(figsize=(8, 4))
plt.plot(time_history, [cathode_oxygen_diffusion[i]['GO2'] for i in range(len(time_history))], label="Diffusion", linewidth=2, color='blue')
plt.plot(time_history, [cathode_oxygen_drag[i]['LO2'] for i in range(len(time_history))], label="Drag", linewidth=2, color='orange')
plt.title("Cathode Oxygen Diffusion and Drag vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Moles per second (mol/s)")
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
ax1.plot(time_history, [electrolyzer_history_cathode[i]['LH2O'] for i in range(len(time_history))], label="LH2O", linewidth=2, color='tab:blue')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("LH2O (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history, [electrolyzer_history_cathode[i]['LH2'] for i in range(len(time_history))], label="LH2", linewidth=1.5, color='tab:orange')
ax2.plot(time_history, [electrolyzer_history_cathode[i]['LO2'] for i in range(len(time_history))], label="LO2", linewidth=1.5, color='tab:green')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("LH2 / LO2 (mol)", color='black')
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
ax1.plot(time_history, [electrolyzer_history_cathode[i]['GH2'] for i in range(len(time_history))], label="GH2", linewidth=2, color='tab:blue')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("GH2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history, [electrolyzer_history_cathode[i]['GH2O'] for i in range(len(time_history))], label="GH2O", linewidth=1.5, color='tab:orange')
ax2.plot(time_history, [electrolyzer_history_cathode[i]['GO2'] for i in range(len(time_history))], label="GO2", linewidth=1.5, color='tab:green')
ax2.set_xlabel("Time (s)")
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
ax1.plot(time_history, [electrolyzer_history_anode[i]['LO2'] for i in range(len(time_history))], label="LO2", linewidth=2, color='tab:blue')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("LO2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history, [electrolyzer_history_anode[i]['LH2'] for i in range(len(time_history))], label="LH2", linewidth=1.5, color='tab:orange')
ax2.plot(time_history, [electrolyzer_history_anode[i]['LO2'] for i in range(len(time_history))], label="LO2", linewidth=1.5, color='tab:green')
ax2.set_xlabel("Time (s)")
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
ax1.plot(time_history, [electrolyzer_history_anode[i]['GO2'] for i in range(len(time_history))], label="GO2", linewidth=2, color='tab:blue')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("GO2 (mol)", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.legend(loc='center right')
ax1.grid(True)
ax2.plot(time_history, [electrolyzer_history_anode[i]['GH2O'] for i in range(len(time_history))], label="GH2O", linewidth=1.5, color='tab:orange')
ax2.plot(time_history, [electrolyzer_history_anode[i]['GH2'] for i in range(len(time_history))], label="GH2", linewidth=1.5, color='tab:green')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("GH2O / GH2 (mol)", color='black')
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='y', labelcolor='black')
ax2.legend(loc='center right')
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + 'anode_gas_generation.png', dpi=600)
if show_plots: plt.show()

###############################################################################################################################