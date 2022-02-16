import matplotlib.pyplot as plt
import pandas as pd

vrchat_comp = pd.read_csv("Oculus_VRChat/oculus_murderer.csv")
vrchat_comp = vrchat_comp.loc[:300, ["cpu_utilization_percentage", "gpu_utilization_percentage"]].reset_index(drop=True)

vrchat_throuput_UDP = pd.read_csv("output/vrchat_game_murder/throughput/trans_UDP_172-65-223-171.csv")
vrchat_throuput_UDP = vrchat_throuput_UDP.loc[100:, ["egress"]].reset_index(drop=True)

vrchat_throuput_TCP = pd.read_csv("output/vrchat_game_murder/throughput/trans_TCP_13-224-163-76.csv")
vrchat_throuput_TCP = vrchat_throuput_TCP.loc[100:, ["egress"]].reset_index(drop=True)

figure = plt.figure(figsize=(32,18), dpi=80)
ax = figure.add_subplot(121)
ax.tick_params(pad=18, labelsize=34)
ax.plot(vrchat_comp["cpu_utilization_percentage"], color="blue", linestyle="dashdot",
        label="CPU", linewidth=4)
ax.plot(vrchat_comp["gpu_utilization_percentage"], color="red", linestyle="dashdot",
        label="GPU", linewidth=4)
ax.set_xlim(0, 300)
ax.set_ylabel("Utilization Percentage %", fontsize=40)
ax.set_xlabel("Time/s", fontsize=40)
ax.legend(loc='upper right', fontsize=40)

ax2 = figure.add_subplot(122)
ax2.tick_params(pad=18, labelsize=34)
ax2.plot(vrchat_throuput_UDP["egress"]/1000, color="blue",
        label="UDP Flow", linewidth=4)
ax2.plot(vrchat_throuput_TCP["egress"]/1000, color="red",
        label="TCP Flow", linewidth=4)

ax2.set_ylabel("Throughput KBytes/second", fontsize=40)
ax2.set_xlabel("VRChat Time/s", fontsize=40)
ax2.legend(loc='upper right', fontsize=40)
ax2.set_xlim(0, 300)
plt.savefig("Oculus_complex/real_time_comm_comp.pdf", bbox_inches='tight')
plt.show()
