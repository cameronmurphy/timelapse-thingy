import os
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import config

API_BASE_URL = 'https://dev.virtualearth.net'
REST_MAP_ENDPOINT = 'REST/V1/Imagery/Map'
DOWNLOAD_RETRIES = 5
DOWNLOAD_BACKOFF_FACTOR = 0.3


def build(current_position_lat, current_position_long, output_path):
    url = _build_url(current_position_lat, current_position_long)
    print(url)

    session = requests.Session()

    retry = Retry(
        total=DOWNLOAD_RETRIES,
        read=DOWNLOAD_RETRIES,
        connect=DOWNLOAD_RETRIES,
        backoff_factor=DOWNLOAD_BACKOFF_FACTOR
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    response = session.get(url)

    with open(output_path, 'wb') as output_file:
        output_file.write(response.content)


def _build_url(current_position_lat, current_position_long):
    args = _build_url_args(current_position_lat, current_position_long)

    return os.path.join(
        API_BASE_URL,
        REST_MAP_ENDPOINT,
        config.map_type,
        _build_map_centre_coords_path_segment(),
        str(config.map_zoom) + '?' + '&'.join(args)
    )


def _build_url_args(current_position_lat, current_position_long):
    push_pins = list(config.map_push_pin_dict_list)

    if current_position_lat is not None and current_position_long is not None:
        push_pins += [_build_current_position_push_pin(current_position_lat, current_position_long)]

    push_pin_args = list(map(_build_push_pin_arg, push_pins))
    return [_build_map_size_arg(), _build_format_arg()] + push_pin_args + [_build_key_arg()]


def _build_current_position_push_pin(lat, long):
    return {
        'lat': lat,
        'long': long,
        'icon': config.map_current_position_icon,
    }


def _build_map_centre_coords_path_segment():
    return '{},{}'.format(config.map_centre_coord_dict['lat'], config.map_centre_coord_dict['long'])


def _build_map_size_arg():
    return 'mapSize={},{}'.format(config.map_dimensions_dict['width'], config.map_dimensions_dict['height'])


def _build_format_arg():
    return 'format={}'.format(config.map_format)


def _build_key_arg():
    return 'key={}'.format(config.bing_maps_api_key)


def _build_push_pin_arg(push_pin):
    return 'pp={},{};{};{}'.format(
        push_pin['lat'],
        push_pin['long'],
        push_pin['icon'],
        '' if 'text' not in push_pin else push_pin['text']
    )
