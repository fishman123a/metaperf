import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from src.network.utils import PROJECT_ROOT, throughput_integrate_by_protocol
import seaborn as sns

from visualization_tools.utils import FIG_ROOT



mc_connect = throughput_integrate_by_protocol(pd.concat([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/mc/connect/%d/network/throughput/concat.csv" % i), index_col=0)
    for i in range(1, 11)], ignore_index=True
))
print(mc_connect)
mc_android_connect = throughput_integrate_by_protocol(pd.concat([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/mc_android/connect/%d/network/throughput/concat.csv" % i), index_col=0)
    for i in range(1, 9)], ignore_index=True
))

roblox_connect = throughput_integrate_by_protocol(pd.concat([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/roblox/connect/%d/network/throughput/concat.csv" % i), index_col=0)
    for i in range(1, 6)], ignore_index=True
))

roblox_android_connect = throughput_integrate_by_protocol(pd.concat([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/roblox_android/connect/%d/network/throughput/concat.csv" % i), index_col=0)
    for i in range(2, 6)], ignore_index=True
))


fig, ax = plt.subplots(figsize=(16, 9), dpi=300)

data_a = [mc_connect.TCP / 1024, roblox_connect.TCP / 1024]
data_b = [mc_android_connect.TCP / 1024, roblox_android_connect.TCP / 1024]

for a, b in zip (data_a, data_b):
    print(a.mean(), b.mean())
ticks = ['Minecraft', 'Roblox'] #, 'Interaction']


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

lw = 3
bpl = ax.boxplot(data_a, positions=np.array(range(len(data_a))) * 2.0 - 0.3, sym='', widths=0.5, showfliers=True, showmeans=True,
                  whiskerprops=dict(linestyle='--', linewidth=lw),
                  boxprops=dict(linestyle='--', linewidth=lw),
                  capprops=dict(linestyle='--', linewidth=lw),
                  medianprops=dict(linestyle='--', linewidth=lw), )
bpr = ax.boxplot(data_b, positions=np.array(range(len(data_b))) * 2.0 + 0.3, sym='', widths=0.5, showfliers=True,showmeans=True,
                  whiskerprops=dict(linestyle='-', linewidth=lw),
                  boxprops=dict(linestyle='-', linewidth=lw),
                  capprops=dict(linestyle='-', linewidth=lw),
                  medianprops=dict(linestyle='-', linewidth=lw),
                  )

# set_box_color(bpl, '#D7191C')  # colors are from http://colorbrewer2.org/
# set_box_color(bpr, '#2C7BB6')

# draw temporary red and blue lines and use them to create a legend
# plt.plot([], c='#D7191C', ls='--', label='Without Entity')
# plt.plot([], c='#2C7BB6', label='With Entities')
plt.plot([], c='black', ls='--', label='PC')
plt.plot([], c='black', label='Phone')
plt.legend(fontsize=60, edgecolor="white")

plt.xticks(range(0, len(ticks) * 2, 2), ticks, fontsize=60)

# plt.boxplot([mc_connect_no_entity,
#              mc_stand_no_entity],
#             showmeans=True,
#             positions=[0.6, 2.6])
#
# plt.boxplot([mc_connect_entity,
#              mc_stand_entity],
#             showmeans=True,
#             positions=[1.2, 3.2])

# ax = sns.boxplot(x=df['stage'], y=df['rtt'], hue=df['entity'], width=0.5, whiskerprops=dict(linestyle='-', linewidth=1.0
#                                                                                             , color='black'))
# handles, labels = ax.get_legend_handles_labels()
# ax.legend(handles=handles, labels=labels)

plt.ylim(0, 900)
plt.yticks([200, 400, 600, 800], fontsize=40)
every_nth = 1
for n, label in enumerate(ax.yaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)

plt.ylabel("Throughput (KB/s)", fontsize=60)
plt.tight_layout()

plt.savefig(os.path.join(FIG_ROOT, "mc_roblox_throughput_interplatform.pdf"))
