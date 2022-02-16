import os

import matplotlib.pyplot as plt
import pandas as pd

from src.network.utils import PROJECT_ROOT

FIG_ROOT = os.path.join(PROJECT_ROOT, 'figs')
def setup_plt():
    fs = (16, 9,)
    dpi = 300
    plt.rcParams['figure.figsize'] = [16, 9]
    plt.rcParams['figure.dpi'] = dpi
    plt.rcParams['pdf.fonttype'] = 42

from collections import OrderedDict

linestyles = OrderedDict(
    [('solid',               (0, ())),
     # ('loosely dotted',      (0, (1, 10))),
     # ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     # ('loosely dashed',      (0, (5, 10))),
     # ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     # ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     # ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     # ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     # ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])

def load_data(game_list):
    res = dict()
    for data_dir in game_list:
        res[data_dir] = dict()
        root_dir = os.path.join(PROJECT_ROOT, 'data', data_dir)
        for scenario in os.listdir(root_dir):
            sc_dir = os.path.join(root_dir, scenario)
            if os.listdir(sc_dir)[0][0].isdigit():
                for s_num in os.listdir(sc_dir):
                    sc_num_dir = os.path.join(sc_dir, s_num)
                    identifier = scenario + '-' + s_num
                    res[data_dir][identifier] = dict()
                    network_dir = os.path.join(sc_num_dir, 'network')
                    computation_dir = os.path.join(sc_num_dir, 'computation')
                    res[data_dir][identifier]['throughput'] = pd.read_csv(
                        os.path.join(network_dir, 'throughput', 'concat.csv'), index_col=0)
                    res[data_dir][identifier]['cpu'] = pd.read_csv(os.path.join(computation_dir, 'cpu.csv'))
                    res[data_dir][identifier]['ram'] = pd.read_csv(os.path.join(computation_dir, 'ram.csv'))
                    if os.path.isfile(os.path.join(computation_dir, 'gpu.csv')):
                        res[data_dir][identifier]['ram'] = pd.read_csv(os.path.join(computation_dir, 'gpu.csv'))
            else:
                res[data_dir][scenario] = dict()
                network_dir = os.path.join(sc_dir, 'network')
                computation_dir = os.path.join(sc_dir, 'computation')
                res[data_dir][scenario]['throughput'] = pd.read_csv(
                    os.path.join(network_dir, 'throughput', 'concat.csv'), index_col=0)
                res[data_dir][scenario]['cpu'] = pd.read_csv(os.path.join(computation_dir, 'cpu.csv'))
                res[data_dir][scenario]['ram'] = pd.read_csv(os.path.join(computation_dir, 'ram.csv'))
                if os.path.isfile(os.path.join(computation_dir, 'gpu.csv')):
                    res[data_dir][scenario]['ram'] = pd.read_csv(os.path.join(computation_dir, 'gpu.csv'))
    return res