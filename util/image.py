from datetime import datetime
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

from util import geo

DATETIME_ORIGINAL_TAG_NAME = 'DateTimeOriginal'
DATETIME_ORIGINAL_DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

GPS_INFO_TAG_NAME = 'GPSInfo'
GPS_LATITUDE_REF_TAG_NAME = 'GPSLatitudeRef'
GPS_LATITUDE_TAG_NAME = 'GPSLatitude'
GPS_LONGITUDE_REF_TAG_NAME = 'GPSLongitudeRef'
GPS_LONGITUDE_TAG_NAME = 'GPSLongitude'


def _get_tag_code(tag_list, tag_name):
    return list(tag_list.keys())[list(tag_list.values()).index(tag_name)]


def _get_exif_tag_code(tag_name):
    return _get_tag_code(TAGS, tag_name)


def _get_gps_exif_tag_code(tag_name):
    return _get_tag_code(GPSTAGS, tag_name)


def _get_exif_data(image, tag_name):
    exif_data = image._getexif()
    tag_code = _get_exif_tag_code(tag_name)

    if tag_code in exif_data:
        return exif_data[tag_code]


def open_image(filename):
    return Image.open(filename)


def get_timestamp(image):
    datetime_original_value = _get_exif_data(image, DATETIME_ORIGINAL_TAG_NAME)

    if datetime_original_value is not None:
        return datetime.strptime(datetime_original_value, DATETIME_ORIGINAL_DATE_FORMAT)

    return None


def get_gps_coords(image):
    gps_info = _get_exif_data(image, GPS_INFO_TAG_NAME)

    if gps_info is not None:
        lat_ref = gps_info[_get_gps_exif_tag_code(GPS_LATITUDE_REF_TAG_NAME)]
        (lat_degrees, lat_degrees_denom), (lat_minutes, lat_minutes_denom), (lat_seconds, lat_seconds_denom) =\
            gps_info[_get_gps_exif_tag_code(GPS_LATITUDE_TAG_NAME)]

        lat = geo.deg_to_decimal(
            lat_ref,
            lat_degrees / lat_degrees_denom,
            lat_minutes / lat_minutes_denom,
            lat_seconds / lat_seconds_denom
        )

        long_ref = gps_info[_get_gps_exif_tag_code(GPS_LONGITUDE_REF_TAG_NAME)]
        (long_degrees, long_degrees_denom), (long_minutes, long_minutes_denom), (long_seconds, long_seconds_denom) =\
            gps_info[_get_gps_exif_tag_code(GPS_LONGITUDE_TAG_NAME)]

        long = geo.deg_to_decimal(
            long_ref,
            long_degrees / long_degrees_denom,
            long_minutes / long_minutes_denom,
            long_seconds / long_seconds_denom
        )

        return lat, long

    return None, None
