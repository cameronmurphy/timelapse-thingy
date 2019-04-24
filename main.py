#!/usr/bin/env python3

from datetime import timedelta
import argparse
import image
import util

# Round to the nearest x seconds
INTERVAL_ROUND_TO = 10


def main():
    args = parse_args()

    master_file_paths = util.get_files_sort_filename_asc(args.master_dir)
    start_timestamp, interval_seconds = resolve_start_timestamp_and_interval_seconds(master_file_paths)

    process(master_file_paths, start_timestamp, interval_seconds)


def process(master_files, start_timestamp, interval):
    frame_cursor = 1
    master_file_count = len(master_files)
    master_file_cursor = 0
    timestamp_cursor = start_timestamp

    while master_file_cursor < master_file_count:
        current_image = image.open_image(master_files[master_file_cursor])
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

        # Resolve and dig into corresponding video files to grab accompanying frames
        # If video frames are unavailable for a given time, repeat most recent images

        current_image.close()

        frame_cursor += 1
        master_file_cursor += 1
        timestamp_cursor += timedelta(seconds=interval)


# The first two images set the stage for the intervals this timelapse will be dealing with.
# This method diffs the duration in seconds between the first two photos and rounds to INTERVAL_ROUND_TO
def resolve_start_timestamp_and_interval_seconds(master_file_paths):
    first_image_path, second_image_path = master_file_paths[:2]

    first_image = image.open_image(first_image_path)
    second_image = image.open_image(second_image_path)

    first_datetime = image.get_timestamp(first_image)
    second_datetime = image.get_timestamp(second_image)

    diff_seconds = util.date_diff_seconds(first_datetime, second_datetime)

    first_image.close()
    second_image.close()

    return first_datetime, INTERVAL_ROUND_TO * round(diff_seconds/INTERVAL_ROUND_TO)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--master-dir', required=True, help='Directory containing the master timelapse images')
    parser.add_argument('-o', '--output-dir', default='output', help='Output directory from processing')
    parser.add_argument('-s', '--slave-dirs', required=True, nargs='+',
                        help='The directories containing slave video content')

    return parser.parse_args()


if __name__ == '__main__':
    main()
