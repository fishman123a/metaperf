import os
from enum import Enum
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '../../../'))

class Role(Enum):
    SERVER = 0
    CLIENT = 1

class SupportedProtocol(Enum):
    TCP=0,
    UDP=1,
    RakNet=2

def throughput_integrate_by_protocol(df):
    df_concat = df.T.groupby([s.split('_')[0] for s in df.T.index.values]).sum().T
    df_concat = df_concat.groupby(df_concat.index // 10).sum()
    return df_concat