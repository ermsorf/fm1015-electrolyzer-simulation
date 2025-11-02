"""
Alternative plotter based on main.py
Andreas wanted a clean slate 
to make new plots
"""

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
    "cathode_effluent":[],
    "anode_pressure": [],
    "cathode_pressure": [],
    "diffusion_a2c": [],
    "drag_a2c": [],
    "diffusion_c2a": [],
    "recycled_c2a": [],
    "anode_H2_O2_fraction": [],
    "cathode_H2_O2_fraction": [],
    #
    "anode_volume_fraction": [],
    "cathode_volume_fraction":[],
}  # Track any custom property

### RUN SIMULATION ###
# run for 10 minutes if steady state, else 20 minutes
duration = 60*(20-10*p.steadystate)
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
        custom_property_history["cathode_effluent"].append(system.cathode.tracked_values["effluent_cathode_valve_effluent"]["GH2"])
        custom_property_history["recycled_c2a"].append(system.anode.tracked_values["influent_anode_in_recycled"]["LH2"])
        custom_property_history["anode_pressure"].append(system.anode.pressure)
        custom_property_history["cathode_pressure"].append(system.cathode.pressure)
        custom_property_history["anode_H2_O2_fraction"].append(float(   (system.anode.mols["GH2"] / (system.anode.mols["GH2"] + system.anode.mols["GO2"]))   ) * 100) # 
        custom_property_history["cathode_H2_O2_fraction"].append(float(   (system.cathode.mols["GH2"] / (system.cathode.mols["GH2"] + system.cathode.mols["GO2"]))   ) * 100) #  + 
        custom_property_history["anode_volume_fraction"].append(system.anode.liquid_volume / system.anode.volume)
        custom_property_history["cathode_volume_fraction"].append(system.cathode.liquid_volume / system.cathode.volume)

    except Exception as e:
        print(f"\33[91mError at step {step}, time {system.time}s:\33[0m {e}")
        break

if system.time < duration * 0.1:
    raise RuntimeError("Simulation ran less than 10% of duration. Not continuing")


### PLOTTING  ###

save_plots = True
show_plots = False
steadystate: bool = p.steadystate # Todo add more plot states? "Eh :/", says Andy.

if steadystate:
    plot_save_folder = __file__+"/../plots/steady/"
else:
    plot_save_folder = __file__+"/../plots/step/"

COLOR_H2O = "#1f77b4"  # blue
COLOR_H2 = "#ff7f0e"  # orange
COLOR_O2 = "#2ca02c"  # green

# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['mathtext.fontset'] = 'cm'  # only math uses Computer Modern
# plt.rcParams['mathtext.rm'] = 'serif'    # optional, refine math roman font

###############################################################################################################################
####################################### PLOTS ######################################################################
###############################################################################################################################

# Pressure Plot -----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8, 4))
ax1.plot(time_history_min, [custom_property_history["cathode_pressure"][i] / 1e5 for i in range(len(custom_property_history["cathode_pressure"]))], linewidth=2, color='green')
ax1.set_title("Cathode Pressure")
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$p_c$ [bar]")
ax1.grid(True)
# ax1.ticklabel_format(style='sci', useOffset=False, axis='y')
ax2.plot(time_history_min, [custom_property_history["anode_pressure"][i] / 1e5 for i in range(len(custom_property_history["anode_pressure"]))], linewidth=2, color='red')
ax2.set_title("Anode Pressure")
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$p_a$ [bar]")
ax2.grid(True)
plt.tight_layout()
if save_plots: plt.savefig(plot_save_folder + "tank_pressures.png", dpi=600)
if show_plots: plt.show()


# H2:O2 fraction -------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,4))
# Cathode H2:O2 fraction
ax1.plot(time_history_min, custom_property_history["cathode_H2_O2_fraction"], linewidth=2, color='green')
ax1.set_title(r"Cathode $\mathrm{H}_2:\mathrm{O}_2$ ratio")
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$y_{\mathrm{H}_2}^{c} \;/\; y_{\mathrm{O}_2}^{c}$ [%]")
ax1.grid(True)
# Anode H2:O2 fraction
ax2.plot(time_history_min, custom_property_history["anode_H2_O2_fraction"], label=r"$\mathrm{H}_2$", linewidth=2, color="red")
ax2.set_title(r"Anode $\mathrm{H}_2:\mathrm{O}_2$ ratio")
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$y_{\mathrm{H}_2}^{a} \;/\; y_{\mathrm{O}_2}^{a}$ [%]")
ax2.grid(True)
plt.tight_layout()
plt.savefig(plot_save_folder + "h2_o2.png", dpi=600)
if show_plots: plt.show()


