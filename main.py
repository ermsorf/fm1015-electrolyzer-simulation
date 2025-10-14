from python.objects import *
from python.parameters import *
from python.inef import inlet_pump, anode_in_recycled, cathode_out_recycled, anode_valve_effluent, cathode_valve_effluent
import matplotlib.pyplot as plt
from python.parameters import params as p
## Initialize the system

system = System()
p.add_system(system)
# Track anode mols over time
time_history = []
anode_mols_history = {key: [] for key in Mols.keys()}
custom_property_history = []  # Track any custom property

duration = 10
dt = 0.1
steps = int(duration/dt)

for step in range(steps):
    system.step(dt)
    time_history.append(system.time)
    
    # Record all species
    for key in Mols.keys():
        anode_mols_history[key].append(system.cathode.mols[key])
    
    # Record custom property - change this line to track whatever you want
    custom_property_history.append(system.cathode.pressure)  # Example: cathode pressure
# print("Final anode mols:")
# print(system.anode.mols)
# print("\nFinal cathode mols:")
# print(system.cathode.mols)

# Plot results
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

# Plot liquid species
ax1.plot(time_history, anode_mols_history["LH2O"], label="LH2O", linewidth=2)
ax1.plot(time_history, anode_mols_history["LH2"], label="LH2", linewidth=2)
ax1.plot(time_history, anode_mols_history["LO2"], label="LO2", linewidth=2)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Moles (mol)")
ax1.set_title("Anode Liquid Species")
ax1.legend()
ax1.grid(True)

# Plot gas species
ax2.plot(time_history, anode_mols_history["GH2O"], label="GH2O", linewidth=2)
ax2.plot(time_history, anode_mols_history["GH2"], label="GH2", linewidth=2)
ax2.plot(time_history, anode_mols_history["GO2"], label="GO2", linewidth=2)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Moles (mol)")
ax2.set_title("Anode Gas Species")
ax2.legend()
ax2.grid(True)

# Plot custom property
ax3.plot(time_history, custom_property_history, linewidth=2, color='purple')
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Custom Property")
ax3.set_title("Custom Property vs Time")
ax3.grid(True)

plt.tight_layout()
plt.show()
