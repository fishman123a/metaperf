import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt

vrchat = pandas.read_csv("Oculus_VRChat/oculus_partyroom.csv")
roblox = pandas.read_csv("Oculus_Roblox/roblox_1.csv")

beginning = 80

features = ["cpu_utilization_percentage", "gpu_utilization_percentage", "average_frame_rate", "available_memory_MB"]
features_ = ["CPU Utilization Rate", "GPU Utilization Rate", "Average Frame Rate", "Available Memory(MB)"]
count = 0
for feature in features:
    vrchat_slice = vrchat.loc[220:, [feature]]
    roblox_slice = roblox.loc[beginning:, [feature]]

    vrchat_slice['cdf'] = vrchat_slice.rank(method = 'average', pct = True)
    roblox_slice['cdf'] = roblox_slice.rank(method = 'average', pct = True)

    vrchat_slice = vrchat_slice.sort_values(feature)
    roblox_slice = roblox_slice.sort_values(feature)

    figure = plt.figure(figsize=(16, 9), dpi=80)
    # set up the margin
    ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
    # set up the tick size
    ax.tick_params(pad=18, labelsize=36)
    ax.plot(roblox_slice[feature], roblox_slice['cdf'], label="Roblox(PC Display)",
            linestyle="dashdot",
            color="red", linewidth=5)
    ax.plot(vrchat_slice[feature], vrchat_slice['cdf'], label="VRChat(Standalone)",
            #linestyle="dashed",
            color="blue", linewidth=5)
    plt.legend(loc='lower right', fontsize=40)
    ax.set_xlabel(features_[count], fontsize=40)
    ax.set_ylim(0, 1)
    ax.set_ylabel('CDF', fontsize=40)
    plt.savefig("Output_CDFs_Oculus_Interaction/interaction_" + feature + ".pdf", bbox_inches = 'tight')
    plt.show()
    figure.clf()

    vrchat_slice = vrchat.loc[:220, [feature]]
    roblox_slice = roblox.loc[:beginning, [feature]]
    vrchat_slice['cdf'] = vrchat_slice.rank(method='average', pct=True)
    roblox_slice['cdf'] = roblox_slice.rank(method='average', pct=True)
    vrchat_slice = vrchat_slice.sort_values(feature)
    roblox_slice = roblox_slice.sort_values(feature)

    figure = plt.figure(figsize=(16, 9), dpi=80)
    # set up the margin
    ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
    # set up the tick size
    ax.tick_params(pad=18, labelsize=36)
    ax.plot(roblox_slice[feature], roblox_slice['cdf'], label="Roblox(PC Display)",
            linestyle="dashdot",
            color="red", linewidth=5)
    ax.plot(vrchat_slice[feature], vrchat_slice['cdf'], label="VRChat(Standalone)",
            #linestyle="dashed",
            color="blue", linewidth=5)
    plt.legend(loc='lower right', fontsize=40)
    ax.set_xlabel(features_[count], fontsize=40)
    ax.set_ylim(0, 1)
    ax.set_ylabel('CDF', fontsize=40)
    plt.savefig("Output_CDFs_Oculus_Initialization/initialization_" + feature + ".pdf", bbox_inches = 'tight')
    plt.show()
    figure.clf()

    vrchat_slice = vrchat.loc[:,[feature]]
    roblox_slice = roblox.loc[:,[feature]]
    vrchat_slice['cdf'] = vrchat_slice.rank(method='average', pct=True)
    roblox_slice['cdf'] = roblox_slice.rank(method='average', pct=True)
    vrchat_slice = vrchat_slice.sort_values(feature)
    roblox_slice = roblox_slice.sort_values(feature)

    figure = plt.figure(figsize=(16, 9), dpi=80)
    # set up the margin
    ax = figure.add_axes([0.115, 0.15, 0.8, 0.8])
    # set up the tick size
    ax.tick_params(pad=18, labelsize=36)
    ax.plot(roblox_slice[feature], roblox_slice['cdf'], label="Roblox(PC Display)",
            linestyle="dashdot",
            color="red", linewidth=5)
    ax.plot(vrchat_slice[feature], vrchat_slice['cdf'], label="VRChat(Standalone)",
            # linestyle="dashed",
            color="blue", linewidth=5)
    plt.legend(loc='lower right', fontsize=40)
    ax.set_xlabel(features_[count], fontsize=40)
    ax.set_ylim(0, 1)
    ax.set_ylabel('CDF', fontsize=40)
    plt.savefig("Output_CDFs_Oculus_InGeneral/general_" + feature + ".pdf", bbox_inches='tight')
    plt.show()
    figure.clf()
    count += 1