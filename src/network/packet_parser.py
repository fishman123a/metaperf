import scapy.all as scapy
import pandas as pd
from enum import Enum
import numpy as np
import os.path
import matplotlib.pyplot as plt
from scapy.packet import Raw
from scapy.utils import hexdump
import ray

from src.network.utils import Role, SupportedProtocol


class AbstractNetParser:
    def __init__(self,
                 protocol):
        self.protocol = protocol

    def filter(self,
               raw_pkts,
               server_ip,
               server_port):

        filtered_pkts = [pkt for pkt in raw_pkts if self.protocol.name in pkt and
                         "IP" in pkt and (pkt['IP'].src == server_ip or pkt['IP'].dst == server_ip) and
                         (pkt[self.protocol.name].sport == server_port or pkt[self.protocol.name].dport == server_port)]
        return filtered_pkts

    def parse_general(self,
                      server_port,
                      filtered_pkts):
        raise NotImplementedError()

    def parse_sample_rtt(self,
                         df_general):
        raise NotImplementedError()

    def parse_throughput(self,
                         df_general,
                         interval):
        df = pd.DataFrame(columns=["time", "ingress", "egress"])
        time = interval
        ingress = 0
        egress = 0
        for _, row in df_general.iterrows():
            while time < row.time:
                df.loc[len(df.index)] = [time, ingress, egress]
                time += interval
                ingress = 0
                egress = 0
            if row.role == Role.CLIENT.value:
                ingress += row.len
            else:
                egress += row.len
        return df


class TCPParser(AbstractNetParser):
    def __init__(self):
        AbstractNetParser.__init__(self, SupportedProtocol.TCP)

    def parse_general(self,
                      server_port,
                      filtered_pkts):
        start_time = filtered_pkts[0].time if len(filtered_pkts) > 0 else 0.0
        start_seq = filtered_pkts[0]['TCP'].seq - 1 if len(filtered_pkts) > 0 else 0
        start_ack = filtered_pkts[0]['TCP'].ack - 1 if len(filtered_pkts) > 0 else 0
        start_side = Role.SERVER.value if filtered_pkts[0]['TCP'].sport == server_port else Role.CLIENT.value
        df_dat = []

        @ray.remote
        def get_packet_info(pkt, time):
            try:
                tsdata = dict(pkt.options)
                if isinstance(pkt.payload, scapy.packet.Raw):
                    plen = len(pkt.payload)
                else:
                    plen = 0
                role = Role.SERVER.value if pkt.sport == server_port else Role.CLIENT.value
                res = [float(time - start_time), time,
                       pkt.seq - (start_seq if role == start_side else start_ack),
                       pkt.ack - (start_seq if role != start_side else start_ack),
                       plen, tsdata['Timestamp'][0],
                       tsdata['Timestamp'][1],
                       pkt.payload, role]
                return res
            except KeyError:
                return None

        if len(filtered_pkts) > 100000:
            for p in filtered_pkts:
                df_dat.append(get_packet_info.remote(p['TCP'], p.time, ))
            df = pd.DataFrame(
                columns=["time", "abs-time", "seq", "ack", "len", "tsval", "tsecr", "payload", "role"],
                data=ray.get(df_dat))

            # for d in df_dat:
            #     try:
            #         df.loc[len(df.index)] = ray.get(d)
            #     except TypeError:
            #         pass
            df.dropna(inplace=True)
        else:
            df = pd.DataFrame(
                columns=["time", "abs-time", "seq", "ack", "len", "tsval", "tsecr", "payload", "role"])
            for pkt in filtered_pkts:
                try:
                    tsdata = dict(pkt['TCP'].options)['Timestamp']
                except KeyError:
                    tsdata = [None, None]
                role = Role.SERVER.value if pkt['TCP'].sport == server_port else Role.CLIENT.value
                df.loc[len(df.index)] = [float(pkt.time - start_time), pkt.time,
                                         pkt['TCP'].seq - (start_seq if role == start_side else start_ack),
                                         pkt['TCP'].ack - (start_seq if role != start_side else start_ack),
                                         len(pkt['TCP'].payload), tsdata[0], tsdata[1],
                                         pkt['TCP'].payload, role]

        return df

    def parse_sample_rtt(self, df_general):
        df = pd.DataFrame(columns=["time", "estimated_rtt", "sample_rtt"])
        for idx, row in df_general.iterrows():
            if row.role == Role.CLIENT.value and row.len > 0:
                origin_pkt = row
                for n_idx, n_row in df_general.iloc[idx + 1: idx + 201, :].iterrows():
                    # use tsval and tsecr
                    if not pd.isnull(n_row.tsecr) and not pd.isnull(origin_pkt.tsval):
                        if n_row.role == Role.SERVER.value and n_row.tsecr == origin_pkt.tsval:
                            df.loc[len(df.index)] = [n_row.time, 0, (n_row.time - origin_pkt.time) * 1000]
                            break
                    else:
                        # use ack and seq
                        if n_row.role == Role.SERVER.value and n_row.ack == origin_pkt.len + origin_pkt.seq:
                            df.loc[len(df.index)] = [n_row.time, 0, (n_row.time - origin_pkt.time) * 1000]
                            break

        return df


