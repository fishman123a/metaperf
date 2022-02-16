import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt


def gen_cdf(y,bin_count):
    hist, bin_edges = np.histogram(y,bins=bin_count)
    cdf = np.cumsum(hist) / np.sum(hist)
    return cdf
bins = 50
x = []
for i in range(bins):
    x.append(i / 50)



vrchat = pandas.read_csv("Oculus_VRChat/VRChat_1.csv")
roblox = pandas.read_csv("Oculus_Roblox/roblox_1.csv")

beginning = 80

features = ["cpu_utilization_percentage", "gpu_utilization_percentage", "average_frame_rate"]
features_ = ["CPU Utilization Rate", "GPU Utilization Rate", "Average Frame Rate"]
count = 0
for feature in features:
    vrchat_slice = vrchat.loc[beginning:, [feature]]
    roblox_slice = roblox.loc[beginning:, [feature]]
    vrchat_cdf = gen_cdf(vrchat_slice, bins)
    roblox_cdf = gen_cdf(roblox_slice, bins)

    figure = plt.figure(figsize=(16, 9), dpi=80)
    # set up the margin
    ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
    # set up the tick size
    ax.tick_params(pad=18, labelsize=36)
    ax.plot(x, roblox_cdf, label="Roblox",
            linestyle="dashdot",
            color="red", linewidth=5)
    ax.plot(x, vrchat_cdf, label="VRChat",
            linestyle="dashed",
            color="blue", linewidth=5)
    plt.legend(loc='upper left', fontsize=40)
    ax.set_xlabel('Normalized ' + features_[count], fontsize=40)
    count+=1
    ax.set_ylabel('CDF', fontsize=40)
    plt.savefig("interaction_" + feature + ".pdf")