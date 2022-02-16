import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches

from visualization_tools.utils import FIG_ROOT, load_data, linestyles
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

WINDOWS_LIST = ['mc', 'roblox', 'vrchat']
ANDROID_LIST = ['mc_android', 'roblox_android']

colors = ['b', 'r', 'g', 'c', 'y']

def throughput_cdf(figure, ax, dat_dict, game_list, scene_list, label_list, output_file, interval=0.1):
    style_idx = 0
    def plot_cdf(y, label):
        global style_idx
        count, bins_count = np.histogram(y, bins=50000)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        # x = bins_count[1:]
        # xnew = np.linspace(x.min(), x.max(), 3000)
        # spl = make_interp_spline(x, cdf, k=3)
        # power_smooth = spl(xnew)
        ax.plot(np.concatenate(([bins_count[1]], bins_count[1:])), np.concatenate((np.array([0]), cdf)), c=colors[style_idx], label=label, lw=4, ls=list(linestyles.items())[style_idx][1])
        style_idx = (style_idx + 1) % len(list(linestyles.items()))
    for g, s, l in zip(game_list, scene_list, label_list):
        df = dat_dict[g][s[0]]['throughput']
        df_concat = df.T.groupby([x.split('_')[0] for x in df.T.index.values]).sum().T
        df_concat = df_concat.groupby(df_concat.index // 10).sum()
        if len(s) > 1:
            for s_i in s[1:]:
                df = dat_dict[g][s_i]['throughput']
                df_concat_i = df.T.groupby([x.split('_')[0] for x in df.T.index.values]).sum().T
                df_concat_i = df_concat_i.groupby(df_concat_i.index // 10).sum()
                df_concat = pd.concat([df_concat, df_concat_i], axis=0)

        df_columns = df_concat.columns
        print(df_columns)
        for col in df_columns:
            prot = col
            if col == 'RakNet':
                prot = 'UDP'
            label = '%s [%s]' % (g, prot)
            plot_cdf(df_concat[col] / 1024, label)

    ax.set_ylabel("CDF", fontsize=60)
    ax.set_xlabel("Throughput (KB/s)", fontsize=60)
    plt.legend(fontsize=40, edgecolor="white")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_ROOT, output_file))

style_idx = 0
def throughput_realtime(figure, ax, dat_dict, game_list, scene_list, label_list, output_file, interval=0.1):
    global style_idx
    style_idx = 0
    def plot_realtime(y, label):
        global style_idx

        x = np.arange(0, len(y), 1)
        xnew = np.linspace(x.min(), x.max(), 100)
        spl = make_interp_spline(x,  y, k=2)
        power_smooth = spl(xnew)

        ax.plot(xnew, power_smooth, c=colors[style_idx], label=label, lw=3, ls=list(linestyles.items())[style_idx][1])
        style_idx = (style_idx + 1) % len(list(linestyles.items()))

    for g, s, l in zip(game_list, scene_list, label_list):
        df = dat_dict[g][s[0]]['throughput']
        df_concat = df.T.groupby([x.split('_')[0] for x in df.T.index.values]).sum().T
        df_concat = df_concat.groupby(df_concat.index // 10).sum()
        if len(s) > 1:
            for s_i in s[1:]:
                df = dat_dict[g][s_i]['throughput']
                df_concat_i = df.T.groupby([x.split('_')[0] for x in df.T.index.values]).sum().T
                df_concat_i = df_concat_i.groupby(df_concat_i.index // 10).sum()
                df_concat = pd.concat([df_concat, df_concat_i], axis=0)

        df_columns = df_concat.columns
        print(df_columns)
        for col in df_columns:
            prot = col
            if col == 'RakNet':
                prot = 'UDP'
            label = '%s [%s]' % (g, prot)
            plot_realtime(df_concat[col] / 1024, label)

    ax.set_ylabel("Throughput (KB/s)", fontsize=42)
    ax.set_xlabel("Time (s)", fontsize=40)
    plt.legend(fontsize=20, edgecolor="white")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_ROOT, output_file))

def throughput_box(figure, ax, dat_dict, game_list, scene_list, label_list, output_file, interval=0.1):
    df_all = pd.DataFrame()
    for g, s, l in zip(game_list, scene_list, label_list):
        df = dat_dict[g][s[0]]['throughput']
        df_concat = df.T.groupby([x.split('_')[0] for x in df.T.index.values]).sum().T
        df_concat = df_concat.groupby(df_concat.index // 10).sum()
        if len(s) > 1:
            for s_i in s[1:]:
                df = dat_dict[g][s_i]['throughput']
                df_concat_i = df.T.groupby([x.split('_')[0] for x in df.T.index.values]).sum().T
                df_concat_i = df_concat_i.groupby(df_concat_i.index // 10).sum()
                df_concat = pd.concat([df_concat, df_concat_i], axis=0)
        df_columns = df_concat.columns
        for col in df_columns:
            label = '%s\n[%s]' % (g, col)
            if col == 'RakNet':
                label = '%s\n[%s]' % (g, 'UDP')
            df_all = pd.concat([df_all, pd.DataFrame({label: df_concat[col].to_numpy() / 1024})], axis=1)
            print(df_concat[col])
    print(df_all.info())
    print([df_all[col].mean() for col in df_all])
    df_all.plot(kind='box', ax=ax, showmeans=True,
                # flierprops=dict(linestyle='-', linewidth=1.5),
                whiskerprops=dict(linestyle='-', linewidth=3),
                boxprops=dict(linewidth=3),
                capprops=dict(linestyle='-', linewidth=3),
                medianprops=dict(linestyle='--', linewidth=1),
                fontsize=40)
    ax.set_ylabel("Throughput (KB/s)", fontsize=60)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_ROOT, output_file))


