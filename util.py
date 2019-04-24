import glob
import os


def get_files_sort_filename_asc(path):
    path_joined = os.path.join(path, '*')
    files = glob.glob(path_joined)
    files.sort(key=os.path.basename)
    return files


def date_diff_seconds(date_one, date_two):
    return abs(date_one - date_two).seconds
