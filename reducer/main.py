# !/usr/bin/python

import sys
from reduction import reduce

COLS = {
    'ts': 0,
    'src': 1,
    'src_name': 2,
    'type': 3,
    'dst': 4
}

if __name__ == '__main__':
    forward_file_path = sys.argv[1]
    backward_file_path = sys.argv[2]
    out_dir = sys.argv[3]
    
    reduce(forward_file_path, backward_file_path, out_dir)