class UDPParser(AbstractNetParser):
    def __init__(self):
        AbstractNetParser.__init__(self, SupportedProtocol.UDP)

    def parse_general(self,
                      server_port,
                      filtered_pkts):
        df = pd.DataFrame(columns=["time", "abs-time", "src", "dst", "len", "role"])
        start_time = filtered_pkts[0].time if len(filtered_pkts) > 0 else 0
        for pkt in filtered_pkts:
            role = Role.SERVER.value if pkt['UDP'].sport == server_port else Role.CLIENT.value
            df.loc[len(df.index)] = [pkt.time - start_time, pkt.time, pkt['IP'].src, pkt['IP'].dst, len(pkt), role]
        return df

    def parse_sample_rtt(self,
                         df_general):
        raise RuntimeError("RTT fetching with UDP is not supported")


class RakNetParser(AbstractNetParser):
    def __init__(self):
        AbstractNetParser.__init__(self, SupportedProtocol.RakNet)
        self.encrypted = True

    def filter(self,
               raw_pkts,
               server_ip,
               server_port):
        filtered_pkts = [pkt for pkt in raw_pkts if
                         "IP" in pkt and (pkt['IP'].src == server_ip or pkt['IP'].dst == server_ip) and
                         'UDP' in pkt and
                         (pkt['UDP'].sport == server_port or pkt['UDP'].dport == server_port)]
        return filtered_pkts

    def parse_general(self,
                      server_port,
                      filtered_pkts):
        start_time = filtered_pkts[0].time if len(filtered_pkts) > 0 else 0
        if self.encrypted:
            df = pd.DataFrame(columns=["time", "abs-time", "src", "dst", "len", "role"])
        else:
            df = pd.DataFrame(columns=["time", "abs-time", "src", "dst", "len", "role", "seq", "ack"])
        for pkt in filtered_pkts:
            role = Role.SERVER.value if pkt['UDP'].sport == server_port else Role.CLIENT.value
            if self.encrypted:
                df.loc[len(df.index)] = [pkt.time - start_time, pkt.time, pkt['IP'].src, pkt['IP'].dst, len(pkt), role]
            else:
                raise NotImplementedError('Unencrypted RakNet Parser is still under testification.')
        return df

    def parse_sample_rtt(self,
                         df_general):
        raise NotImplementedError('Unencrypted RakNet Parser is still under testification.')
        # df = pd.DataFrame(columns=["time", "sample_rtt", "is_pingpong"])
        # pkt_server_idx = 0
        # pkt_client_idx = 0
        # for _, pkt in df_general.iterrows():
        #     if pkt.role == Role.SERVER.value:
        #         if pkt.ack != '-1':
        #             max_ack = 0
        #             ack_arr = [record.split() for record in pkt.ack.split("#")]
        #             for ack_range in ack_arr:
        #                 ack = int(ack_range[0])
        #                 if len(ack_range) == 2:
        #                     ack = int(ack_range[1])
        #                 if ack > max_ack:
        #                     max_ack = ack
        #             source_pkt_time = -1.0
        #             source_pkts = df_general[
        #                 (df_general.role == Role.CLIENT.value) & (df_general.seq != '-1')].reset_index(
        #                 drop=True)
        #             pkt_count = source_pkts.shape[0]
        #             while pkt_server_idx < pkt_count:
        #                 if source_pkts.at[pkt_server_idx, 'seq'] == max_ack:
        #                     source_pkt_time = source_pkts.at[pkt_server_idx, 'time']
        #                     pkt_server_idx += 1
        #                     break
        #                 pkt_server_idx += 1
        #             if source_pkt_time > 0:
        #                 df.loc[len(df.index)] = [pkt.time, 1000 * (pkt.time - source_pkt_time), 0]
        #     else:
        #         if pkt.ack != '-1':
        #             max_ack = 0
        #             ack_arr = [record.split() for record in pkt.ack.split("#")]
        #             for ack_range in ack_arr:
        #                 ack = int(ack_range[0])
        #                 if len(ack_range) == 2:
        #                     ack = int(ack_range[1])
        #                 if ack > max_ack:
        #                     max_ack = ack
        #             source_pkt_time = -1.0
        #             source_pkts = df_general[
        #                 (df_general.role == Role.SERVER.value) & (df_general.seq != '-1')].reset_index(
        #                 drop=True)
        #             pkt_count = source_pkts.shape[0]
        #             while pkt_client_idx < pkt_count:
        #                 if source_pkts.at[pkt_client_idx, 'seq'] > max_ack:
        #                     source_pkt_time = source_pkts.at[pkt_client_idx, 'time']
        #                     pkt_client_idx += 1
        #                     break
        #                 pkt_client_idx += 1
        #             if source_pkt_time > 0:
        #                 df.loc[len(df.index)] = [pkt.time, 1000 * (source_pkt_time - pkt.time), 1]
        # return df


TCPParserSingleton = TCPParser()
UDPParserSingleton = UDPParser()
RakNetParserSingleton = RakNetParser()


def parser_factory(protocol):
    if protocol.lower() == SupportedProtocol.TCP.name.lower():
        return TCPParserSingleton
    if protocol.lower() == SupportedProtocol.UDP.name.lower():
        return UDPParserSingleton
    if protocol.lower() == SupportedProtocol.RakNet.name.lower():
        return RakNetParserSingleton
    raise ModuleNotFoundError('Unsupported protocol \"%s\" detected.' % protocol)
