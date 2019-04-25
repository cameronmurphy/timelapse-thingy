from datetime import datetime
import ffmpeg
import util


# Finds the filename of a file modified most recently before timestamp
def _resolve_file_most_recently_modified(path, timestamp):
    file_paths = util.get_file_paths_sort_filename_asc(path)

    file_count = len(file_paths)
    file_index_cursor = 0
    timestamp_cursor = datetime.fromtimestamp(0)

    while timestamp_cursor < timestamp and file_index_cursor < file_count:
        file_path = file_paths[file_index_cursor]
        timestamp_cursor = util.get_file_modified_timestamp(file_path)
        file_index_cursor += 1

    return file_paths[file_index_cursor - 1]


def resolve_frame_from_videos(path, timestamp):
    video_file = _resolve_file_most_recently_modified(path, timestamp)
    print(ffmpeg.probe(video_file))
