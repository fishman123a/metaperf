import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.network.utils import PROJECT_ROOT
from visualization_tools.utils import FIG_ROOT

WINDOWS_LIST = ['mc', 'roblox', 'vrchat']
ANDROID_LIST = ['mc_android', 'roblox_android']

mc_connect = np.concatenate([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/mc/connect_many_entity/%d/computation/gpu.csv" % i))[
        'core_ocp'].to_numpy()
    for i in range(1, 6)]
)

mc_interaction = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/mc/stand_still_many_entity/computation/gpu.csv"))[
    'core_ocp'].to_numpy()

mc_general = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/mc/stand_still_no_entity/computation/gpu.csv"))[
    'core_ocp'].to_numpy()


roblox_connect = np.concatenate([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/roblox/connect/%d/computation/gpu.csv" % i))[
        'core_ocp'].to_numpy()
    for i in range(1, 6)]
)

roblox_interaction = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/roblox/rub/computation/gpu.csv"))[
    'core_ocp'].to_numpy()

roblox_general = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/roblox/stand_still/computation/gpu.csv"))[
    'core_ocp'].to_numpy()

vrchat_connect = np.concatenate([
    pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/vrchat/connection/%d/computation/gpu.csv" % i))[
        'core_ocp'].to_numpy()
    for i in range(2, 6)]
)

vrchat_interaction = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/vrchat/item_interaction/computation/gpu.csv"))[
    'core_ocp'].to_numpy()

vrchat_general = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/vrchat/no_model_loading/computation/gpu.csv"))[
    'core_ocp'].to_numpy()

def get_mean_df(dats, titles):
    df = pd.DataFrame(index=["mean", "var"])
    for d, t in zip(dats, titles):
        df[t] = [np.mean(d * 100), np.std(d * 100)]
    return df


def run(fig, ax, connection,
        interaction,
        general, output_file, y_lim=70):
    plt.rcParams['pdf.fonttype'] = 42

    error_params = dict(elinewidth=1, ecolor='gray', capsize=2)

    edge_colors = ['b', 'r', 'g', 'c', 'y']
    hatches = ['///', '\\\\\\', '+++', 'xx', 'oo', 'OO', '..', '**']
    total_width, n = 0.8, 3
    width = total_width / n
    x = list(range(n))
    y_max = 0
    for col, c, h in zip(connection.columns.values, edge_colors, hatches):
        mean_list = [connection.at['mean', col], interaction.at['mean', col] if col in interaction.columns else 0,
                     general.at['mean', col]]

        std_list = [connection.at['var', col], interaction.at['mean', col] if col in interaction.columns else 0,
                    general.at['var', col]]
        y_max = max((np.array(mean_list) + np.array(std_list)).tolist() + [y_max])
        label = col

        rect1 = plt.bar(x, mean_list, width=width, label=label, color='white', edgecolor=c,
                        hatch=h, yerr=std_list, error_kw=error_params)

        for i in range(len(x)):
            x[i] = x[i] + width

        for rect in rect1:
            height = rect.get_height()
            if height == 0:
                continue
            plt.annotate(round(height),  # put the detail data
                         xy=(rect.get_x() + rect.get_width() / 2, height),  # get the center location.
                         xytext=(0, 3),  # 3 points vertical offset
                         fontsize=30,
                         textcoords="offset points",
                         ha='center', va='bottom')
    for i in range(len(x)):
        x[i] = x[i] - 2 * width
    lgd = ax.legend(loc='upper left', fontsize=40, edgecolor="white")
    lgd.get_frame().set_alpha(0)
    plt.xticks(x, ['Avatar\nCreation', 'Interaction', 'Regular\nGameplay'], fontsize=50)
    plt.yticks([25, 50, 75, 100], fontsize=40)
    ax.set_ylabel("GPU Utilization\nPercentage (%)", fontsize=50)
    ax.set_ylim(0, y_lim)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_ROOT, output_file))



if __name__ == '__main__':
    fs = (16, 9,)
    dpi = 300
    fig1, ax1 = plt.subplots(figsize=fs, dpi=dpi)
    run(fig1, ax1, connection=get_mean_df([mc_connect, roblox_connect, vrchat_connect],
                                        ['MC', 'Roblox', 'VR Chat']),
        interaction=get_mean_df([mc_interaction, roblox_interaction, vrchat_interaction],
                                ['MC', 'Roblox', 'VR Chat']),
        general=get_mean_df([mc_general, roblox_general, vrchat_general],
                            ['MC', 'Roblox', 'VR Chat']), output_file="gpu_bar_pc.pdf"),

