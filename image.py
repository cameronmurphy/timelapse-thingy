from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


DATETIME_ORIGINAL_TAG_NAME = 'DateTimeOriginal'


def _get_exif_tag_code(tag_name):
    return list(TAGS.keys())[list(TAGS.values()).index(tag_name)]


def open_image(filename):
    return Image.open(filename)


def get_timestamp(image):
    if 'parsed_exif' not in image.info:
        raise RuntimeError('Image has no EXIF data')

    datetime_original_tag_code = _get_exif_tag_code(DATETIME_ORIGINAL_TAG_NAME)

    if datetime_original_tag_code not in image.info['parsed_exif']:
        raise RuntimeError('Image has no DateTimeOriginal EXIF tag')

    datetime_original_value = image.info['parsed_exif'][datetime_original_tag_code]

    return datetime.strptime(datetime_original_value, '%Y:%m:%d %H:%M:%S')
