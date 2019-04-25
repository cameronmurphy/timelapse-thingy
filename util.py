from datetime import datetime
import glob
import os


def get_file_paths_sort_filename_asc(path):
    path_joined = os.path.join(path, '*')
    files = glob.glob(path_joined)
    files.sort(key=os.path.basename)
    return files


def get_file_modified_timestamp(path):
    file_created_epoch = os.path.getmtime(path)
    return datetime.fromtimestamp(file_created_epoch)


def date_diff_seconds(date_one, date_two):
    return abs(date_one - date_two).seconds
