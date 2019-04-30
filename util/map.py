import os

import config

API_BASE_URL = 'https://dev.virtualearth.net'
ROAD_MAP_ENDPOINT = 'REST/V1/Imagery/Map/Road'


def build(current_position_coords_dict):
    map_centre_coords_path_segment = '{},{}'.format(
        config.map_centre_coord_dict['lat'],
        config.map_centre_coord_dict['long']
    )

    args = ['mapSize={},{}'.format(config.map_dimensions_dict['width'], config.map_dimensions_dict['height'])]
    args += list(map(build_push_pin_arg, config.map_push_pin_dict_list))
    args += ['key={}'.format(config.bing_maps_api_key)]

    url = os.path.join(
        API_BASE_URL,
        ROAD_MAP_ENDPOINT,
        map_centre_coords_path_segment,
        str(config.map_zoom) + '?' + '&&'.join(args)
    )

    print(url)


def build_push_pin_arg(push_pin):
    return 'pp={},{};{};{}'.format(push_pin['lat'], push_pin['long'], push_pin['icon'], push_pin['text'])
