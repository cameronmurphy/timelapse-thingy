import os
from dotenv import load_dotenv

frame_index_digits = None
source_index_digits = None
output_format = None
interval_round_to = None
montage_arg_list = None
montage_source_order_dict = None
bing_maps_api_key = None
map_zoom = None
map_centre_coord_dict = None
map_dimensions_dict = None
map_push_pin_dict_list = None
map_current_position_icon = None


def load():
    load_dotenv()
    
    global frame_index_digits
    global source_index_digits
    global output_format
    global interval_round_to
    global montage_arg_list
    global montage_source_order_dict
    global bing_maps_api_key
    global map_zoom
    global map_centre_coord_dict
    global map_dimensions_dict
    global map_push_pin_dict_list
    global map_current_position_icon

    frame_index_digits = int(os.getenv('FRAME_INDEX_DIGITS'))
    source_index_digits = int(os.getenv('SOURCE_INDEX_DIGITS'))
    output_format = os.getenv('OUTPUT_FORMAT')
    interval_round_to = int(os.getenv('INTERVAL_ROUND_TO'))
    montage_arg_list = eval(os.getenv('MONTAGE_ARG_LIST'))
    montage_source_order_dict = eval(os.getenv('MONTAGE_SOURCE_ORDER_DICT'))
    bing_maps_api_key = os.getenv('BING_MAPS_API_KEY')
    map_zoom = int(os.getenv('MAP_ZOOM'))
    map_centre_coord_dict = eval(os.getenv('MAP_CENTRE_COORDS_DICT'))
    map_dimensions_dict = eval(os.getenv('MAP_DIMENSIONS_DICT'))
    map_push_pin_dict_list = eval(os.getenv('MAP_PUSH_PIN_DICT_LIST'))
    map_current_position_icon = int(os.getenv('MAP_CURRENT_POSITION_ICON'))
