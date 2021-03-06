#!/usr/bin/env python3

import argparse
import os
from datetime import timedelta
from glob import glob
from shutil import copyfile

import config
from util import date, fs, image, string, video


def main():
    args = _parse_args()
    config.load()

    master_file_paths = fs.get_file_paths_sort_filename_asc(args.master_dir)
    start_timestamp, interval_seconds = _resolve_start_timestamp_and_interval_seconds(master_file_paths)

    _process(
        master_file_paths,
        start_timestamp,
        interval_seconds,
        args.output_dir,
        args.slave_dirs,
        args.slave_filename_date_regex,
        args.slave_filename_date_format,
        args.slave_offsets)


def _process(
        master_file_paths,
        start_timestamp,
        interval,
        output_dir,
        slave_dirs,
        slave_filename_date_regex,
        slave_filename_date_format,
        slave_offsets):

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    frame_cursor = 1
    master_file_count = len(master_file_paths)
    master_file_cursor = 0
    timestamp_cursor = start_timestamp

    while master_file_cursor < master_file_count:
        _print_processing_heading(frame_cursor, 1)

        with image.open_image(master_file_paths[master_file_cursor]) as current_image:
            current_image_timestamp = image.get_timestamp(current_image)

            if master_file_cursor > 0:
                variance = date.date_diff_seconds(timestamp_cursor, current_image_timestamp)

                # Tolerance of interval - 1 means, for a timelapse where photos are taken every 30 seconds, if there's a
                # gap in the timelapse, we will pick up the next available image when we've skipped enough frames to be
                # within 29 seconds either side of our expectations.
                if variance > interval - 1:
                    # Repeat the previous image while we're within a gap
                    master_file_cursor -= 1
                    _print_fallback_message(master_file_paths[master_file_cursor])
                else:
                    # Align with the new timestamp
                    timestamp_cursor = current_image_timestamp

        _copy_file_to_output(frame_cursor, 1, master_file_paths[master_file_cursor], output_dir)
        _process_slaves(
            slave_dirs,
            slave_offsets,
            timestamp_cursor,
            frame_cursor,
            output_dir,
            slave_filename_date_regex,
            slave_filename_date_format)

        frame_cursor += 1
        master_file_cursor += 1
        timestamp_cursor += timedelta(seconds=interval)


def _process_slaves(
        slave_dirs,
        slave_offsets,
        timestamp,
        output_frame_index,
        output_dir,
        slave_filename_date_regex,
        slave_filename_date_format):

    for slave_index0, slave_dir in enumerate(slave_dirs):
        slave_timestamp = timestamp

        if len(slave_offsets) > slave_index0:
            slave_timestamp += timedelta(seconds=slave_offsets[slave_index0])

        _process_slave(
            slave_index0 + 1,
            slave_dir,
            slave_timestamp,
            output_frame_index,
            output_dir,
            slave_filename_date_regex,
            slave_filename_date_format)


def _process_slave(
        slave_index,
        slave_dir,
        timestamp,
        output_frame_index,
        output_dir,
        slave_filename_date_regex,
        slave_filename_date_format):
    _print_processing_heading(output_frame_index, slave_index + 1)

    image_bytes, source_filename, source_frame_index = video.resolve_frame_from_videos(
        slave_dir,
        timestamp,
        slave_filename_date_regex,
        slave_filename_date_format)

    if image_bytes is None:
        if output_frame_index == 1:
            raise RuntimeError('Cannot fall back on first frame of slave ' + slave_dir)

        _slave_fallback(output_frame_index, slave_index + 1, output_dir)
    else:
        _write_to_output(
            output_frame_index,
            slave_index + 1,
            image_bytes,
            source_filename,
            source_frame_index,
            output_dir)


# Go and find the most recent frame for a given slave, repeat for current frame
def _slave_fallback(output_frame_index, source_index, output_dir):
    source_index_padded = string.zero_pad(source_index, config.source_index_digits)
    output_frame_index_padded = string.zero_pad(output_frame_index, config.frame_index_digits)
    fallback_frame_index_padded = string.zero_pad(output_frame_index - 1, config.frame_index_digits)

    fallback_image_glob = '{}_{}_*'.format(fallback_frame_index_padded, source_index_padded)
    fallback_image_paths = glob(os.path.join(output_dir, fallback_image_glob))

    if len(fallback_image_paths) != 1:
        raise RuntimeError('Unable to fallback for frame {} source {}'.format(output_frame_index, source_index))

    fallback_frame_path = fallback_image_paths[0]
    _print_fallback_message(fallback_frame_path)
    output_filename = output_frame_index_padded + os.path.basename(fallback_frame_path)[config.frame_index_digits:]
    copyfile(fallback_frame_path, os.path.join(output_dir, output_filename))


def _write_to_output(frame_index, source_index, image_bytes, source_filename, source_frame_index, output_dir):
    output_filename = _build_output_filename(frame_index, source_index, source_filename, source_frame_index)
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w+b') as output_file:
        output_file.write(image_bytes)


def _copy_file_to_output(frame_index, source_index, source_path, output_dir):
    output_filename = _build_output_filename(frame_index, source_index, os.path.basename(source_path))
    output_path = os.path.join(output_dir, output_filename)

    copyfile(source_path, output_path)


def _build_output_filename(frame_index, source_index, filename, source_frame_index=None):
    frame_index_padded = string.zero_pad(frame_index, config.frame_index_digits)
    source_index_padded = string.zero_pad(source_index, config.source_index_digits)
    filename_without_extension = os.path.splitext(filename)[0]

    filename = '_'.join((
        frame_index_padded,
        source_index_padded,
        filename_without_extension,
    ))

    if source_frame_index is not None:
        filename = '_'.join([filename, str(source_frame_index)])

    return '{}.{}'.format(filename, config.output_format)


# The first two images set the stage for the intervals this timelapse will be dealing with.
# This method diffs the duration in seconds between the first two photos and rounds to INTERVAL_ROUND_TO
def _resolve_start_timestamp_and_interval_seconds(master_file_paths):
    first_image_path, second_image_path = master_file_paths[:2]

    first_image = image.open_image(first_image_path)
    second_image = image.open_image(second_image_path)

    first_datetime = image.get_timestamp(first_image)
    second_datetime = image.get_timestamp(second_image)

    diff_seconds = date.date_diff_seconds(first_datetime, second_datetime)

    first_image.close()
    second_image.close()

    return first_datetime, config.interval_round_to * round(diff_seconds/config.interval_round_to)


def _print_processing_heading(frame_index, source_index):
    print(
        '\n================================ Processing frame {} for source {} ================================'.format(
            string.zero_pad(frame_index, config.frame_index_digits),
            string.zero_pad(source_index, config.source_index_digits)
        )
    )


def _print_fallback_message(fallback_image_path):
    print('Falling back to ' + fallback_image_path)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--master-dir', required=True, help='Directory containing the master timelapse images')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory from processing')
    parser.add_argument('-s', '--slave-dirs', required=True, nargs='+',
                        help='The directories containing slave video content')
    parser.add_argument('-r', '--slave-filename-date-regex', default='^\\d{8}_\\d{6}',
                        help='Regex used to match the date portion of the slave video filenames')
    parser.add_argument('-f', '--slave-filename-date-format', default='%Y%m%d_%H%M%S',
                        help='The date format within the slave video filenames')
    parser.add_argument('-z', '--slave-offsets', type=int, nargs='+', default=[],
                        help='Account for slave videos being out of sync with master (in seconds) e.g. -158 -159')

    return parser.parse_args()


if __name__ == '__main__':
    main()
