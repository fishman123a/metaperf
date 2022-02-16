import os
import pandas as pd

class ProcProcessor:
    def __init__(self,
                 parser,
                 input_path,
                 output_dir):
        self.parser = parser
        self.input_path = input_path
        self.output_dir = output_dir

    def get_cpu(self, cover=False):
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
        out_path = os.path.join(self.output_dir, 'cpu.csv')
        if not cover and os.path.isfile(out_path):
            return pd.read_csv(out_path)
        df = self.parser.parse_cpu(os.path.join(self.input_path, 'cpu'))
        df.to_csv(out_path)
        return df

    def get_ram(self, cover=False):
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
        out_path = os.path.join(self.output_dir, 'ram.csv')
        if not cover and os.path.isfile(out_path):
            return pd.read_csv(out_path)
        df = self.parser.parse_ram(os.path.join(self.input_path, 'mem'))
        df.to_csv(out_path)
        return df

    def get_gpu(self, cover=False):
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
        out_path = os.path.join(self.output_dir, 'gpu.csv')
        if not cover and os.path.isfile(out_path):
            return pd.read_csv(out_path)
        df = self.parser.parse_gpu(os.path.join(self.input_path, 'gpu'))
        df.to_csv(out_path)
        return df

    def get_all(self, cover=False):
        self.get_ram(cover)
        self.get_cpu(cover)
        try:
            self.get_gpu(cover)
        except RuntimeError:
            pass
        except  FileNotFoundError:
            pass
