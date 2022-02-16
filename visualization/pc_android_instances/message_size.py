import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.network.utils import PROJECT_ROOT, Role
from visualization_tools.throughput_box import WINDOWS_LIST
from visualization_tools.utils import setup_plt, FIG_ROOT


def get_message_size(game, scene):
    filtered_dir = os.path.join(PROJECT_ROOT, 'data', game, scene,'network\\filtered_csvs')
    sizes = dict()
    for file in os.listdir(filtered_dir):
        df = pd.read_csv(os.path.join(filtered_dir, file))
        key = file.split("_")[0]
        if key=='RakNet':
            key = 'UDP'
        if key in sizes.keys():
            sizes[key] = np.concatenate((sizes[key], df[df.role == Role.SERVER.value].len.astype(int).to_numpy()))
        else:
            sizes[key] = df[df.role == Role.SERVER.value].len.astype(int).to_numpy()
    return sizes

def message_size_box(figure, ax, game_list, scene_list):
    df = pd.DataFrame(index=["mean", "var"])
    for g, s in zip(game_list, scene_list):
        sizes = get_message_size(g, s)
        for key, value in sizes.items():
            df['%s [%s]' % (g, key)] = [np.mean(value), np.std(value)]
    return df

def run(fig, ax):
    setup_plt()

    connection = message_size_box('', '', WINDOWS_LIST, [
        'connect\\2', 'connect\\2', 'connection\\2'
    ])
    interaction = message_size_box('', '', WINDOWS_LIST, [
        'move_battle', 'rub', 'item_interaction'
    ])

    error_params = dict(elinewidth=1, ecolor='gray', capsize=2)\

    edge_colors = ['b', 'r', 'g', 'c', 'y']
    hatches = ['///', '\\\\\\', '---', '+++', 'xxx', 'ooo', 'OOO', '...', '***']
    width = 0.13
    x = np.array([0.0, 1.0])
    y_max = 0
    for col, c, h in zip(connection.columns.values, edge_colors, hatches):
        mean_list = [connection.at['mean', col], interaction.at['mean', col] if col in interaction.columns else 0]

        std_list = [connection.at['var', col], interaction.at['mean', col] if col in interaction.columns else 0]
        y_max = max((np.array(mean_list) + np.array(std_list)).tolist() + [y_max])
        label = col

        rect1 = plt.bar(x, mean_list, width=width, label=label, color='white', edgecolor=c,
                        hatch=h, yerr=std_list, error_kw=error_params)
        for rect in rect1:
            height = int(rect.get_height())
            if height == 0:
                continue
            plt.annotate('{}'.format(height),  # put the detail data
                         xy=(rect.get_x() + rect.get_width() / 2, height),  # get the center location.
                         xytext=(0, 3),  # 3 points vertical offset
                         fontsize=10,
                         textcoords="offset points",
                         ha='center', va='bottom')
        x += width
    ax.legend(loc='upper right',fontsize=15,edgecolor="white")
    x = (x - np.array([0.0, 1.0])) / 2 + np.array([0.0, 1.0]) - width/2
    plt.xticks(x, ['Avatar Creation', 'Interaction'], fontsize=25)
    plt.yticks(fontsize=18)
    ax.set_ylabel("Average Packet Payload\nLength (Bytes)", fontsize=25)
    ax.set_ylim(0, y_max+200)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_ROOT, "pkt_payload_pc.pdf"))
    plt.show()

    # output_df = pd.concat([connection, interaction], ignore_index=True).drop(index=[1, 3])
    # output_df.index = ["avatar creation", "interaction"]
    #
    # ax1.set_ylabel("Packet Payload (Bytes)")
    # bars = output_df.plot(kind='bar', ax=ax1)
    # plt.xticks(rotation=90)
    # plt.show()
    # print(output_df)


if __name__ == '__main__':
    fig1, ax1 = plt.subplots(dpi=300)
    run(fig1, ax1)

