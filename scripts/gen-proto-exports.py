import sys
import os


def get_target_from_filepath(filepath: str) -> str:
    basename = os.path.basename(filepath)
    without_ext = os.path.splitext(basename)
    return without_ext[0]


if __name__ == '__main__':
    with open('protogen/__init__.py', 'w') as f:
        for arg in sys.argv[1:]:
            target = get_target_from_filepath(arg) # target is name of protobuf file without the .proto
            code_target = target[0].upper()
            f.write(f'from .{target}_pb2_grpc import *\n')
            f.write(f'from .{target}_pb2 import *\n')

