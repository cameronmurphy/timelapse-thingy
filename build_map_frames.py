#!/usr/bin/env python3

import argparse
from glob import glob
import os

import config
from util import map, timelapse, string


def main():
    args = _parse_args()
    config.load()

    frame_count, source_count = timelapse.resolve_frame_count_and_source_count(args.working_dir)

    if args.master_source_index > source_count:
        raise RuntimeError('Invalid master source index {}'.format(args.master_source_index))

    for frame_index in range(1, frame_count + 1):
        frame_index_padded = string.zero_pad(frame_index, config.frame_index_digits)
        master_source_index_padded = string.zero_pad(args.master_source_index, config.source_index_digits)

        files_glob = os.path.join(args.working_dir, '{}_{}_*'.format(frame_index_padded, master_source_index_padded))
        file_paths = glob(files_glob)

        if len(file_paths) != 1:
            raise RuntimeError(
                'Source image missing for frame {} source {}'.format(frame_index_padded, master_source_index_padded)
            )

        map.build({})


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--working-dir', required=True, help='The directory containing the source images')
    parser.add_argument('-m', '--master-source-index', default=1, help='Source index for images containing GPS data')

    return parser.parse_args()


if __name__ == '__main__':
    main()
