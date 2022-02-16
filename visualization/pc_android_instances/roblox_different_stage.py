import os

import matplotlib.pyplot as plt
import pandas as pd

from src.network.utils import PROJECT_ROOT, throughput_integrate_by_protocol
from visualization_tools.utils import FIG_ROOT

fsize = 35

def auto_label(rects):
    for rect in rects:
        height = int(rect.get_height())
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    fontsize=13,
                    textcoords="offset points",
                    ha='center', va='bottom')


brookheaven_comp = pd.DataFrame()
brookheaven_comp['cpu_utilization_percentage'] = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/rub/computation/cpu.csv'))[
    'total'] * 100
brookheaven_comp['gpu_utilization_percentage'] = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/rub/computation/gpu.csv'))[
    'core_ocp']  * 100
brookheaven_throughput = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/rub/network/throughput/concat.csv')
)/ 1024)
brookheaven_throughput_ingress = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/rub/network/throughput/concat_ingress.csv')
)/ 1024)

build2survive_comp = pd.DataFrame()
build2survive_comp['cpu_utilization_percentage'] = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/build2survive/computation/cpu.csv'))[
    'total']  * 100
build2survive_comp['gpu_utilization_percentage'] = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/build2survive/computation/gpu.csv'))[
    'core_ocp']  * 100
build2survive_throughput = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/build2survive/network/throughput/concat.csv')
) / 1024)
build2survive_throughput['TCP'] = 0
build2survive_throughput_ingress = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/build2survive/network/throughput/concat_ingress.csv')
) / 1024)

animefight_comp = pd.DataFrame()
animefight_comp['cpu_utilization_percentage'] = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/animefight/computation/cpu.csv'))[
    'total']  * 100
animefight_comp['gpu_utilization_percentage'] = pd.read_csv(os.path.join(PROJECT_ROOT, 'data/roblox/animefight/computation/gpu.csv'))[
    'core_ocp']  * 100
animefight_throughput = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/animefight/network/throughput/concat.csv')
)/ 1024)
animefight_throughput_ingress = throughput_integrate_by_protocol(pd.read_csv(
    os.path.join(PROJECT_ROOT, 'data/roblox/animefight/network/throughput/concat_ingress.csv')
)/ 1024)
animefight_throughput['TCP'] = 0
namelist = ["Role-Play: BrookHeaven", "Building: BuildToSurvive", "Fighting: AnimeFight"]

figure = plt.figure(figsize=(16, 9))

CPU = [brookheaven_comp["cpu_utilization_percentage"].mean(),
       build2survive_comp["cpu_utilization_percentage"].mean(),
       animefight_comp["cpu_utilization_percentage"].mean()]

CPU_ = [brookheaven_comp["cpu_utilization_percentage"].std(),
       build2survive_comp["cpu_utilization_percentage"].std(),
       animefight_comp["cpu_utilization_percentage"].std()]

GPU = [brookheaven_comp["gpu_utilization_percentage"].mean(),
       build2survive_comp["gpu_utilization_percentage"].mean(),
       animefight_comp["gpu_utilization_percentage"].mean()]

GPU_ = [brookheaven_comp["gpu_utilization_percentage"].std(),
       build2survive_comp["gpu_utilization_percentage"].std(),
       animefight_comp["gpu_utilization_percentage"].std()]

TCP = [brookheaven_throughput['TCP'].mean(), build2survive_throughput['TCP'].mean(),
       animefight_throughput['TCP'].mean()]
TCP_ = [brookheaven_throughput['TCP'].std(), build2survive_throughput['TCP'].std(),
       animefight_throughput['TCP'].std()]

UDP = [brookheaven_throughput['UDP'].mean(), build2survive_throughput['UDP'].mean(),
       animefight_throughput['UDP'].mean()]
UDP_ = [brookheaven_throughput['UDP'].std(), build2survive_throughput['UDP'].std(),
       animefight_throughput['UDP'].std()]

UDP_in = [brookheaven_throughput_ingress['UDP'].mean(), build2survive_throughput_ingress['UDP'].mean(),
       animefight_throughput_ingress['UDP'].mean()]
UDP_in_ = [brookheaven_throughput_ingress['UDP'].std(), build2survive_throughput_ingress['UDP'].std(),
       animefight_throughput_ingress['UDP'].std()]
x = list(range(len(CPU)))
total_width, n = 0.8, len(CPU)
width = total_width/n


ax = figure.add_subplot(211)
error_params = dict(elinewidth=1, ecolor='black', capsize=10)

rect1 = ax.bar(x, CPU, width=width, label='CPU',color='white', edgecolor="red",
                    hatch='///',
               yerr=CPU_, error_kw=error_params
               )
for i in range(len(x)):
    x[i] = x[i] + width
rect2 = ax.bar(x, GPU, width=width, label='GPU',color='white', edgecolor="blue",
                    hatch='+++', yerr=GPU_, error_kw=error_params)


ax.set_xlabel("Roblox (PC) Computation for different Games",fontsize=fsize)

auto_label(rect1)
auto_label(rect2)
ax.legend(loc='upper left',edgecolor="white",fontsize=25)
for i in range(len(x)):
    x[i] = x[i] - width * 0.5
plt.xticks(x, ["", "", ""], fontsize=fsize)
ax.set_ylabel("Utility (%)", fontsize=30)
ax.set_ylim(0, 100)


ax2 = figure.add_subplot(212)
error_params = dict(elinewidth=1, ecolor='black', capsize=10)

rect1 = ax2.bar(x, TCP, width=width, label='TCP',color='white', edgecolor="green",
                    hatch='///',yerr=TCP_, error_kw=error_params)
for i in range(len(x)):
    x[i] = x[i] + width
rect2 = ax2.bar(x, UDP, width=width, label='UDP',color='white', edgecolor="blue",
                    hatch='+++', yerr=UDP_, error_kw=error_params)
# for i in range(len(x)):
#     x[i] = x[i] + width
# rect3 = ax2.bar(x, UDP_in, width=width, label='UDP (Upload)',color='white', edgecolor="y",
#                     hatch='+++', yerr=UDP_in_, error_kw=error_params)
ax2.set_xlabel("Roblox (PC) Throughput for different Games", fontsize=fsize)

auto_label(rect1)
auto_label(rect2)
ax2.legend(loc='upper left',edgecolor="white", fontsize=25)
for i in range(len(x)):
    x[i] = x[i] - width * 0.5
plt.xticks(x, namelist, fontsize=20)
ax2.set_ylim(0, 40)
ax2.set_ylabel("Throughput (KB/s)", fontsize=30)
plt.savefig(os.path.join(FIG_ROOT, "different_game_roblox.pdf"), bbox_inches='tight')
plt.show()