import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

vrchat = pd.read_csv("Oculus_VRChat/oculus_partyroom.csv")
roblox = pd.read_csv("Oculus_Roblox/roblox_1.csv")

beginning = 220

features = ["cpu_utilization_percentage", "gpu_utilization_percentage", "average_frame_rate", "available_memory_MB"]
features_ = ["CPU Utilization Rate", "GPU Utilization Rate", "Average Frame Rate", "Available Memory(MB)"]
name_list = ['Avatar Creation', 'Interaction', 'In General']


def auto_label(rects):
    for rect in rects:
        height = int(rect.get_height())
        plt.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    fontsize=13,
                    textcoords="offset points",
                    ha='center', va='bottom')




count = 0
for feature in features:
    vrchat_inter = vrchat.loc[beginning:, [feature]]
    roblox_inter = roblox.loc[80:, [feature]]
    vrchat_ini = vrchat.loc[:beginning, [feature]]
    roblox_ini = roblox.loc[:80, [feature]]
    vrchat_gen = vrchat.loc[:, [feature]]
    roblox_gen = roblox.loc[:, [feature]]


    Roblox = [roblox_ini.stack().mean(), roblox_inter.stack().mean(), roblox_gen.stack().mean()]
    Roblox_std = [roblox_ini.stack().std(), roblox_inter.stack().std(), roblox_gen.stack().std()]
    VRChat = [vrchat_ini.stack().mean(), vrchat_inter.stack().mean(), vrchat_gen.stack().mean()]
    VRChat_std = [vrchat_ini.stack().std(), vrchat_inter.stack().std(), vrchat_gen.stack().std()]
    error_params = dict(elinewidth=1, ecolor='black', capsize=5)
    x = list(range(len(Roblox)))
    total_width, n = 0.8, len(Roblox)
    width = total_width/n

    rect1 = plt.bar(x, Roblox, width=width, label='Roblox(PC Display)',color='white', edgecolor="red",
                    hatch='///',yerr=Roblox_std, error_kw=error_params)
    for i in range(len(x)):
        x[i] = x[i] + width
    rect2 = plt.bar(x, VRChat, width=width, label='VRChat(Standalone)',color='white', edgecolor="blue",
                    hatch='+++', yerr=VRChat_std, error_kw=error_params)
    plt.ylabel(features_[count],fontsize=15)

    auto_label(rect1)
    auto_label(rect2)

    count += 1
    plt.legend(loc='upper right',fontsize=12,edgecolor="white")
    for i in range(len(x)):
        x[i] = x[i] - width * 0.5
    plt.xticks(x, name_list, fontsize=15)
    plt.ylim(0, max(roblox_ini.stack().mean(), roblox_inter.stack().mean(),
                    vrchat_ini.stack().mean(), vrchat_inter.stack().mean(),
                    roblox_gen.stack().mean(), vrchat_gen.stack().mean())*1.3)
    plt.savefig("Output_bars_Oculus/" +feature + ".pdf",bbox_inches = 'tight')
    plt.show()