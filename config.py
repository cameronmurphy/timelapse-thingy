import os
from dotenv import load_dotenv

frame_index_digits = None
source_index_digits = None
output_format = None
interval_round_to = None
montage_arg_list = None
montage_source_order_dict = None


def load():
    load_dotenv()
    
    global frame_index_digits
    global source_index_digits
    global output_format
    global interval_round_to
    global montage_arg_list
    global montage_source_order_dict

    frame_index_digits = int(os.getenv('FRAME_INDEX_DIGITS'))
    source_index_digits = int(os.getenv('SOURCE_INDEX_DIGITS'))
    output_format = os.getenv('OUTPUT_FORMAT')
    interval_round_to = int(os.getenv('INTERVAL_ROUND_TO'))
    montage_arg_list = eval(os.getenv('MONTAGE_ARG_LIST'))
    montage_source_order_dict = eval(os.getenv('MONTAGE_SOURCE_ORDER_DICT'))
