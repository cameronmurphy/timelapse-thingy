import os
import re

import constants
from util import fs


def parse_frame_index_and_source_index(filename):
    regex = '^(\\d{{{}}})_(\\d{{{}}})'.format(constants.FRAME_INDEX_DIGITS, constants.SOURCE_INDEX_DIGITS)
    match = re.match(regex, filename)

    if match is not None:
        return int(match.group(1)), int(match.group(2))


def resolve_frame_count_and_source_count(path):
    file_paths = fs.get_file_paths_sort_filename_asc(path)
    last_file_path = file_paths[-1]
    last_filename = os.path.basename(last_file_path)

    frame_index, source_index = parse_frame_index_and_source_index(last_filename)

    if frame_index is None:
        raise RuntimeError('File {} does not match expected format'.format(last_filename))

    return frame_index, source_index
