import matplotlib.pyplot as plt
import pandas as pd

vrchat_comp = pd.read_csv("Oculus_VRChat/oculus_partyroom.csv")
vrchat_comp_ini = vrchat_comp.loc[50:200, ["cpu_utilization_percentage", "gpu_utilization_percentage"]].reset_index(drop=True)
vrchat_comp_inter = vrchat_comp.loc[250:480, ["cpu_utilization_percentage", "gpu_utilization_percentage"]].reset_index(drop=True)

vrchat_comm_tcp = pd.read_csv("output/vrchat_party_room(summer hotel)/throughput/trans_TCP_13-224-163-138.csv")
vrchat_comm_ini_tcp = vrchat_comm_tcp.loc[:150, ["egress"]].reset_index(drop=True)
vrchat_comm_inter_tcp = vrchat_comm_tcp.loc[150:, ["egress"]].reset_index(drop=True)

vrchat_comm_udp = pd.read_csv("output/vrchat_party_room(summer hotel)/throughput/trans_UDP_172-65-251-63.csv")
vrchat_comm_ini_udp = vrchat_comm_udp.loc[:150, ["egress"]].reset_index(drop=True)
vrchat_comm_inter_udp = vrchat_comm_udp.loc[150:, ["egress"]].reset_index(drop=True)

max = 40

figure = plt.figure(figsize=(32,18), dpi=80)
ax = figure.add_subplot(121)
ax.tick_params(pad=18, labelsize=34)
ax.plot(vrchat_comp_ini["cpu_utilization_percentage"], color="blue", linestyle="dashdot",
        label="CPU", linewidth=4)
ax.plot(vrchat_comp_ini["gpu_utilization_percentage"], color="red", linestyle="dashdot",
        label="GPU", linewidth=4)

ax.annotate('High CPU and GPU load', xy=(10, 80), xytext=(12, 85),
            xycoords='data', fontsize=50,
            arrowprops=dict(facecolor='black', shrink=0.05))

ax.set_xlim(0, max)
ax.set_xlabel("VRChat Avatar Creation Time/s", fontsize=40)
ax.set_ylabel("Utilization Percentage %", fontsize=40)
#ax.set_xlabel("VRChat Avatar Creation Time/s", fontsize=30)
ax.legend(loc='upper right', fontsize=40)

ax2 = figure.add_subplot(122)
ax2.tick_params(pad=18, labelsize=34)
ax2.plot(vrchat_comm_ini_tcp/1000, color="blue",
        label="TCP", linewidth=4)
ax2.plot(vrchat_comm_ini_udp/1000, color="red",
        label="UDP", linewidth=4)
ax2.annotate('Low Throughput', xy=(10, 80), xytext=(17, 130),
            xycoords='data', fontsize=50,
            arrowprops=dict(facecolor='black', shrink=0.05))
ax2.set_ylabel("Throughput KBytes/second", fontsize=40)
ax2.set_xlabel("VRChat Avatar Creation Time/s", fontsize=40)
ax2.legend(loc='upper right', fontsize=40)

ax2.set_xlim(0, max)
plt.savefig("Oculus_complex/VRChat_ini_comp_comm.pdf", bbox_inches='tight')
plt.show()

max = 50
figure = plt.figure(figsize=(32,18), dpi=80)
ax = figure.add_subplot(121)
ax.tick_params(pad=18, labelsize=34)
ax.plot(vrchat_comp_inter["cpu_utilization_percentage"], color="blue", linestyle="dashdot",
        label="CPU", linewidth=4)
ax.plot(vrchat_comp_inter["gpu_utilization_percentage"], color="red", linestyle="dashdot",
        label="GPU", linewidth=4)
ax.set_xlim(0, max)
ax.set_xlabel("VRChat Interaction Time/s", fontsize=40)
ax.set_ylabel("Utilization Percentage %", fontsize=40)
#ax.set_xlabel("VRChat Interaction Time/s", fontsize=30)
ax.legend(loc='upper right', fontsize=40)

ax2 = figure.add_subplot(122)
ax2.tick_params(pad=18, labelsize=34)
ax2.plot(vrchat_comm_inter_tcp/1000, color="blue",
        label="TCP", linewidth=4)
ax2.plot(vrchat_comm_inter_udp/1000, color="red",
        label="UDP", linewidth=4)

ax2.set_ylabel("Throughput KBytes/second", fontsize=40)
ax2.set_xlabel("VRChat Interaction Time/s", fontsize=40)
ax2.legend(loc='upper right', fontsize=40)
ax2.set_xlim(0, max)

ax2.annotate('No Obvious Relation', xy=(20, 80), xytext=(25, 130),
            xycoords='data', fontsize=50,
            arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig("Oculus_complex/VRChat_inter_comp_comm.pdf", bbox_inches='tight')
plt.show()