import glob
import json
import os

import ray

from src.network.packet_parser import parser_factory
from src.network.packet_processor import PacketProcessor, integrate_throughput
from src.network.utils import PROJECT_ROOT


def gen_data(server_ip,
             server_port,
             parser,
             input_path,
             output_dir,
             annot,
             cover=False):
    pp = PacketProcessor(server_ip,
                         server_port,
                         parser,
                         input_path,
                         output_dir,
                         annot)
    pp.get_filtered_data(cover=False)
    try:
        pp.get_rtt(cover=cover)
    except RuntimeError:
        pass
    pp.get_throughput(cover=cover)


def gen_input_list():
    pathname = os.path.join(PROJECT_ROOT, 'trace\**\cap.pcapng')
    return glob.glob(pathname, recursive=True)


if __name__ == '__main__':
    # ray.init()
    network_attr = json.load(open('../trace/trace_attributes.json'))
    for attr in network_attr['trace_attrs']:

        src_file = os.path.abspath(os.path.join(PROJECT_ROOT, 'trace', attr['input_path'], 'network\\cap.pcapng'))
        output_dir = os.path.dirname(os.path.join(PROJECT_ROOT, 'data', attr['input_path'], 'network\\cap.pcapng'))
        server_ips = attr['server-ip'].split(',')
        for ip in server_ips:
            gen_data(ip,
                     attr['server-port'],
                     parser_factory(attr['protocol']),
                     src_file,
                     output_dir,
                     annot='_' + '-'.join(ip.split('.')))
        data_dir = os.path.join(PROJECT_ROOT, 'data', os.path.join(attr['input_path'], 'network'))
        trace_dir = os.path.join(PROJECT_ROOT, 'trace', os.path.join(attr['input_path'], 'network'))
        integrate_throughput(data_dir, trace_dir, cover=False)
        integrate_throughput(data_dir, trace_dir, cover=False, flow='ingress', output='concat_ingress.csv')
        print("[%s] finished" % src_file)