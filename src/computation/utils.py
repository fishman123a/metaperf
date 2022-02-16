import shutil
import subprocess
from enum import Enum
import os

from src.network.utils import PROJECT_ROOT


class SupportedPlatform(Enum):
    Windows = 0,
    Android = 1

def file_len(fname):
    with open(fname, encoding='ANSI') as f:
        return len(f.readlines())

def fix_codec(dirs, cover=False):
    for d in dirs:
        for root, subdirs, _ in os.walk(d):
            for s in subdirs:
                if s == 'cpu':
                    fix_dir = os.path.join(root, s)
                    output_dir = os.path.join(fix_dir, 'fixed')
                    if not os.path.isdir(output_dir):
                        os.makedirs(output_dir)
                    for file in os.listdir(fix_dir):
                        file_path = os.path.join(fix_dir, file)
                        if os.path.isdir(file_path):
                            continue
                        output_path = os.path.join(fix_dir, 'fixed', file)
                        print(output_path)
                        subprocess.run(["powershell", "-Command",' Get-Content %s | Set-Content -Encoding oem %s' % (file_path, output_path)])
                        os.remove(file_path)
                    for file in os.listdir(output_dir):
                        shutil.copy(os.path.join(output_dir, file), os.path.join(fix_dir, file))
                    for file in os.listdir(output_dir):
                        os.remove(os.path.join(output_dir, file),)
                    os.rmdir(os.path.join(fix_dir, 'fixed'))
if __name__ == '__main__':
    pc_traces = ['mc','roblox','vrchat']
    paths = [os.path.join(PROJECT_ROOT, 'trace', pt) for pt in pc_traces]
    fix_codec(paths)