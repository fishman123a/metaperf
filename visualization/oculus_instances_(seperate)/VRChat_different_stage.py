import matplotlib.pyplot as plt
import pandas as pd
from decimal import Decimal
fsize = 20

def auto_label(rects):
    for rect in rects:
        height = Decimal(float(rect.get_height())).quantize(Decimal("0.0"))
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    fontsize=13,
                    textcoords="offset points",
                    ha='center', va='bottom')


vrchat_home_comp = pd.read_csv("Oculus_VRChat/oculus_home.csv")
vrchat_home_comp = vrchat_home_comp.loc[:, ["cpu_utilization_percentage", "gpu_utilization_percentage"]]
vrchat_home_tcp = 0
vrchat_home_udp = pd.read_csv("output/vrchat_home/throughput/UDP_172-65-200-252.csv")
vrchat_home_udp = vrchat_home_udp.loc[:, ["egress"]]

vrchat_party_comp = pd.read_csv("Oculus_VRChat/oculus_partyroom.csv")
vrchat_party_comp = vrchat_party_comp.loc[:, ["cpu_utilization_percentage", "gpu_utilization_percentage"]]
vrchat_party_tcp = pd.read_csv("output/vrchat_party_room(summer hotel)/throughput/TCP_210-0-146-155.csv")
vrchat_party_tcp = vrchat_party_tcp.loc[:, ["egress"]]/100
vrchat_party_udp = pd.read_csv("output/vrchat_party_room(summer hotel)/throughput/UDP_172-65-251-63.csv")
vrchat_party_udp = vrchat_party_udp.loc[:, ["egress"]]/100

vrchat_game_comp = pd.read_csv("Oculus_VRChat/oculus_murderer.csv")
vrchat_game_comp = vrchat_game_comp.loc[:, ["cpu_utilization_percentage", "gpu_utilization_percentage"]]
vrchat_game_tcp = pd.read_csv("output/vrchat_game_murder/throughput/TCP_13-224-163-76.csv")
vrchat_game_tcp = vrchat_game_tcp.loc[:, ["egress"]]/100
vrchat_game_udp = pd.read_csv("output/vrchat_game_murder/throughput/UDP_172-65-223-171.csv")
vrchat_game_udp = vrchat_game_udp.loc[:, ["egress"]]/100

namelist = ["Lobby", "Party Room (Summer Hotel)", "Game: Murder 4"]

figure = plt.figure(figsize=(16, 9))

CPU = [vrchat_home_comp["cpu_utilization_percentage"].mean(),
       vrchat_party_comp["cpu_utilization_percentage"].mean(),
       vrchat_game_comp["cpu_utilization_percentage"].mean()]

CPU_ = [vrchat_home_comp["cpu_utilization_percentage"].std(),
       vrchat_party_comp["cpu_utilization_percentage"].std(),
       vrchat_game_comp["cpu_utilization_percentage"].std()]

GPU = [vrchat_home_comp["gpu_utilization_percentage"].mean(),
       vrchat_party_comp["gpu_utilization_percentage"].mean(),
       vrchat_game_comp["gpu_utilization_percentage"].mean()]

GPU_ = [vrchat_home_comp["gpu_utilization_percentage"].std(),
       vrchat_party_comp["gpu_utilization_percentage"].std(),
       vrchat_game_comp["gpu_utilization_percentage"].std()]

TCP = [vrchat_home_tcp, vrchat_party_tcp.stack().mean(),
       vrchat_game_tcp.stack().mean()]
TCP_ = [vrchat_home_tcp, vrchat_party_tcp.stack().std(),
       vrchat_game_tcp.stack().std()]

UDP = [vrchat_home_udp.stack().mean(), vrchat_party_udp.stack().mean(),
       vrchat_game_udp.stack().mean()]
UDP_ = [vrchat_home_udp.stack().std(), vrchat_party_udp.stack().std(),
       vrchat_game_udp.stack().std()]

x = list(range(len(CPU)))
total_width, n = 0.8, len(CPU)
width = total_width/n


ax = figure.add_subplot(211)
error_params = dict(elinewidth=1, ecolor='black', capsize=5)

rect1 = ax.bar(x, CPU, width=width, label='CPU',color='white', edgecolor="red",
                    hatch='///',
               yerr=CPU_, error_kw=error_params
               )
for i in range(len(x)):
    x[i] = x[i] + width
rect2 = ax.bar(x, GPU, width=width, label='GPU',color='white', edgecolor="blue",
                    hatch='+++', yerr=GPU_, error_kw=error_params)


ax.set_xlabel("VRChat(Standalone) Computation in different Games",fontsize=fsize)

auto_label(rect1)
auto_label(rect2)
ax.legend(loc='upper right',edgecolor="white",fontsize=fsize)
for i in range(len(x)):
    x[i] = x[i] - width * 0.5
plt.xticks(x, ["", "", ""], fontsize=fsize)
plt.ylabel("CPU Utilization Rate", fontsize=fsize)
ax.set_ylim(0, 100)


ax2 = figure.add_subplot(212)
error_params = dict(elinewidth=1, ecolor='black', capsize=5)

rect1 = ax2.bar(x, TCP, width=width, label='TCP',color='white', edgecolor="green",
                    hatch='///',yerr=TCP_, error_kw=error_params)
for i in range(len(x)):
    x[i] = x[i] + width
rect2 = ax2.bar(x, UDP, width=width, label='UDP',color='white', edgecolor="blue",
                    hatch='+++', yerr=UDP_, error_kw=error_params)


ax2.set_xlabel("VRChat(Standalone) Throughput in different Games", fontsize=fsize)

auto_label(rect1)
auto_label(rect2)
ax2.legend(loc='upper right',edgecolor="white", fontsize=fsize)
for i in range(len(x)):
    x[i] = x[i] - width * 0.5
plt.xticks(x, namelist, fontsize=20)
ax2.set_ylim(0, 60)
plt.ylabel("Throughput (KBytes/s)", fontsize=fsize)

plt.savefig("Oculus_complex/different_game_vrchat.pdf", bbox_inches='tight')
plt.show()