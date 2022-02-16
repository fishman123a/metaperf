import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.network.utils import PROJECT_ROOT, throughput_integrate_by_protocol
from visualization_tools.utils import FIG_ROOT

vrchat_connect_throughput = throughput_integrate_by_protocol(pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/vrchat/connection/2/network/throughput/concat.csv")))



vrchat_connect_gpu = pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/vrchat/connection/2/computation/gpu.csv"))

vrchat_connect_cpu = pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/vrchat/connection/2/computation/cpu.csv"))

vrchat_connect_ram = pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/vrchat/connection/2/computation/ram.csv"))


fig, axes = plt.subplots(2, dpi=300, figsize=(16, 10))
ax1 = axes[0]
ax2 = axes[1]
legend_font = 35
ylabel_font = 50
linewidth=4
ax1.set_yscale('symlog')
every_nth = 2

ax1.plot(vrchat_connect_throughput.index, vrchat_connect_throughput.TCP / 1024, c='red', ls='--', label="TCP Flow", lw=linewidth)
ax1.plot(vrchat_connect_throughput.index, vrchat_connect_throughput.UDP / 1024, c='blue', label="UDP Flow", lw=linewidth)
ax1.annotate("midway spike", xy=(22, 3000), xytext=(23, 15000),
            arrowprops=dict(arrowstyle="->", facecolor='red', lw=3), fontsize=legend_font, va="bottom", ha="left")
ax1.annotate("end elevation", xy=(34, 2000), xytext=(33, 1500),
            arrowprops=dict(arrowstyle="->", facecolor='red', lw=3), fontsize=legend_font, va="top", ha="right")
for n, label in enumerate(ax1.yaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
ax1.get_xaxis().set_visible(False)
ax1.set_ylabel("Throughput\n(KB/s)", fontsize=ylabel_font)
ax1.set_ylim(0, 100000)
ax2.plot(vrchat_connect_cpu.index, vrchat_connect_cpu.total * 100, c='red', ls='--', label="CPU", lw=linewidth)
ax2.plot(vrchat_connect_gpu.index, vrchat_connect_gpu.core_ocp  * 100, c='blue', label="GPU", lw=linewidth)
ax2.annotate("end elevation", xy=(34, 80), xytext=(38, 50),
            arrowprops=dict(arrowstyle="->", facecolor='red', lw=3), fontsize=legend_font, va="top", ha="right")
every_nth = 1
for n, label in enumerate(ax2.yaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
# ax2.get_xaxis().set_visible(False)
ax2.fill_between(np.arange(21, 31), 0, 100, color='y', alpha=0.4) #, label='GPU Highland')
ax2.set_ylabel('Utility (%)', fontsize=ylabel_font)
ax2.set_xlabel('Time (s)', fontsize=70)
ax2.text(25.5, 80, 'midway highland\n(GPU)', fontsize=legend_font, ha='center', va='center')
ax2.set_ylim(0, 100)
# ax3.plot(vrchat_connect_ram.index, vrchat_connect_ram.ratio, c='red', ls='--', label='Memory Usage', lw=linewidth)
# ax3.plot(vrchat_connect_gpu.index, vrchat_connect_gpu.mem_ocp, c='blue', label='Video Memory Usage', lw=linewidth)
# every_nth = 2
# for n, label in enumerate(ax3.yaxis.get_ticklabels()):
#     if n % every_nth != 0:
#         label.set_visible(False)
#
# ax3.set_xlabel('Time (s)', fontsize=ylabel_font)
# ax3.set_ylabel('Usage', fontsize=ylabel_font)
for ax in axes:
    ax.legend(loc="upper left", fontsize=legend_font, edgecolor="white")
    ax.set_xlim(13, 38)
    ax.tick_params(axis='both', labelsize=legend_font)
plt.tight_layout()
plt.savefig(os.path.join(FIG_ROOT, 'vrchat_connect_timeline.pdf'))