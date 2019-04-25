import ffmpeg
import os
import util


def _get_first_video_stream(video_info):
    if 'streams' in video_info:
        for stream in video_info['streams']:
            if 'codec_type' in stream and stream['codec_type'] == 'video':
                return stream


def resolve_frame_from_videos(path, timestamp, filename_date_regex, filename_date_format):
    video_file_path = util.resolve_latest_file_by_filename_timestamp(
        path,
        timestamp,
        filename_date_regex,
        filename_date_format)
    video_timestamp = util.parse_date_from_filename(video_file_path, filename_date_regex, filename_date_format)

    if video_file_path is None:
        raise RuntimeError('No appropriate video file found in ' + path)

    video_info = ffmpeg.probe(video_file_path)
    video_stream = _get_first_video_stream(video_info)

    if video_stream is None:
        raise RuntimeError('No video stream found in ' + video_file_path)

    if 'avg_frame_rate' not in video_stream:
        raise RuntimeError('Video stream has no avg_frame_rate property in ' + video_file_path)

    if 'nb_frames' not in video_stream:
        raise RuntimeError('Video stream has no nb_frames property in ' + video_file_path)

    # Average frame rate often expressed as fraction so eval() calculates it
    frame_rate = round(eval(video_stream['avg_frame_rate']))
    seek_seconds = (timestamp - video_timestamp).seconds
    seek_frame = frame_rate * seek_seconds

    # Do we have enough frames to find the frame we're interested in?
    if int(video_stream['nb_frames']) >= seek_frame:
        out, err = (
            ffmpeg
            .input(video_file_path)
            .filter('select', 'gte(n,{})'.format(seek_frame))
            .output('pipe:', vframes=1, format='image2')
            .run(capture_stdout=True)
        )

        if err:
            raise RuntimeError('Error retrieving video frame: ' + err)

        return out, os.path.basename(video_file_path), seek_frame
