import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

roblox = pd.read_csv("Oculus_Roblox/Roblox_1.csv")
roblox = roblox.loc[:, ["power_current"]]
vrchat = pd.read_csv("Oculus_VRChat/VRChat_1.csv")
vrchat = vrchat.loc[:, ["power_current"]]
print((vrchat.mean() - roblox.mean())/roblox.mean())


figure = plt.figure(figsize=(20,11.25), dpi=80)
ax = figure.add_subplot(111)
ax.tick_params(pad=18, labelsize=34)
ax.plot(roblox["power_current"], color="blue", linestyle="dashdot",
        label="Roblox(PC Display)", linewidth=4)
ax.plot(vrchat["power_current"], color="red",
        label="VRChat(Standalone)", linewidth=4)
ax.set_ylabel("Energy Consumption", fontsize=30)
ax.set_xlim(0, 210)
ax.set_ylim(800, 1800)
ax.set_xlabel("Time/s", fontsize=30)
ax.legend(loc='upper right', fontsize=40)

plt.savefig("Oculus_complex/real_time_energy.pdf", bbox_inches='tight')
plt.show()