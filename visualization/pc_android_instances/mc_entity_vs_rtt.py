import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from src.network.utils import PROJECT_ROOT
import seaborn as sns

from visualization_tools.utils import FIG_ROOT


def parse_rtt(rtt, interval=0.3):
    time = interval
    rtt_sum = 0
    count = 0
    df = pd.DataFrame(columns=['time', 'rtt'])
    for _, row in rtt.iterrows():
        while time < row.time:
            res = np.NaN
            if count == 0:
                if len(df.index) > 0:
                    res = np.NaN  # df.at[len(df.index) - 1, 'rtt']
            else:
                res = rtt_sum / count
            df.loc[len(df.index)] = [time, res]
            time += interval
            rtt_sum = 0
            count = 0
        rtt_sum += row.sample_rtt
        count += 1
    return df


df = pd.DataFrame(columns=['rtt', 'entity', 'stage'])

mc_connect_no_entity = np.concatenate([
    parse_rtt(pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/mc/connect_no_entity/%d/network/rtt/TCP_123-57-84-206.csv" % i))).dropna()[
        'rtt'].to_numpy()
    for i in range(1, 6)]
)
for i in mc_connect_no_entity:
    df.loc[len(df.index)] = [i, 'No Entity', 'Avatar Creation']

mc_connect_entity = np.concatenate([
    parse_rtt(pd.read_csv(
        os.path.join(PROJECT_ROOT, "data/mc/connect_many_entity/%d/network/rtt/TCP_123-57-84-206.csv" % i))).dropna()[
        'rtt'].to_numpy()
    for i in range(1, 6)]
)
for i in mc_connect_entity:
    df.loc[len(df.index)] = [i, 'With Entities', 'Avatar Creation']

mc_stand_no_entity = parse_rtt(pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/mc/stand_still_long_no_entity/network/rtt/TCP_123-57-84-206.csv"))).dropna()[
    'rtt'].to_numpy()
for i in mc_stand_no_entity:
    df.loc[len(df.index)] = [i, 'No Entity', 'Regular Gameplay']

mc_stand_entity = parse_rtt(pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/mc/stand_still_long_many_entity/network/rtt/TCP_123-57-84-206.csv"))).dropna()[
    'rtt'].to_numpy()
for i in mc_stand_entity:
    df.loc[len(df.index)] = [i, 'With Entities', 'Regular Gameplay']

mc_interaction_no_entity = parse_rtt(pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/mc/interaction_no_entity/network/rtt/TCP_123-57-84-206.csv"))).dropna()[
    'rtt'].to_numpy()
for i in mc_stand_no_entity:
    df.loc[len(df.index)] = [i, 'No Entity', 'Interaction']

mc_interaction_entity = parse_rtt(pd.read_csv(
    os.path.join(PROJECT_ROOT, "data/mc/interaction_many_entity/network/rtt/TCP_123-57-84-206.csv"))).dropna()[
    'rtt'].to_numpy()
for i in mc_stand_entity:
    df.loc[len(df.index)] = [i, 'With Entities', 'Interaction']

fig, ax = plt.subplots(figsize=(16, 9), dpi=300)

data_a = [mc_connect_no_entity, mc_stand_no_entity] #, mc_interaction_no_entity]
data_b = [mc_connect_entity, mc_stand_entity] #, mc_interaction_entity]
for a, b in zip (data_a, data_b):
    print(a.mean(), b.mean())

ticks = ['Avatar\nCreation', 'Regular\nGamePlay'] #, 'Interaction']


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


bpl = plt.boxplot(data_a, positions=np.array(range(len(data_a))) * 2.0 - 0.3, sym='', widths=0.5, showfliers=True, showmeans=True,
                  whiskerprops=dict(linestyle='--', linewidth=2),
                  boxprops=dict(linestyle='--', linewidth=2),
                  capprops=dict(linestyle='--', linewidth=2),
                  medianprops=dict(linestyle='--', linewidth=2), )
bpr = plt.boxplot(data_b, positions=np.array(range(len(data_b))) * 2.0 + 0.3, sym='', widths=0.5, showfliers=True,showmeans=True,
                  whiskerprops=dict(linestyle='-', linewidth=2),
                  boxprops=dict(linestyle='-', linewidth=2),
                  capprops=dict(linestyle='-', linewidth=2),
                  medianprops=dict(linestyle='-', linewidth=2),
                  )

# set_box_color(bpl, '#D7191C')  # colors are from http://colorbrewer2.org/
# set_box_color(bpr, '#2C7BB6')

# draw temporary red and blue lines and use them to create a legend
# plt.plot([], c='#D7191C', ls='--', label='Without Entity')
# plt.plot([], c='#2C7BB6', label='With Entities')
plt.plot([], c='black', ls='--', label='Without Entity')
plt.plot([], c='black', label='With Entities')
plt.legend(fontsize=40, edgecolor="white")

plt.xticks(range(0, len(ticks) * 2, 2), ticks, fontsize=50)
plt.xlim(-1, len(ticks) * 2 - 1)
plt.ylim(0, 8)

# plt.boxplot([mc_connect_no_entity,
#              mc_stand_no_entity],
#             showmeans=True,
#             positions=[0.6, 2.6])
#
# plt.boxplot([mc_connect_entity,
#              mc_stand_entity],
#             showmeans=True,
#             positions=[1.2, 3.2])

# ax = sns.boxplot(x=df['stage'], y=df['rtt'], hue=df['entity'], width=0.5, whiskerprops=dict(linestyle='-', linewidth=1.0
#                                                                                             , color='black'))
# handles, labels = ax.get_legend_handles_labels()
# ax.legend(handles=handles, labels=labels)

plt.ylim(55, 125)
plt.xticks(fontsize=50)
plt.yticks(fontsize=40)
plt.ylabel("RTT (ms)", fontsize=70)
plt.tight_layout()

plt.savefig(os.path.join(FIG_ROOT, "mc_entity_vs_rtt.pdf"))
