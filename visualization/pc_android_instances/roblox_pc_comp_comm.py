import matplotlib.pyplot as plt
import pandas as pd
import os

from src.network.utils import PROJECT_ROOT, throughput_integrate_by_protocol
from visualization_tools.utils import FIG_ROOT

roblox_comp = pd.DataFrame()
["cpu_utilization_percentage", "gpu_utilization_percentage"]
roblox_comp.cpu_utilization_percentage = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/rub/computation/cpu.csv'))[
    'total']
roblox_comp.gpu_utilization_percentage = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/rub/computation/gpu.csv'))[
    'core_ocp']

roblox_throughput = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/rub/network/throughput/concat.csv')
))

figure = plt.figure(figsize=(40, 18), dpi=80)
ax = figure.add_subplot(121)
ax.tick_params(pad=18, labelsize=34)
ax.plot(roblox_comp["cpu_utilization_percentage"], color="blue", linestyle="dashdot",
        label="CPU", linewidth=4)
ax.plot(roblox_comp["gpu_utilization_percentage"], color="red", linestyle="dashdot",
        label="GPU", linewidth=4)

ax.set_ylabel("Utilization Percentage %", fontsize=30)
ax.set_xlabel("Time/s", fontsize=30)
ax.legend(loc='upper right', fontsize=40)

ax2 = figure.add_subplot(122)
ax2.tick_params(pad=18, labelsize=34)
ax2.plot(roblox_throughput['UDP'], color="blue",
         label="UDP Flow", linewidth=4)
ax2.plot(roblox_throughput['TCP'], color="red",
         label="TCP Flow", linewidth=4)

ax2.set_ylabel("Throughput Bytes/(0.1 second)", fontsize=30)
ax2.set_xlabel("Roblox Time/0.1 s", fontsize=30)
ax2.legend(loc='upper right', fontsize=40)

plt.savefig(os.path.join(FIG_ROOT, ""), bbox_inches='tight')
plt.show()