if __name__ == '__main__':
    win_data = load_data(WINDOWS_LIST)
    android_data = load_data(ANDROID_LIST)
    fs = (16, 9,)
    dpi = 300
    # plt.rcParams['pdf.fonttype'] = 42

    # plt.gca().set_ylim(bottom=0, top=35)
    # plt.gca().set_xlim(left=0, right=5)
    # fig1, ax1 = plt.subplots(figsize=fs, dpi=dpi)
    # plt.ylim(bottom=0, top=35)
    # plt.yticks(fontsize=40)
    # throughput_box(fig1, ax1, win_data, WINDOWS_LIST, [
    #     ['battle'], ['rub'], ['item_interaction']
    # ], ['Minecraft', 'Roblox', 'VRchat'], "througput_box_interaction_pc.pdf")
    #
    # fig2, ax2 = plt.subplots(figsize=fs, dpi=dpi)
    # plt.ylim(bottom=0, top=175)
    # plt.yticks(fontsize=40)
    # throughput_box(fig2, ax2, android_data, ANDROID_LIST, [
    #     ['battle'], ['rub']
    # ], ['Minecraft', 'Roblox'],"througput_box_interaction_android.pdf")
    #
    # fig3, ax3 = plt.subplots(figsize=fs, dpi=dpi)
    # ax3.annotate('Large Downstream Spike', xy=(3.75, 4000), xytext=(2, 8000),
    #              arrowprops=dict(arrowstyle="->", facecolor='red', lw=3),
    #              fontsize=40, va="center", ha="center")
    # ax3.add_patch(patches.Rectangle((3.8, 25000), 0.4, -24400,
    #                                 linewidth=4, edgecolor='r', facecolor='none'))
    # plt.yscale('symlog')
    # plt.ylim(bottom=0, top=30000)
    # plt.yticks(fontsize=40)
    # throughput_box(fig3, ax3, win_data, WINDOWS_LIST, [
    #       ['connect-%d' % i for i in range(1, 11)], ['connect-%d' % i for i in range(1, 6)], ['connection-%d' % i for i in range(2,6)]
    # ], ['Minecraft', 'Roblox', 'VRchat'], "througput_box_connection_pc.pdf")

    # fig4, ax4 = plt.subplots(figsize=fs, dpi=dpi)
    # plt.yscale('linear')
    # plt.ylim(bottom=0, top=1000)
    # throughput_box(fig4, ax4, android_data, ANDROID_LIST, [
    #      ['connect-%d' % i for i in range(1, 9)], ['connect-%d' % i for i in range(1, 6)]
    # ], ['Minecraft', 'Roblox'], "througput_box_connection_android.pdf")
    #
    #
    # fig5, ax5 = plt.subplots(figsize=(16,9), dpi=dpi)
    # plt.xticks(fontsize=30)
    # plt.yticks(fontsize=30)
    # plt.ylim(bottom=0, top=1)
    # plt.xlim(left=0, right=25)
    # plt.locator_params(axis='x', nbins=3)
    # throughput_cdf(fig5, ax5, win_data, WINDOWS_LIST, [
    #     ['battle'], ['rub'], ['item_interaction']
    # ], ['Minecraft', 'Roblox', 'VRchat'], "througput_cdf_interaction_pc.pdf")
    #
    # fig6, ax6 = plt.subplots(figsize=(9,9), dpi=dpi)
    # plt.xticks(fontsize=30)
    # plt.locator_params(axis='x', nbins=3)
    # plt.yticks(fontsize=30)
    # plt.ylim(bottom=0, top=1)
    # plt.xlim(left=0, right=500)
    # throughput_cdf(fig6, ax6, win_data, WINDOWS_LIST, [
    #     ['connect-%d' % i for i in range(1, 11)], ['connect-%d' % i for i in range(1, 6)], ['connection-%d' % i for i in range(2,6)]
    # ], ['Minecraft', 'Roblox', 'VRchat'], "througput_cdf_connection_pc.pdf")
    #
    # fig7, ax7 = plt.subplots(figsize=(16,9), dpi=dpi)
    # plt.xticks(fontsize=30)
    # plt.yticks(fontsize=30)
    # plt.ylim(bottom=0, top=35)
    # plt.xlim(left=0, right=25)
    # plt.locator_params(axis='x', nbins=3)
    # throughput_realtime(fig7, ax7, win_data, WINDOWS_LIST, [
    #     ['battle'], ['rub'], ['item_interaction']
    # ], ['Minecraft', 'Roblox', 'VRchat'], "througput_realtime_interaction_pc.pdf")
    #
    fig8, ax8 = plt.subplots(figsize=(16, 9), dpi=dpi)
    plt.xticks(fontsize=40)
    plt.yticks(fontsize=40)
    plt.ylim(bottom=0, top=1)
    plt.xlim(left=0, right=60)
    plt.locator_params(axis='x', nbins=3)
    throughput_cdf(fig8, ax8, win_data, WINDOWS_LIST, [
        ['stand_still_many_entity'], ['stand_still'], ['stand_still']
    ], ['Minecraft', 'Roblox', 'VRchat'], "througput_cdf_regular_pc.pdf")

