#!/usr/bin/env python3

import argparse
import os
import subprocess
from dotenv import load_dotenv
from glob import glob

from util import timelapse, string


def main():
    args = _parse_args()
    load_dotenv()

    montage_args = eval(os.getenv('MONTAGE_ARGS'))
    montage_source_order_dict = eval(os.getenv('MONTAGE_SOURCE_ORDER_DICT'))

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    frame_count, source_count = timelapse.resolve_frame_count_and_source_count(args.input_dir)
    processes = []

    for frame_index in range(1, frame_count + 1):
        sources = [''] * source_count

        frame_index_padded = string.zero_pad(frame_index, int(os.getenv('FRAME_INDEX_DIGITS')))
        files_glob = os.path.join(args.input_dir, '{}_*'.format(frame_index_padded))
        file_paths = glob(files_glob)

        for file_path in file_paths:
            frame_index, source_index = timelapse.parse_frame_index_and_source_index(os.path.basename(file_path))
            sources[montage_source_order_dict[source_index] - 1] = file_path

        print('Building frame ' + str(frame_index))

        output_filename = '{}.{}'.format(frame_index_padded, os.getenv('OUTPUT_FORMAT'))
        output_path = os.path.join(args.output_dir, output_filename)
        command = ['montage'] + sources + montage_args + [output_path]

        process = subprocess.Popen(command)
        processes.append(process)

    for process in processes:
        process.wait()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--input-dir', required=True, help='Directory containing the timelapse images')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory from processing')

    return parser.parse_args()


if __name__ == '__main__':
    main()
