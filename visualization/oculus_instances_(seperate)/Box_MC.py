import matplotlib.pyplot as plt
import pandas as pd

mc_connect_no_entity = pd.read_csv("MC/connect_no_entity/network/rtt/TCP_123-57-84-206.csv")
mc_connect_no_entity = mc_connect_no_entity.loc[:,["sample_rtt"]]

mc_connect_entity = pd.read_csv("MC/connect_many_entity/network/rtt/TCP_123-57-84-206.csv")
mc_connect_entity = mc_connect_entity.loc[:, ["sample_rtt"]]

mc_stand_no_entity = pd.read_csv("MC/stand_still_no_entity/network/rtt/TCP_123-57-84-206.csv")
mc_stand_no_entity = mc_stand_no_entity.loc[:, ["sample_rtt"]]

mc_stand_entity = pd.read_csv("MC/stand_still_many_entity/network/rtt/TCP_123-57-84-206.csv")
mc_stand_entity = mc_stand_entity.loc[:, ["sample_rtt"]]

plt.figure(figsize=(16, 9))  # 设置画布的尺寸
plt.title('Minecraft Computation Burden with RTT', fontsize=40)  # 标题，并设定字号大小
labels = 'Connection', 'General'  # 图例

# vert=False:水平箱线图；showmeans=True：显示均值
plt.boxplot([mc_connect_no_entity["sample_rtt"],
             mc_stand_no_entity["sample_rtt"]],
            labels=labels, showmeans=True,
            positions=[0.6, 2.6],
            patch_artist = True, boxprops = {'color':'orangered','facecolor':'red'})

plt.boxplot([mc_connect_entity["sample_rtt"],
             mc_stand_entity["sample_rtt"]],
            labels=labels, showmeans=True,
            positions=[1.2, 3.2],
            patch_artist = True, boxprops = {'color':'orangered','facecolor':'blue'})

plt.xticks(fontsize=30)
plt.yticks(fontsize=25)

plt.ylabel("RTT(ms)", fontsize=40)
plt.show()