# Cathode oxygen transfer mechanisms -------------------------------------------------------------------------------
cathode_oxygen_diffusion = system.electrolyzer.track_oxygen_diffusion
cathode_drag = system.electrolyzer.track_drag

plt.figure(figsize=(8, 4))
plt.plot(time_history_min, [cathode_oxygen_diffusion[i]['GO2'] for i in range(len(time_history_min))], label=r"$\dot{n}^{\delta}_{\mathrm{O_2}}$", linewidth=2, color='blue')
plt.plot(time_history_min, [cathode_drag[i]['LO2'] for i in range(len(time_history_min))], label=r"$\dot{n}^{\mathrm{d}}_{\mathrm{O_2}}$", linewidth=2, color='orange')
plt.title(r"Cathode $\mathrm{O_2}$ Transfer Mechanisms")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"$\dot{n}_{\mathrm{O_2}}$")
plt.grid(True)
plt.legend(loc='center right')
if save_plots: plt.savefig(plot_save_folder + 'cathode_o2_transfer_mechanisms.png', dpi=600)
if show_plots: plt.show()

# Anode H2 transfer mechanisms ------------------------------------------------------------------------------- 
anode_hydrogen_diffusion= system.electrolyzer.track_hydrogen_diffusion
anode_recycled = custom_property_history["recycled_c2a"]

plt.figure(figsize=(8, 4))
plt.plot(time_history_min, [anode_hydrogen_diffusion[i]['GH2'] for i in range(len(time_history_min))], label=r"$\dot{n}^{\delta}_{\mathrm{H_2}}$", linewidth=2, color='blue')
plt.plot(time_history_min, anode_recycled, label=r"$\dot{n}^{\mathrm{d}}_{\mathrm{H_2}}$", linewidth=2, color='orange')
plt.title(r"anode $\mathrm{H_2}$ Transfer Mechanisms")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"$\dot{n}_{\mathrm{H_2}}$")
plt.grid(True)
plt.legend(loc='center right')
if save_plots: plt.savefig(plot_save_folder + 'anode_h2_transfer_mechanisms.png', dpi=600)
if show_plots: plt.show()



# Hydrogent effluent to storage ------------------------------------------------------------------------------- 
hydrogen_effluent = custom_property_history["cathode_effluent"]

plt.figure(figsize=(8, 4))
plt.plot(time_history_min, hydrogen_effluent, label=r"$\dot{n}^{\mathrm{c,e}}_{\mathrm{H_2}}$", linewidth=2, color='blue')
plt.title(r"Cathode $\mathrm{H_2}$ Effluent To Storage")
plt.xlabel(r"$t$ [min]")
plt.ylabel(r"$\dot{n}^{\mathrm{c,e}}_{\mathrm{H_2}}$")
plt.grid(True)
plt.legend(loc='center right')
if save_plots: plt.savefig(plot_save_folder + 'cathode_effluent_valve.png', dpi=600)
if show_plots: plt.show()

# Hydrogent effluent to storage ------------------------------------------------------------------------------- 
hydrogen_effluent = custom_property_history["cathode_effluent"]
hydrogen_effluent_sum = np.zeros(len(hydrogen_effluent))
# Numerically integrate values 
for i in range(len(hydrogen_effluent_sum)):
    for j in range(i):
        hydrogen_effluent_sum[i] +=hydrogen_effluent[j]

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,4))
# nd -- Hydrogen flow
ax1.plot(time_history_min, hydrogen_effluent, label=r"$\dot{n}^{\mathrm{c,e}}_{\mathrm{H_2}}$", linewidth=2, color='blue')
ax1.set_title(r"Cathode $\mathrm{H_2}$ Effluent To Storage")
ax1.set_xlabel(r"$t$ [min]")
ax1.set_ylabel(r"$\dot{n}^{\mathrm{c,e}}_{\mathrm{H_2}}$")
ax1.grid(True)
# Total (integral) hydrogen ammount in storage tank
ax2.plot(time_history_min, hydrogen_effluent_sum, label=r"$\mathrm{H}_2$", linewidth=2, color="red")
ax2.set_title(r"Total Cathode $\mathrm{H_2}$ Effluent To Storage")
ax2.set_xlabel(r"$t$ [min]")
ax2.set_ylabel(r"$n^{\mathrm{c,e}}_{\mathrm{H_2}}$")
ax2.grid(True)
plt.tight_layout()
plt.savefig(plot_save_folder + "cathode_effluent_valve_withTotalGas.png", dpi=600)
if show_plots: plt.show()
