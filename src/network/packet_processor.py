import scapy.all as scapy
import pandas as pd
from enum import Enum
import numpy as np
import os.path
import matplotlib.pyplot as plt
from scapy.packet import Raw
from scapy.utils import hexdump

from src.network.packet_parser import TCPParser, TCPParserSingleton
from src.network.utils import PROJECT_ROOT


class PacketProcessor:
    def __init__(self, server_ip, server_port,
                 # client_ip, client_port,
                 parser,
                 input_path,
                 output_dir,
                 annot=''):
        self.server_ip = server_ip
        self.server_port = server_port
        # self.client_ip = client_ip
        # self.client_port = client_port
        self.parser = parser
        self.input_path = input_path
        self.output_dir = output_dir
        self.annot = annot
        self.filtered_data = self.get_filtered_data()

    def get_filtered_trace(self, cover=False):
        out_dir = os.path.join(self.output_dir, 'filtered_caps')
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, self.parser.protocol.name + self.annot + '.pcap')
        if not cover and os.path.isfile(out_path):
            return scapy.rdpcap(out_path)
        filtered_pkts = self.parser.filter(scapy.rdpcap(self.input_path),
                                                        self.server_ip,
                                                        self.server_port)
        scapy.wrpcap(out_path, filtered_pkts)
        return filtered_pkts

    def get_filtered_data(self, cover=False):
        out_dir = os.path.join(self.output_dir, 'filtered_csvs')
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, self.parser.protocol.name + self.annot + '.csv')
        if not cover and os.path.isfile(out_path):
            return pd.read_csv(out_path)
        filtered_pkts = self.get_filtered_trace()
        filtered_data = self.parser.parse_general(self.server_port, filtered_pkts)
        filtered_data.to_csv(out_path, index=False)
        return filtered_data

    def get_rtt(self, cover=False):
        out_dir = os.path.join(self.output_dir, 'rtt')
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, self.parser.protocol.name + self.annot + '.csv')
        if not cover and os.path.isfile(out_path):
            return pd.read_csv(out_path)
        filtered_data = self.filtered_data
        rtt = self.parser.parse_sample_rtt(filtered_data)
        rtt.to_csv(out_path, index=False)
        return rtt

    def get_throughput(self, interval=0.1, cover=False):
        out_dir = os.path.join(self.output_dir, 'throughput')
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_path = os.path.join(out_dir, self.parser.protocol.name + self.annot + '.csv')
        if not cover and os.path.isfile(out_path):
            return pd.read_csv(out_path)
        filtered_data = self.filtered_data
        throughput = self.parser.parse_throughput(filtered_data, interval)
        throughput.to_csv(out_path, index=False)
        return throughput


def integrate_throughput(data_dir, trace_dir, interval=0.1, cover=False, flow='egress', output='concat.csv'):

    time_file = os.path.join(data_dir, 'start_time.txt')
    if os.path.isfile(time_file) :
        with open(time_file, 'r') as f:
            trace_time_0 = float(f.readline())
    else:
        raw_pcap = scapy.rdpcap(os.path.join(trace_dir, 'cap.pcapng'))
        trace_time_0 = raw_pcap[0].time
        open( time_file, "w").write(str(trace_time_0))

    df = pd.DataFrame()

    if os.path.isfile(os.path.join(data_dir, 'throughput', output)) and not cover:
        return
    for filtered_csv in os.listdir(os.path.join(data_dir, 'filtered_csvs')):
        annot = filtered_csv.split('.')[0]
        print("new flow")
        flow_time_0 = float(pd.read_csv(os.path.join(data_dir, 'filtered_csvs',filtered_csv)).at[0, 'abs-time'])
        time_offset = round((flow_time_0-trace_time_0) / interval)
        print(time_offset)
        throughput = np.concatenate((
            np.zeros(time_offset),
            pd.read_csv(os.path.join(data_dir, 'throughput', filtered_csv))[flow].to_numpy()
        ))
        df = pd.concat([df, pd.DataFrame({annot: throughput})], axis=1)
        df.fillna(0, inplace=True)
        df.to_csv(os.path.join(data_dir, 'throughput', output))







if __name__ == '__main__':
    # pp = PacketProcessor('123.57.84.206',
    #                      25565,
    #                      # '192.168.3.9',
    #                      # 51633,
    #                      TCPParserSingleton,
    #                      os.path.abspath(os.path.join(__file__, '../../../trace/mc/battle/network/cap.pcapng')),
    #                      os.path.abspath(os.path.join(__file__, '../../../data/mc/battle/network/'))
    #                      )
    # print(pp.get_throughput(cover=False).info())
    integrate_throughput('vrchat/connection/4/network')

