#!/usr/bin/env python3

import argparse
import os
import subprocess
from glob import glob

import config
from util import timelapse, string


def main():
    args = _parse_args()
    config.load()

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    frame_count, source_count = timelapse.resolve_frame_count_and_source_count(args.input_dir)
    processes = []

    for frame_index in range(1, frame_count + 1):
        sources = [''] * source_count

        frame_index_padded = string.zero_pad(frame_index, config.frame_index_digits)
        files_glob = os.path.join(args.input_dir, '{}_*'.format(frame_index_padded))
        file_paths = glob(files_glob)

        for file_path in file_paths:
            frame_index, source_index = timelapse.parse_frame_index_and_source_index(os.path.basename(file_path))
            sources[config.montage_source_order_dict[source_index] - 1] = file_path

        print('Composing frame ' + frame_index_padded)

        output_filename = '{}.{}'.format(frame_index_padded, config.output_format)
        output_path = os.path.join(args.output_dir, output_filename)
        command = ['montage'] + sources + config.montage_arg_list + [output_path]

        process = subprocess.Popen(command)
        processes.append(process)

    for process in processes:
        process.wait()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--input-dir', required=True, help='Directory containing source images')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory from composed frames')

    return parser.parse_args()


if __name__ == '__main__':
    main()
