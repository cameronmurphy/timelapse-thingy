#!/usr/bin/env python3

import argparse
from glob import glob
import os

import config
from util import image, map, timelapse, string


def main():
    args = _parse_args()
    config.load()

    frame_count, source_count = timelapse.resolve_frame_count_and_source_count(args.working_dir)
    input_source_index_padded = string.zero_pad(args.input_source_index, config.source_index_digits)
    output_source_index_padded = string.zero_pad(args.output_source_index, config.source_index_digits)

    if args.input_source_index > source_count:
        raise RuntimeError('Invalid input source index {}'.format(args.input_source_index))

    for frame_index in range(1, frame_count + 1):
        frame_index_padded = string.zero_pad(frame_index, config.frame_index_digits)

        files_glob = os.path.join(args.working_dir, '{}_{}_*'.format(frame_index_padded, input_source_index_padded))
        file_paths = glob(files_glob)

        if len(file_paths) != 1:
            raise RuntimeError(
                'Source image missing for frame {} source {}'.format(frame_index_padded, input_source_index_padded)
            )

        with image.open_image(file_paths[0]) as current_image:
            current_lat, current_long = image.get_gps_coords(current_image)
            output_filename = '{}_{}_MAP.{}'.format(frame_index_padded, output_source_index_padded, config.map_format)
            output_path = os.path.join(args.working_dir, output_filename)

            print('Composing map frame ' + frame_index_padded)
            
            map.build(current_lat, current_long, output_path)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--working-dir', required=True, help='The directory containing the source images')
    parser.add_argument('-i', '--input-source-index', default=1, help='Source index for images containing GPS data')
    parser.add_argument('-o', '--output-source-index', default=4, help='Source index for output map frames')

    return parser.parse_args()


if __name__ == '__main__':
    main()
