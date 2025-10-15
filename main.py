from python.objects import *
from python.parameters import *
# from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent
import matplotlib.pyplot as plt
from python.parameters import params as p
## Initialize the system

system = System()
p.add_system(system)
# Track anode and cathode mols over time
time_history = []
mols_history = {
    "anode": {key: [] for key in Mols.keys()},
    "cathode": {key: [] for key in Mols.keys()}
}
custom_property_history = {
    "Anode Pressure": [],
    "Cathode Pressure": [],
    "IPP": [],
}  # Track any custom property

duration = 60*40
dt = 1
steps = int(duration/dt)

for step in range(steps):
    try:
        system.step(dt)
        time_history.append(system.time)
        print("Time (s):", system.time)
        # Record all species for both tanks
        for key in Mols.keys():
            mols_history["anode"][key].append(system.anode.mols[key])
            mols_history["cathode"][key].append(system.cathode.mols[key])

        # Record custom properties
        # custom_property_history["Anode Pressure"].append(system.anode.pressure)
        custom_property_history["IPP"].append(p.IPP)
    except Exception as e:
        print(f"Error at step {step}, time {system.time}s: {e}")
        break

    # Manual notes text box
manual_notes = """
Electrolyzer functions

generation

"""

# Plot results
fig, axes = plt.subplots(3, 2, figsize=(15, 12), sharex=True)
fig.suptitle('Electrolyzer State Over Time', fontsize=16)

# Plot liquid species
axes[0, 0].plot(time_history, mols_history["anode"]["LH2O"], label="LH2O", linewidth=2)
axes[0, 0].plot(time_history, mols_history["anode"]["LH2"], label="LH2", linewidth=2)
axes[0, 0].plot(time_history, mols_history["anode"]["LO2"], label="LO2", linewidth=2)
axes[0, 0].set_ylabel("Moles (mol)")
axes[0, 0].set_title("Anode Liquid Species")
axes[0, 0].legend()
axes[0, 0].grid(True)

axes[0, 1].plot(time_history, mols_history["cathode"]["LH2O"], label="LH2O", linewidth=2)
axes[0, 1].plot(time_history, mols_history["cathode"]["LH2"], label="LH2", linewidth=2)
axes[0, 1].plot(time_history, mols_history["cathode"]["LO2"], label="LO2", linewidth=2)
axes[0, 1].set_ylabel("Moles (mol)")
axes[0, 1].set_title("Cathode Liquid Species")
axes[0, 1].legend()
axes[0, 1].grid(True)

# Plot gas species
axes[1, 0].plot(time_history, mols_history["anode"]["GH2O"], label="GH2O", linewidth=2)
axes[1, 0].plot(time_history, mols_history["anode"]["GH2"], label="GH2", linewidth=2)
axes[1, 0].plot(time_history, mols_history["anode"]["GO2"], label="GO2", linewidth=2)
axes[1, 0].set_ylabel("Moles (mol)")
axes[1, 0].set_title("Anode Gas Species")
axes[1, 0].legend()
axes[1, 0].grid(True)

axes[1, 1].plot(time_history, mols_history["cathode"]["GH2O"], label="GH2O", linewidth=2)
axes[1, 1].plot(time_history, mols_history["cathode"]["GH2"], label="GH2", linewidth=2)
axes[1, 1].plot(time_history, mols_history["cathode"]["GO2"], label="GO2", linewidth=2)
axes[1, 1].set_ylabel("Moles (mol)")
axes[1, 1].set_title("Cathode Gas Species")
axes[1, 1].legend()
axes[1, 1].grid(True)

# Get function names
anode_influent_names = [f.__name__ for f in system.anode.influent_functions]
anode_effluent_names = [f.__name__ for f in system.anode.effluent_functions]
cathode_influent_names = [f.__name__ for f in system.cathode.influent_functions]
cathode_effluent_names = [f.__name__ for f in system.cathode.effluent_functions]

# Format text
text_to_display = (
    "Anode Influent:\n" + ("\n".join(anode_influent_names) if anode_influent_names else "  None") + "\n\n"
    "Anode Effluent:\n" + ("\n".join(anode_effluent_names) if anode_effluent_names else "  None") + "\n\n"
    "Cathode Influent:\n" + ("\n".join(cathode_influent_names) if cathode_influent_names else "  None") + "\n\n"
    "Cathode Effluent:\n" + ("\n".join(cathode_effluent_names) if cathode_effluent_names else "  None")
)

# Display function names on the bottom-left subplot
axes[2, 0].text(0.05, 0.95, text_to_display, transform=axes[2, 0].transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


axes[2, 0].text(0.5, 0.95, manual_notes, transform=axes[2, 0].transAxes, fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

axes[2, 0].set_title("Info & Notes")
axes[2, 0].set_xticks([])
axes[2, 0].set_yticks([])
axes[2, 0].grid(False)

axes[2, 1].plot(time_history, custom_property_history["IPP"], linewidth=2, color='green')
axes[2, 1].set_xlabel("Time (s)")
axes[2, 1].set_ylabel("A/cm2")
axes[2, 1].set_title("IPP vs Time")
axes[2, 1].grid(True)

plt.tight_layout()
plt.show()





