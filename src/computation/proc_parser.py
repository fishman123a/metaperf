import os
import pandas as pd
import regex as re
import numpy as np

from src.computation.utils import SupportedPlatform, file_len


class AbstractProcParser:
    def __init__(self):
        pass

    def parse_ram(self, trace_dir):
        raise NotImplementedError()

    def parse_cpu(self, trace_dir):
        raise NotImplementedError()

    def parse_gpu(self, trace_dir):
        raise NotImplementedError()


class AndroidProcParser(AbstractProcParser):
    def __init__(self):
        AbstractProcParser.__init__(self)
    def parse_ram(self, trace_dir):
        df = pd.DataFrame(columns=['total', 'free', 'occupied', 'ratio'])
        re_filter = re.compile(r'\d+')
        trace_count = max([int(re_filter.findall(filename)[0]) for filename in os.listdir(trace_dir)])
        trace_no = 1
        while trace_no <= trace_count:
            trace_file = os.path.join(trace_dir, 'mem_%d' % trace_no)
            if not os.path.isfile(trace_file) or os.path.getsize(trace_file) == 0:
                if trace_no > 1:
                    df = df.append(df.loc[len(df.index) - 1])
                else:
                    df.loc[len(df.index)] = [0, 0, 0, 0.0]
            else:
                with open(trace_file, 'r') as f:
                    mem_total = int(next(f).split()[1])
                    mem_free = int(next(f).split()[1])
                    mem_occupied = mem_total - mem_free
                    mem_ratio = mem_occupied / mem_total
                    df.loc[len(df.index)] = [mem_total, mem_free, mem_occupied, mem_ratio]
            trace_no += 1
        return df

    def parse_cpu(self, trace_dir):
        core_count = -1
        with open(os.path.join(trace_dir, os.listdir(trace_dir)[0]), 'r') as f:
            while True:
                line = f.readline()
                if line.startswith('intr'):
                    break
                core_count += 1

        df = pd.DataFrame(columns=['total'] + ['cpu%d' % x for x in range(core_count)])

        def extract_cpu_time(file):
            total_times = []
            idles = []
            with open(file, 'r') as f:
                for _ in range(core_count + 1):
                    cpu_info = list(map(int, f.readline().split()[1:8]))
                    idles.append(cpu_info[3])
                    total_times.append(sum(cpu_info))
            return np.array(total_times), np.array(idles)

        re_filter = re.compile(r'\d+')
        trace_count = min(
            max([int(re_filter.findall(filename)[0]) for filename in
                 [x for x in os.listdir(trace_dir) if x.startswith('cpu_s')]]),
            max([int(re_filter.findall(filename)[0]) for filename in
                 [x for x in os.listdir(trace_dir) if x.startswith('cpu_e')]]),
        )
        trace_no = 1
        while trace_no <= trace_count:
            trace_jif_start = os.path.join(trace_dir, 'cpu_s%d' % trace_no)
            trace_jif_end = os.path.join(trace_dir, 'cpu_e%d' % trace_no)
            if not os.path.isfile(trace_jif_start) or not os.path.isfile(trace_jif_end) or os.path.getsize(
                    trace_jif_start) == 0 or os.path.getsize(trace_jif_end) == 0:
                if trace_no > 1:
                    df = df.append(df.loc[len(df.index) - 1], ignore_index=True)
                else:
                    raise NotImplementedError("TODO: error file handling")
            else:
                total_time_start, idle_start = extract_cpu_time(trace_jif_start)
                total_time_end, idle_end = extract_cpu_time(trace_jif_end)
                cpu_usage = 1 - (idle_end - idle_start) / (total_time_end - total_time_start)
                df.loc[len(df.index)] = cpu_usage
            trace_no += 1

        return df

    def parse_gpu(self, trace_dir):
        raise RuntimeError("Android GPU measurement is under development!")


class WinProcParser(AbstractProcParser):
    def __init__(self):
        AbstractProcParser.__init__(self)
    def parse_ram(self, trace_dir):
        with open(os.path.join(trace_dir, 'mem_total'), 'r') as f:
            mem_total = int(int(f.readline()) / 1024)
        with open(os.path.join(trace_dir, 'mem_free'), 'r') as f:
            mem_free_list = [int(x) for x in [line.rstrip() for line in f]]
        df = pd.DataFrame(columns=['total', 'free', 'occupied', 'ratio'])
        for mf in mem_free_list:
            df.loc[len(df.index)] = [mem_total, mf, mem_total - mf, (mem_total - mf) / mem_total]
        return df

    def parse_cpu(self, trace_dir):
        core_count = file_len(os.path.join(trace_dir, os.listdir(trace_dir)[0])) - 1
        df = pd.DataFrame(columns=['total'] + ['cpu%d' % x for x in range(core_count)])
        re_filter = re.compile(r'\d+')
        trace_count = max([int(re_filter.findall(filename)[0]) for filename in
                           [x for x in os.listdir(trace_dir) if x.startswith('cpu_')]])
        trace_no = 1
        while trace_no <= trace_count:
            trace_file = os.path.join(trace_dir, 'cpu_%d' % trace_no)
            if not os.path.isfile(trace_file) or os.path.getsize(trace_file) == 0:
                if trace_no > 1:
                    df = df.append(df.loc[len(df.index) - 1], ignore_index=True)
                else:
                    raise NotImplementedError("TODO: first error file handling")
            else:
                with open(trace_file, 'r') as f:
                    data_dict = dict()
                    for line in f:
                        (core_no, core_ocp) = line.split(': ')
                        if core_no == '_Total':
                            core_no = 'total'
                        else:
                            core_no = 'cpu%s' % core_no
                        data_dict[str(core_no)] = int(core_ocp) / 100
                    df = df.append(data_dict, ignore_index=True)
            trace_no += 1
        return df

    def parse_gpu(self, trace_dir):
        trace_file = os.path.join(trace_dir, 'gpu_dat')
        df = pd.DataFrame(columns=['core_ocp', 'mem_ocp'])
        with open(trace_file, 'r') as f:
            for line in f:
                splited = line.split()
                df.loc[len(df.index)] = [int(splited[0]) / 100, int(splited[2]) / 100]
        return df


WinProcParserSingleton = WinProcParser()
AndroidProcParserSingleton = AndroidProcParser()


def parser_factory(platform):
    if platform.lower() == SupportedPlatform.Windows.name.lower():
        return WinProcParserSingleton
    if platform.lower() == SupportedPlatform.Android.name.lower():
        return AndroidProcParserSingleton
    raise ModuleNotFoundError('Unsupported platform \"%s\" detected.' % platform)
