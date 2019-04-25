from datetime import datetime
import glob
import os
import re


def get_file_paths_sort_filename_asc(path):
    path_joined = os.path.join(path, '*')
    files = glob.glob(path_joined)
    files.sort(key=os.path.basename)
    return files


# Finds the file with the most proximate timestamp (without surpassing max_timestamp) embedded in the filename
def resolve_latest_file_by_filename_timestamp(path, max_timestamp, date_regex, date_format):
    file_paths = get_file_paths_sort_filename_asc(path)
    latest_file_path = None

    for file_path in file_paths:
        filename_timestamp = parse_date_from_filename(file_path, date_regex, date_format)

        if filename_timestamp < max_timestamp:
            latest_file_path = file_path
        else:
            break

    return latest_file_path


def parse_date_from_filename(path, date_regex, date_format):
    filename_timestamp_match = re.match(date_regex, os.path.basename(path))

    if filename_timestamp_match is not None:
        return datetime.strptime(filename_timestamp_match.group(0), date_format)


def resolve_first_file_match(path, regex):
    file_paths = get_file_paths_sort_filename_asc(path)

    for file_path in file_paths:
        if re.match(regex, os.path.basename(file_path)):
            return file_path


def get_file_modified_timestamp(path):
    file_created_epoch = os.path.getmtime(path)
    return datetime.fromtimestamp(file_created_epoch)


def date_diff_seconds(date_one, date_two):
    return abs(date_one - date_two).seconds
