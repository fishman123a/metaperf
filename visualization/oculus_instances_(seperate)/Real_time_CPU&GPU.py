import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

roblox = pd.read_csv("Oculus_Roblox/Roblox_1.csv")
roblox = roblox.loc[:,["cpu_utilization_percentage", "gpu_utilization_percentage"]]
vrchat = pd.read_csv("Oculus_VRChat/VRChat_1.csv")
vrchat = vrchat.loc[:,["cpu_utilization_percentage", "gpu_utilization_percentage"]]

figure = plt.figure(figsize=(32,18), dpi=80)
ax = figure.add_subplot(211)
ax.tick_params(pad=18, labelsize=34)
ax.plot(roblox["cpu_utilization_percentage"], color="blue", linestyle="dashdot",
        label="CPU", linewidth=4)
ax.plot(roblox["gpu_utilization_percentage"], color="red", linestyle="dashdot",
        label="GPU", linewidth=4)


ax.annotate('Wakeup from standby mode', xy=(90, 60), xytext=(100, 70),
            xycoords='data', fontsize=50,
            arrowprops=dict(facecolor='black', shrink=0.05))


ax.set_ylabel("Utilization Percentage %", fontsize=30)
ax.set_xlabel("Roblox Time/s", fontsize=30)
ax.legend(loc='upper right', fontsize=40)

ax2 = figure.add_subplot(212)
ax2.tick_params(pad=18, labelsize=34)
ax2.plot(vrchat["cpu_utilization_percentage"], color="blue",
        label="CPU", linewidth=4)
ax2.plot(vrchat["gpu_utilization_percentage"], color="red",
        label="GPU", linewidth=4)

ax2.set_ylabel("Utilization Percentage %", fontsize=30)
ax2.set_xlabel("VRChat Time/s", fontsize=30)
#ax2.legend(loc='upper right', fontsize=40)

plt.savefig("Oculus_complex/real_time_cpu_gpu.pdf", bbox_inches='tight')
plt.show()


