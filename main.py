#!/usr/bin/env python3

from datetime import timedelta
from shutil import copyfile
import argparse
import image
import os
import util


INTERVAL_ROUND_TO = 10
FRAME_INDEX_DIGITS = 7
SOURCE_INDEX_DIGITS = 2
OUTPUT_FORMAT = 'JPG'


def main():
    args = _parse_args()

    master_file_paths = util.get_files_sort_filename_asc(args.master_dir)
    start_timestamp, interval_seconds = _resolve_start_timestamp_and_interval_seconds(master_file_paths)

    _process(master_file_paths, start_timestamp, interval_seconds, args.output_dir)


def _process(master_files, start_timestamp, interval, output_dir):
    frame_cursor = 1
    master_file_count = len(master_files)
    master_file_cursor = 0
    timestamp_cursor = start_timestamp

    while master_file_cursor < master_file_count:
        with image.open_image(master_files[master_file_cursor]) as current_image:
            current_image_timestamp = image.get_timestamp(current_image)

            if master_file_cursor > 0:
                offset = util.date_diff_seconds(timestamp_cursor, current_image_timestamp)

                # Tolerance of interval - 1 means, for a timelapse where photos are taken every 30 seconds,
                # if there's a gap in the timelapse, we will pick up the next available image when we've skipped enough
                # frames to be within 29 seconds either side of our expectations.
                if offset > interval - 1:
                    # Repeat the previous image while we're within a gap
                    master_file_cursor -= 1
                else:
                    # Align with the new timestamp
                    timestamp_cursor = current_image_timestamp

        _copy(frame_cursor, 1, master_files[master_file_cursor], output_dir)

        # Resolve and dig into corresponding video files to grab accompanying frames
        # If video frames are unavailable for a given time, repeat most recent images

        frame_cursor += 1
        master_file_cursor += 1
        timestamp_cursor += timedelta(seconds=interval)


def _save(image_bytes, frame_index, source_index, src_filename, output_dir):
    output_filename = _build_filename(frame_index, source_index, src_filename)
    output_path = os.path.join(output_dir, output_filename)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    with open(output_path, 'w+b') as output_file:
        output_file.write(image_bytes)


def _copy(frame_index, source_index, src_path, output_dir):
    output_filename = _build_filename(frame_index, source_index, os.path.basename(src_path))
    output_path = os.path.join(output_dir, output_filename)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    copyfile(src_path, output_path)


def _build_filename(frame_index, source_index, filename):
    frame_index_padded = str(frame_index).rjust(FRAME_INDEX_DIGITS, '0')
    source_index_padded = str(source_index).rjust(SOURCE_INDEX_DIGITS, '0')
    filename_without_extension = os.path.splitext(filename)[0]

    return '_'.join((
        frame_index_padded,
        source_index_padded,
        filename_without_extension,
    )) + '.' + OUTPUT_FORMAT


# The first two images set the stage for the intervals this timelapse will be dealing with.
# This method diffs the duration in seconds between the first two photos and rounds to INTERVAL_ROUND_TO
def _resolve_start_timestamp_and_interval_seconds(master_file_paths):
    first_image_path, second_image_path = master_file_paths[:2]

    first_image = image.open_image(first_image_path)
    second_image = image.open_image(second_image_path)

    first_datetime = image.get_timestamp(first_image)
    second_datetime = image.get_timestamp(second_image)

    diff_seconds = util.date_diff_seconds(first_datetime, second_datetime)

    first_image.close()
    second_image.close()

    return first_datetime, INTERVAL_ROUND_TO * round(diff_seconds/INTERVAL_ROUND_TO)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--master-dir', required=True, help='Directory containing the master timelapse images')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory from processing')
    parser.add_argument('-s', '--slave-dirs', required=True, nargs='+',
                        help='The directories containing slave video content')

    return parser.parse_args()


if __name__ == '__main__':
    main()
