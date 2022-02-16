import json
import os

from src.computation.proc_parser import parser_factory
from src.computation.proc_processor import ProcProcessor
from src.network.utils import PROJECT_ROOT

if __name__ == '__main__':
    trace_attr = json.load(open('../trace/trace_attributes.json'))

    for attr in trace_attr['trace_attrs']:

        src_dir = os.path.abspath(os.path.join(PROJECT_ROOT, 'trace', attr['input_path']))
        output_dir = os.path.join(PROJECT_ROOT, 'data', attr['input_path'], 'computation')
        ProcProcessor(parser_factory(attr['platform']),
                      src_dir,
                      output_dir).get_all(cover=False)

